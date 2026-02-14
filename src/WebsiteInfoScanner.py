# Website-Info-Scanner by isrt

import os
import sys
import time
import re
import socket
import concurrent.futures
import ssl
import urllib3
from urllib.parse import urlparse

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError:
    print("[ERROR] Module 'requests' oder 'beautifulsoup4' fehlen.")
    print("Installation: pip install requests beautifulsoup4")
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
yellow = rgb(255, 215, 0)

BEFORE = f"{purple}[{white}WEB{purple}]"
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
    prompt = f"{purple}[{white}{label}{purple}] {white}URL ► {reset()}"
    clean_prompt = re.sub(r"\033\[[0-9;]+m", "", prompt)
    padding = max(0, (width - len(clean_prompt)) // 2)
    sys.stdout.write(" " * padding + prompt)
    sys.stdout.flush()
    return input()

def Slow(text: str, delay: float = 0.002):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def Error(msg):
    print(f"\n{purple}[{red}ERROR{purple}] {white}{msg}{reset()}")

def Continue():
    print()
    input(f"{purple}[{white}ENTER{purple}] {white}Drücke Enter zum Fortfahren...{reset()}")

# ===== Scanner Logik =====

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}

def ScanWebsite(url):
    try:
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        domain = urlparse(url).netloc
        ip = socket.gethostbyname(domain)
        
        results = []
        results.append(f"{INFO_ADD} Website    : {white}{url}{reset()}")
        results.append(f"{INFO_ADD} Domain     : {white}{domain}{reset()}")
        results.append(f"{INFO_ADD} IP Address : {white}{ip}{reset()}")
        
        # Status & Security
        response = requests.get(url, timeout=10, headers=HEADERS, verify=False)
        results.append(f"{INFO_ADD} Status     : {white}{response.status_code}{reset()}")
        results.append(f"{INFO_ADD} SSL Secure : {white}{url.startswith('https://')}{reset()}")
        
        # Tech Detection
        soup = BeautifulSoup(response.content, 'html.parser')
        server = response.headers.get('Server', 'Unknown')
        powered = response.headers.get('X-Powered-By', 'Unknown')
        results.append(f"{INFO_ADD} Server     : {white}{server}{reset()}")
        results.append(f"{INFO_ADD} Powered By : {white}{powered}{reset()}")
        
        # Simple Tech Check
        techs = []
        if soup.find('script', src=re.compile(r'jquery', re.I)): techs.append("jQuery")
        if soup.find('link', href=re.compile(r'bootstrap', re.I)): techs.append("Bootstrap")
        if techs:
            results.append(f"{INFO_ADD} Techs Found: {white}{', '.join(techs)}{reset()}")

        # Print all with Slow effect
        print(f"\n{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\n")
        for line in results:
            Slow(line)
        print(f"\n{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
        
    except Exception as e:
        Error(f"Scan fehlgeschlagen: {e}")

def main():
    try:
        clear()
        set_title("Surreal - Website Info Scanner")

        frame_top()
        target = surreal_prompt("WEBSITE")
        frame_bottom()

        if not target.strip():
            Error("Eingabe darf nicht leer sein.")
            Continue()
            return

        typing_effect(
            f"{BEFORE} {current_time_hour()} {AFTER} {WAIT} Analyzing Website & Technologies..",
            0.03,
            purple,
            centered=True,
        )

        ScanWebsite(target)
        Continue()

    except KeyboardInterrupt:
        print(f"\n{INFO_ADD} {white}Scanner gestoppt.{reset()}")
    except Exception as e:
        Error(str(e))
        Continue()

if __name__ == "__main__":
    main()