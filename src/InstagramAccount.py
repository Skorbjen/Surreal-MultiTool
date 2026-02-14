# Instagram-Account by isrt

import os
import sys
import time
import re
import contextlib

try:
    import instaloader
except ImportError:
    print("[ERROR] Modul 'instaloader' fehlt. Installiere es mit: pip install instaloader")
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

BEFORE = f"{purple}[{white}INSTA{purple}]"
AFTER = ""
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
    prompt = f"{purple}[{white}{label}{purple}] {white}Username ► {reset()}"
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

# ===== Instagram Logik =====

def Search(username):
    @contextlib.contextmanager
    def SuppressOutput():
        with open(os.devnull, 'w') as devnull:
            old_stdout = sys.stdout
            old_stderr = sys.stderr
            sys.stdout = devnull
            sys.stderr = devnull
            try:
                yield
            finally:
                sys.stdout = old_stdout
                sys.stderr = old_stderr

    try:
        with SuppressOutput():
            loader = instaloader.Instaloader()
            profile = instaloader.Profile.from_username(loader.context, username)
        
        info = f"""
{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────

 {INFO_ADD} Username       : {white}{profile.username}
 {INFO_ADD} ID             : {white}{profile.userid}
 {INFO_ADD} Full Name      : {white}{profile.full_name}
 {INFO_ADD} Biography      : {white}{profile.biography}
 {INFO_ADD} URL Bio        : {white}{profile.external_url}
 {INFO_ADD} Followers      : {white}{profile.followers}
 {INFO_ADD} Following      : {white}{profile.followees}
 {INFO_ADD} Verified       : {white}{'True' if profile.is_verified else 'False'}
 {INFO_ADD} Private        : {white}{'True' if profile.is_private else 'False'}
 {INFO_ADD} Business       : {white}{'True' if profile.is_business_account else 'False'}"""

        if profile.is_business_account:
            info += f"\n {INFO_ADD} Category       : {white}{profile.business_category_name}"

        info += f"\n\n{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────"
        Slow(info)

        # Posts anzeigen, falls nicht privat
        if not profile.is_private:
            typing_effect(f"\n{INFO_ADD} Lade letzte Beiträge..", 0.03, purple)
            posts = profile.get_posts()
            for i, post in enumerate(posts):
                if i >= 3: break # Max 3 Beiträge für die Übersicht
                post_info = f"""
 {INFO_ADD} Post n°{i+1}
 {INFO_ADD} URL            : {white}https://www.instagram.com/p/{post.shortcode}/
 {INFO_ADD} Date           : {white}{post.date}
 {INFO_ADD} Likes          : {white}{post.likes}
 {INFO_ADD} Comments       : {white}{post.comments}
 {INFO_ADD} Caption        : {white}{str(post.caption)[:50]}..."""
                Slow(post_info)
            print(f"{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")

    except Exception as e:
        Error(f"Account '{username}' konnte nicht gefunden werden oder ist gesperrt.")

def main():
    try:
        clear()
        set_title("Surreal - Instagram Lookup")

        frame_top()
        user = surreal_prompt("INSTAGRAM")
        frame_bottom()

        if not user.strip():
            Error("Eingabe darf nicht leer sein.")
            Continue()
            return

        typing_effect(
            f"{BEFORE} {current_time_hour()} {AFTER} {WAIT} Fetching Instagram Profile Data..",
            0.03,
            purple,
            centered=True,
        )

        Search(user)
        Continue()

    except KeyboardInterrupt:
        print(f"\n{INFO_ADD} {white}Abgebrochen.{reset()}")
    except Exception as e:
        Error(str(e))
        Continue()

if __name__ == "__main__":
    main()