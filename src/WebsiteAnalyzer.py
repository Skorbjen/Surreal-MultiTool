# Website-Vulnerability-Scanner by isrt

import os
import sys
import time
import re

try:
    import requests
except ImportError:
    print("[ERROR] Modul 'requests' fehlt. Installiere es mit: pip install requests")
    sys.exit(1)

# Design Basics

def rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m"

def reset():
    return "\033[0m"

purple_dark = rgb(75, 0, 130)
purple = rgb(138, 43, 226)
purple_light = rgb(186, 85, 211)
purple_lighter = rgb(221, 160, 221)
white = rgb(255, 255, 255)
gray = rgb(150, 150, 150)
red = rgb(255, 80, 80)
green = rgb(80, 255, 80)
yellow = rgb(255, 215, 0)

BEFORE = f"{purple}[{white}SCAN{purple}]"
BEFORE_GREEN = f"{purple}[{green}VULN{purple}]"
AFTER = ""
WAIT = f"{yellow}WAIT{purple}"
INFO_ADD = f"{purple}[{white}INFO{purple}]"
GEN_VALID = f"{green}FOUND{purple}"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def set_title(title):
    if os.name == "nt":
        t = title.replace("&", "^&").replace("<", "^<").replace(">", "^>").replace("|", "^|")
        os.system(f"title {t}")
    else:
        sys.stdout.write(f"\033]0;{title}\007")
        sys.stdout.flush()

def current_time_hour():
    return time.strftime("%H:%M:%S")

def typing_effect(text, speed=0.03, color=None, centered=False):
    width = 120
    try:
        import shutil
        width = shutil.get_terminal_size((120, 24)).columns
    except Exception: pass

    if centered:
        clean_text = re.sub(r"\033\[[0-9;]+m", "", text)
        padding = max(0, (width - len(clean_text)) // 2)
        sys.stdout.write(" " * padding)
    if color: sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(speed)
    if color: sys.stdout.write(reset())
    print()

def frame_top():
    width = 120
    try:
        import shutil
        width = shutil.get_terminal_size((120, 24)).columns
    except Exception: pass
    bar = "─" * max(20, width - 2)
    print(f"{purple_dark}┌{bar}┐{reset()}")

def frame_bottom():
    width = 120
    try:
        import shutil
        width = shutil.get_terminal_size((120, 24)).columns
    except Exception: pass
    bar = "─" * max(20, width - 2)
    print(f"{purple_dark}└{bar}┘{reset()}")

def surreal_prompt(label):
    width = 120
    try:
        import shutil
        width = shutil.get_terminal_size((120, 24)).columns
    except Exception: pass
    prompt = f"{purple}[{white}{label}{purple}] {white}► {reset()}"
    clean_prompt = re.sub(r"\033\[[0-9;]+m", "", prompt)
    padding = max(0, (width - len(clean_prompt)) // 2)
    sys.stdout.write(" " * padding + prompt)
    sys.stdout.flush()
    return input()

def Error(msg):
    print(f"\n{purple}[{red}ERROR{purple}] {white}{msg}{reset()}")

def Continue():
    print()
    input(f"{purple}[{white}ENTER{purple}] {white}Drücke Enter zum Fortfahren...{reset()}")

# ===== Vulnerability Scanner Logik =====

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def CheckPaths(url, paths, vuln_name):
    found = False
    base_url = url if url.endswith("/") else url + "/"
    for path in paths:
        try:
            response = requests.get(base_url + path, timeout=5, headers=HEADERS)
            if response.status_code == 200:
                found = True
                print(f"{BEFORE_GREEN} {current_time_hour()} {GEN_VALID} {white}{vuln_name}: {green}/{path}{reset()}")
        except: continue
    if not found:
        print(f"{BEFORE} {current_time_hour()} {purple}[{red}NONE{purple}] {white}{vuln_name}: {gray}Keine Pfade gefunden{reset()}")

def TestPayloads(url, payloads, indicators, vuln_name):
    found = False
    try:
        orig_res = requests.get(url, timeout=7, headers=HEADERS)
        base_url = url if url.endswith("/") else url + "/"
        for payload in payloads:
            try:
                res = requests.get(base_url + payload, timeout=5, headers=HEADERS)
                if res.status_code == 200 and res.text != orig_res.text:
                    for indicator in indicators:
                        if indicator.lower() in res.text.lower():
                            found = True
                            print(f"{BEFORE_GREEN} {current_time_hour()} {GEN_VALID} {white}{vuln_name}: {green}{payload}{reset()}")
                            break
            except: continue
    except: pass
    if not found:
        print(f"{BEFORE} {current_time_hour()} {purple}[{red}NONE{purple}] {white}{vuln_name}: {gray}Nicht anfällig{reset()}")

def main():
    try:
        clear()
        set_title("Surreal - Vulnerability Scanner")

        frame_top()
        url = surreal_prompt("TARGET URL")
        frame_bottom()

        if not url.strip():
            Error("Eingabe darf nicht leer sein.")
            Continue()
            return

        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        typing_effect(
            f"{BEFORE} {current_time_hour()} {AFTER} {WAIT} Searching for Vulnerabilities..",
            0.03,
            purple,
            centered=True,
        )
        print(f"\n{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\n")

        # SQL Injection
        sql_p = ["'", '"', "' OR '1'='1'", "admin'--"]
        sql_i = ["SQL syntax", "mysql", "Unclosed quotation mark", "ORA-"]
        TestPayloads(url, sql_p, sql_i, "SQL Injection")

        # XSS
        xss_p = ["<script>alert(1)</script>", "<img src=x onerror=alert(1)>"]
        xss_i = ["<script>", "alert(", "onerror="]
        TestPayloads(url, xss_p, xss_i, "XSS")

        # Pfad-Checks
        paths = ["admin", "config.php", ".env", "backup", "logs", "api/v1"]
        CheckPaths(url, paths, "Sensitive Path")

        # Files
        files = ["etc/passwd", "wp-config.php", "server-status"]
        CheckPaths(url, files, "Sensitive File")

        print(f"\n{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
        Continue()

    except KeyboardInterrupt:
        print(f"\n{INFO_ADD} {white}Scanner gestoppt.{reset()}")
    except Exception as e:
        Error(str(e))
        Continue()

if __name__ == "__main__":
    main()