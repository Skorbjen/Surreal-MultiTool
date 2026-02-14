# Phone-Number-Lookup by isrt

import os
import sys
import time
import re

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except ImportError:
    print("[ERROR] Modul 'phonenumbers' fehlt. Installiere es mit: pip install phonenumbers")
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

BEFORE = f"{purple}[{white}PHONE{purple}]"
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
    prompt = f"{purple}[{white}{label}{purple}] {white}Number ► {reset()}"
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

# ===== Phone Lookup Logik =====

def Lookup(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            Error("Die Telefonnummer ist ungültig.")
            return

        status = "Valid"
        country_code = f"+{parsed_number.country_code}"
        
        try: operator = carrier.name_for_number(parsed_number, "en") or "Unknown"
        except: operator = "Unknown"
            
        try: 
            timezones = timezone.time_zones_for_number(parsed_number)
            timezone_info = timezones[0] if timezones else "Unknown"
        except: timezone_info = "Unknown"
            
        try: country = geocoder.country_name_for_number(parsed_number, "en") or "Unknown"
        except: country = "Unknown"
            
        try: region = geocoder.description_for_number(parsed_number, "en") or "Unknown"
        except: region = "Unknown"
            
        try: formatted = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL)
        except: formatted = "Unknown"

        result = f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

 {INFO_ADD} Phone        : {white}{phone_number}
 {INFO_ADD} Formatted    : {white}{formatted}
 {INFO_ADD} Status       : {white}{status}
 {INFO_ADD} Country Code : {white}{country_code}
 {INFO_ADD} Country      : {white}{country}
 {INFO_ADD} Region       : {white}{region}
 {INFO_ADD} Timezone     : {white}{timezone_info}
 {INFO_ADD} Operator     : {white}{operator}

{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"""
        Slow(result)

    except Exception:
        Error("Ungültiges Format! Bitte nutze das internationale Format (z.B. +49...)")

def main():
    try:
        clear()
        set_title("Surreal - Phone Number Lookup")

        frame_top()
        number = surreal_prompt("PHONE")
        frame_bottom()

        if not number.strip():
            Error("Eingabe darf nicht leer sein.")
            Continue()
            return

        typing_effect(
            f"{BEFORE} {current_time_hour()} {AFTER} {WAIT} Retrieving Phone Information..",
            0.03,
            purple,
            centered=True,
        )

        Lookup(number)
        Continue()

    except KeyboardInterrupt:
        print(f"\n{INFO_ADD} {white}Abgebrochen.{reset()}")
    except Exception as e:
        Error(str(e))
        Continue()

if __name__ == "__main__":
    main()