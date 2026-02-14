# Email-Lookup by isrt

import os
import sys
import time
import re

try:
    import dns.resolver
except ImportError:
    print("[ERROR] Modul 'dnspython' fehlt. Installiere es mit: pip install dnspython")
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

BEFORE = f"{purple}[{white}EMAIL{purple}]"
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

def surreal_prompt_email():
    width = 120
    try:
        import shutil
        width = shutil.get_terminal_size((120, 24)).columns
    except Exception:
        pass

    prompt = f"{purple}[{white}EMAIL LOOKUP{purple}] {white}Email ► {reset()}"
    clean_prompt = re.sub(r"\033\[[0-9;]+m", "", prompt)
    padding = max(0, (width - len(clean_prompt)) // 2)
    sys.stdout.write(" " * padding + prompt)
    sys.stdout.flush()
    return input()

def Censored(value: str):
    if "@" in value:
        name, domain = value.split("@", 1)
        if len(name) > 2:
            name_mask = name[0] + "*" * (len(name) - 2) + name[-1]
        else:
            name_mask = "*" * len(name)
        masked = name_mask + "@" + domain
    else:
        masked = "*" * len(value)
    print(f"{BEFORE} {gray}[CENSORED]{reset()} {white}{masked}{reset()}")

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

# ===== Lookup-Logik =====

def GetEmailInfo(email):
    info = {}
    try:
        domain_all = email.split('@')[-1]
    except Exception:
        domain_all = None
    try:
        name = email.split('@')[0]
    except Exception:
        name = None
    try:
        domain = re.search(r"@([^@.]+)\.", email).group(1)
    except Exception:
        domain = None
    try:
        tld = f".{email.split('.')[-1]}"
    except Exception:
        tld = None

    try:
        mx_records = dns.resolver.resolve(domain_all, 'MX')
        mx_servers = [str(record.exchange) for record in mx_records]
        info["mx_servers"] = mx_servers
    except Exception:
        info["mx_servers"] = None

    try:
        spf_records = dns.resolver.resolve(domain_all, 'SPF')
        info["spf_records"] = [str(record) for record in spf_records]
    except Exception:
        info["spf_records"] = None

    try:
        dmarc_records = dns.resolver.resolve(f"_dmarc.{domain_all}", 'TXT')
        info["dmarc_records"] = [str(record) for record in dmarc_records]
    except Exception:
        info["dmarc_records"] = None

    mx_servers = info.get("mx_servers") or []
    for server in mx_servers:
        if "google.com" in server:
            info["google_workspace"] = True
        elif "outlook.com" in server:
            info["microsoft_365"] = True

    return info, domain_all, domain, tld, name

def main():
    try:
        clear()
        set_title("Surreal - Email Lookup")

        frame_top()
        email = surreal_prompt_email()
        frame_bottom()

        Censored(email)
        typing_effect(
            f"{BEFORE} {current_time_hour()} {AFTER} {WAIT} Information Recovery..",
            0.03,
            purple,
            centered=True,
        )

        info, domain_all, domain, tld, name = GetEmailInfo(email)

        try:
            mx_servers = info["mx_servers"]
            if mx_servers:
                mx_servers = " / ".join(mx_servers)
        except Exception:
            mx_servers = None

        try:
            spf_records = info["spf_records"]
        except Exception:
            spf_records = None

        try:
            dmarc_records = info["dmarc_records"]
            if dmarc_records:
                dmarc_records = " / ".join(dmarc_records)
        except Exception:
            dmarc_records = None

        try:
            google_workspace = info["google_workspace"]
        except Exception:
            google_workspace = None

        try:
            mailgun_validation = info["mailgun_validation"]
            if mailgun_validation:
                mailgun_validation = " / ".join(mailgun_validation)
        except Exception:
            mailgun_validation = None

        Slow(f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

{INFO_ADD} Email      : {white}{email}{red}
{INFO_ADD} Name       : {white}{name}{red}
{INFO_ADD} Domain     : {white}{domain}{red}
{INFO_ADD} TLD        : {white}{tld}{red}
{INFO_ADD} Domain All : {white}{domain_all}{red}
{INFO_ADD} Servers    : {white}{mx_servers}{red}
{INFO_ADD} SPF        : {white}{spf_records}{red}
{INFO_ADD} DMARC      : {white}{dmarc_records}{red}
{INFO_ADD} Workspace  : {white}{google_workspace}{red}
{INFO_ADD} Mailgun    : {white}{mailgun_validation}{red}

{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
""")

        Continue()

    except Exception as e:
        Error(e)

if __name__ == "__main__":
    main()
