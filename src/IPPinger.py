# Ip-Pinger by isrt

import os
import sys
import time
import re
import socket
import concurrent.futures

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
yellow = rgb(255, 215, 0)

BEFORE = f"{purple}[{white}PING{purple}]"
AFTER = ""
INPUT = f"{white}INPUT{purple}"
WAIT = f"{yellow}WAIT{purple}"
INFO_ADD = f"{purple}[{white}INFO{purple}]"

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
    except Exception:
        pass

    if centered:
        clean_text = re.sub(r"\033\[[0-9;]+m", "", text)
        padding = max(0, (width - len(clean_text)) // 2)
        sys.stdout.write(" " * padding)
    if color:
        sys.stdout.write(color)
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(speed)
    if color:
        sys.stdout.write(reset())
    print()

def frame_top():
    width = 120
    try:
        import shutil
        width = shutil.get_terminal_size((120, 24)).columns
    except Exception:
        pass
    bar = "─" * max(20, width - 2)
    print(f"{purple_dark}┌{bar}┐{reset()}")

def frame_bottom():
    width = 120
    try:
        import shutil
        width = shutil.get_terminal_size((120, 24)).columns
    except Exception:
        pass
    bar = "─" * max(20, width - 2)
    print(f"{purple_dark}└{bar}┘{reset()}")

def surreal_prompt(label):
    width = 120
    try:
        import shutil
        width = shutil.get_terminal_size((120, 24)).columns
    except Exception:
        pass

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
    input(f"{purple}[{white}ENTER{purple}] {white}Drücke Enter zum Beenden/Fortfahren...{reset()}")

# ===== Pinger-Logik =====

def PingIp(hostname, port, num_bytes):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(2)
            start_time = time.time()
            sock.connect((hostname, port))
            data = b'\x00' * num_bytes
            sock.sendall(data)
            end_time = time.time()
            elapsed_time = (end_time - start_time) * 1000
            print(f"{BEFORE} {white}Host: {purple_light}{hostname}{reset} {white}Time: {purple_lighter}{elapsed_time:.2f}ms{reset} {white}Port: {white}{port}{reset} {white}Status: {white}Succeed{reset}")
    except socket.timeout:
        print(f"{BEFORE} {white}Host: {purple_light}{hostname}{reset} {red}Timeout{reset} {white}Port: {white}{port}{reset} {red}Status: Fail{reset}")
    except Exception as e:
        print(f"{BEFORE} {white}Host: {purple_light}{hostname}{reset} {red}Fail{reset} {white}Port: {white}{port}{reset} {red}Status: {e}{reset}")

def main():
    try:
        clear()
        set_title("Surreal - IP Pinger")

        frame_top()
        hostname = surreal_prompt("TARGET IP")
        
        if not hostname.strip():
            frame_bottom()
            Error("IP darf nicht leer sein.")
            Continue()
            return

        try:
            port_input = surreal_prompt("PORT (Default: 80)")
            port = int(port_input) if port_input.strip() else 80
            
            bytes_input = surreal_prompt("BYTES (Default: 64)")
            num_bytes = int(bytes_input) if bytes_input.strip() else 64
        except ValueError:
            frame_bottom()
            Error("Port und Bytes müssen Zahlen sein.")
            Continue()
            return
            
        frame_bottom()

        typing_effect(
            f"{BEFORE} {current_time_hour()} {AFTER} {WAIT} Connecting to Host..",
            0.03,
            purple,
            centered=True,
        )

        try:
            target_ip = socket.gethostbyname(hostname)
        except socket.gaierror:
            Error(f"Host '{hostname}' nicht gefunden.")
            Continue()
            return

        print(f"\n{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\n")

        with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
            while True:
                executor.submit(PingIp, target_ip, port, num_bytes)
                time.sleep(0.7)

    except KeyboardInterrupt:
        print(f"\n\n{INFO_ADD} {white}Gestoppt durch Nutzer.{reset()}")
        Continue()
    except Exception as e:
        Error(f"Fehler: {e}")
        Continue()

if __name__ == "__main__":
    main()