# Website-Url-Scanner by isrt

import os
import sys
import time
import re
from urllib.parse import urljoin, urlparse

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

BEFORE = f"{purple}[{white}URL{purple}]"
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

# ===== Scanner Logik =====

HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
all_links = set()

def IsValidExtension(url):
    return re.search(r'\.(html|xhtml|php|js|css)$', url) or not re.search(r'\.\w+$', url)

def ExtractLinks(base_url, domain, soup):
    extracted = []
    tags = soup.find_all(['a', 'link', 'script', 'img', 'iframe', 'form'])
    for tag in tags:
        attr = tag.get('href') or tag.get('src') or tag.get('action')
        if attr:
            full_url = urljoin(base_url, attr)
            if domain in full_url and IsValidExtension(full_url) and full_url not in all_links:
                all_links.add(full_url)
                extracted.append(full_url)
    return extracted

def FindUrls(website_url, recursive=False):
    try:
        domain = urlparse(website_url).netloc
        response = requests.get(website_url, headers=HEADERS, timeout=10)
        if response.status_code != 200:
            Error(f"Status {response.status_code} für {website_url}")
            return

        soup = BeautifulSoup(response.content, 'html.parser')
        new_links = ExtractLinks(website_url, domain, soup)

        for link in new_links:
            print(f"{BEFORE} {white}Gefunden: {purple_light}{link}{reset()}")
            if recursive:
                # Einfache Rekursion für "All Website"
                time.sleep(0.1)
                FindUrls(link, recursive=False)

    except Exception as e:
        Error(f"Fehler bei {website_url}: {e}")

def main():
    try:
        clear()
        set_title("Surreal - Website URL Scanner")

        frame_top()
        url = surreal_prompt("WEBSITE URL")
        if not url.strip():
            frame_bottom()
            Error("Eingabe darf nicht leer sein.")
            Continue()
            return
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        print(f"\n{purple}[{white}01{purple}] {white}Nur Startseite{reset()}")
        print(f"{purple}[{white}02{purple}] {white}Ganze Website (Deep Scan){reset()}")
        choice = surreal_prompt("CHOICE")
        frame_bottom()

        typing_effect(
            f"{BEFORE} {current_time_hour()} {AFTER} {WAIT} Crawling for Links..",
            0.03,
            purple,
            centered=True,
        )

        print(f"\n{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\n")
        
        if choice in ['1', '01']:
            FindUrls(url, recursive=False)
        else:
            FindUrls(url, recursive=True)

        print(f"\n{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")
        Continue()

    except KeyboardInterrupt:
        print(f"\n{INFO_ADD} {white}Scanner gestoppt.{reset()}")
    except Exception as e:
        Error(str(e))
        Continue()

if __name__ == "__main__":
    main()