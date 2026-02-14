# Ip-Lookup by isrt

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
yellow = rgb(255, 215, 0)

BEFORE = f"{purple}[{white}IP{purple}]"
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

def surreal_prompt_ip():
    width = 120
    try:
        import shutil
        width = shutil.get_terminal_size((120, 24)).columns
    except Exception:
        pass

    prompt = f"{purple}[{white}IP LOOKUP{purple}] {white}IP ► {reset()}"
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

def Continue():
    input(f"\n{purple}[{white}ENTER{purple}] {white}Drücke Enter zum Fortfahren...{reset()}")

def Error(e: Exception):
    print(f"{purple}[{red}ERROR{purple}] {red}{e}{reset()}")

# IP-Lookup Logik

def get_ip_info(ip):
    try:
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=10)
        response.raise_for_status()
        api = response.json()
        
        status = "Valid" if api.get('status') == "success" else "Invalid"
        country = api.get('country', "None")
        country_code = api.get('countryCode', "None")
        region = api.get('regionName', "None")
        region_code = api.get('region', "None")
        zip_code = api.get('zip', "None")
        city = api.get('city', "None")
        latitude = api.get('lat', "None")
        longitude = api.get('lon', "None")
        timezone = api.get('timezone', "None")
        isp = api.get('isp', "None")
        org = api.get('org', "None")
        as_host = api.get('as', "None")
        
        return {
            'status': status,
            'country': country,
            'country_code': country_code,
            'region': region,
            'region_code': region_code,
            'zip': zip_code,
            'city': city,
            'latitude': latitude,
            'longitude': longitude,
            'timezone': timezone,
            'isp': isp,
            'org': org,
            'as': as_host
        }
    except Exception:
        return None

def main():
    try:
        clear()
        set_title("Surreal - IP Lookup")
        # Banner entfernt

        frame_top()
        ip = surreal_prompt_ip()
        frame_bottom()

        typing_effect(
            f"{BEFORE} {current_time_hour()} {AFTER} {WAIT} Search for information..",
            0.03,
            purple,
            centered=True,
        )

        ip_info = get_ip_info(ip)
        
        if ip_info:
            Slow(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

{INFO_ADD} Status     : {white}{ip_info['status']}{red}
{INFO_ADD} Country    : {white}{ip_info['country']} ({ip_info['country_code']}){red}
{INFO_ADD} Region     : {white}{ip_info['region']} ({ip_info['region_code']}){red}
{INFO_ADD} Zip        : {white}{ip_info['zip']}{red}
{INFO_ADD} City       : {white}{ip_info['city']}{red}
{INFO_ADD} Latitude   : {white}{ip_info['latitude']}{red}
{INFO_ADD} Longitude  : {white}{ip_info['longitude']}{red}
{INFO_ADD} Timezone   : {white}{ip_info['timezone']}{red}
{INFO_ADD} ISP        : {white}{ip_info['isp']}{red}
{INFO_ADD} Org        : {white}{ip_info['org']}{red}
{INFO_ADD} AS         : {white}{ip_info['as']}{red}

{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
""")
        else:
            Error(Exception("Keine IP-Informationen gefunden"))

        Continue()

    except Exception as e:
        Error(e)

if __name__ == "__main__":
    main()
