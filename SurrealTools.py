import os
import sys
import time
import webbrowser
from pathlib import Path
from colorama import init
import re
import shutil
import socket

# Colorama initialisieren für Windows
init(autoreset=True)

PASSWORD = "surreal"
MAX_TRIES = 3

def clear():
    """Löscht den Terminal-Bildschirm"""
    os.system('cls' if os.name == 'nt' else 'clear')

def set_title(title):
    """Setzt den Terminal-Titel"""
    if os.name == 'nt':  # Windows
        title = title.replace('&', '^&').replace('<', '^<').replace('>', '^>').replace('|', '^|')
        os.system(f'title {title}')
    else:  # Linux/Mac
        print(f'\033]0;{title}\007', end='')

def rgb(r, g, b):
    """Gibt RGB-Farbe für Terminal zurück"""
    return f"\033[38;2;{r};{g};{b}m"

def reset():
    """Reset Farbe"""
    return "\033[0m"

# Farben - Purple gradient shades
purple_dark = rgb(75, 0, 130)
purple = rgb(138, 43, 226)
purple_light = rgb(186, 85, 211)
purple_lighter = rgb(221, 160, 221)
white = rgb(255, 255, 255)
gray = rgb(150, 150, 150)

# Options 
option_01 = "Website Analyzer"
option_02 = "Website Info Scanner"
option_03 = "Website Url Scanner"
option_04 = "IP Analyzer"
option_05 = "Port Scanner "
option_06 = "Ping Tool"
option_07 = "Document Creator"
option_08 = "Tracker "
option_09 = "Image Exif"
option_10 = "Search Tool"
option_11 = "Username Search"
option_12 = "Email Lookup"
option_13 = "Email Search"
option_14 = "Phone Lookup "
option_15 = "IP Lookup"
option_16 = "Social Account Info"
option_17 = "Email Simulator"
option_18 = "Password Manager"
option_19 = "Hash Calculator"
option_20 = "Encryption Tool"
option_21 = "Database Search"
option_22 = " "
option_23 = " "
option_24 = " "
option_25 = " "
option_26 = " "
option_27 = " "
option_28 = " "
option_29 = " "
option_30 = " "
option_31 = " "
option_32 = " "
option_33 = " "
option_34 = " "
option_35 = " "
option_36 = " "
option_37 = " "
option_38 = " "
option_39 = " "
option_40 = " "
option_41 = " "
option_42 = " "
option_43 = " "
option_44 = " "
option_45 = " "
option_46 = " "
option_47 = " "
option_48 = " "
option_49 = " "
option_50 = " "
option_51 = " "
option_52 = " "
option_53 = " "
option_54 = " "
option_55 = " "
option_56 = " "
option_57 = " "
option_58 = " "
option_59 = " "
option_60 = " "
option_61 = " "
option_62 = " "
option_63 = " "
option_64 = " "
option_65 = " "
option_66 = " "
option_67 = " "
option_68 = " "
option_69 = " "
option_70 = " "
option_71 = " "
option_72 = " "
option_73 = " "
option_74 = " "
option_75 = " "
option_76 = " "
option_77 = " "
option_78 = " "
option_79 = " "
option_80 = " "
option_81 = " "
option_82 = " "
option_83 = " "
option_84 = " "
option_85 = " "
option_86 = " "
option_87 = " "
option_88 = " "
option_89 = " "
option_90 = " "
option_91 = " "
option_92 = " "
option_93 = " "
option_94 = " "
option_95 = " "
option_96 = " "
option_97 = " "
option_98 = " "
option_99 = " "
option_100 = " "

# Option Text formatiert
option_01_txt = f"{purple}[{white}01{purple}]{white} " + option_01
option_02_txt = f"{purple}[{white}02{purple}]{white} " + option_02
option_03_txt = f"{purple}[{white}03{purple}]{white} " + option_03
option_04_txt = f"{purple}[{white}04{purple}]{white} " + option_04
option_05_txt = f"{purple}[{white}05{purple}]{white} " + option_05
option_06_txt = f"{purple}[{white}06{purple}]{white} " + option_06
option_07_txt = f"{purple}[{white}07{purple}]{white} " + option_07
option_08_txt = f"{purple}[{white}08{purple}]{white} " + option_08
option_09_txt = f"{purple}[{white}09{purple}]{white} " + option_09
option_10_txt = f"{purple}[{white}10{purple}]{white} " + option_10
option_11_txt = f"{purple}[{white}11{purple}]{white} " + option_11
option_12_txt = f"{purple}[{white}12{purple}]{white} " + option_12
option_13_txt = f"{purple}[{white}13{purple}]{white} " + option_13
option_14_txt = f"{purple}[{white}14{purple}]{white} " + option_14
option_15_txt = f"{purple}[{white}15{purple}]{white} " + option_15
option_16_txt = f"{purple}[{white}16{purple}]{white} " + option_16
option_17_txt = f"{purple}[{white}17{purple}]{white} " + option_17
option_18_txt = f"{purple}[{white}18{purple}]{white} " + option_18
option_19_txt = f"{purple}[{white}19{purple}]{white} " + option_19
option_20_txt = f"{purple}[{white}20{purple}]{white} " + option_20
option_21_txt = f"{purple}[{white}21{purple}]{white} " + option_21
option_22_txt = f"{purple}[{white}22{purple}]{white} " + option_22
option_23_txt = f"{purple}[{white}23{purple}]{white} " + option_23
option_24_txt = f"{purple}[{white}24{purple}]{white} " + option_24
option_25_txt = f"{purple}[{white}25{purple}]{white} " + option_25
option_26_txt = f"{purple}[{white}26{purple}]{white} " + option_26
option_27_txt = f"{purple}[{white}27{purple}]{white} " + option_27
option_28_txt = f"{purple}[{white}28{purple}]{white} " + option_28
option_29_txt = f"{purple}[{white}29{purple}]{white} " + option_29
option_30_txt = f"{purple}[{white}30{purple}]{white} " + option_30
option_31_txt = f"{purple}[{white}31{purple}]{white} " + option_31
option_32_txt = f"{purple}[{white}32{purple}]{white} " + option_32
option_33_txt = f"{purple}[{white}33{purple}]{white} " + option_33
option_34_txt = f"{purple}[{white}34{purple}]{white} " + option_34
option_35_txt = f"{purple}[{white}35{purple}]{white} " + option_35
option_36_txt = f"{purple}[{white}36{purple}]{white} " + option_36
option_37_txt = f"{purple}[{white}37{purple}]{white} " + option_37
option_38_txt = f"{purple}[{white}38{purple}]{white} " + option_38
option_39_txt = f"{purple}[{white}39{purple}]{white} " + option_39
option_40_txt = f"{purple}[{white}40{purple}]{white} " + option_40
option_41_txt = f"{purple}[{white}41{purple}]{white} " + option_41
option_42_txt = f"{purple}[{white}42{purple}]{white} " + option_42
option_43_txt = f"{purple}[{white}43{purple}]{white} " + option_43
option_44_txt = f"{purple}[{white}44{purple}]{white} " + option_44
option_45_txt = f"{purple}[{white}45{purple}]{white} " + option_45
option_46_txt = f"{purple}[{white}46{purple}]{white} " + option_46
option_47_txt = f"{purple}[{white}47{purple}]{white} " + option_47
option_48_txt = f"{purple}[{white}48{purple}]{white} " + option_48
option_49_txt = f"{purple}[{white}49{purple}]{white} " + option_49
option_50_txt = f"{purple}[{white}50{purple}]{white} " + option_50
option_51_txt = f"{purple}[{white}51{purple}]{white} " + option_51
option_52_txt = f"{purple}[{white}52{purple}]{white} " + option_52
option_53_txt = f"{purple}[{white}53{purple}]{white} " + option_53
option_54_txt = f"{purple}[{white}54{purple}]{white} " + option_54
option_55_txt = f"{purple}[{white}55{purple}]{white} " + option_55
option_56_txt = f"{purple}[{white}56{purple}]{white} " + option_56
option_57_txt = f"{purple}[{white}57{purple}]{white} " + option_57
option_58_txt = f"{purple}[{white}58{purple}]{white} " + option_58
option_59_txt = f"{purple}[{white}59{purple}]{white} " + option_59
option_60_txt = f"{purple}[{white}60{purple}]{white} " + option_60
option_61_txt = f"{purple}[{white}61{purple}]{white} " + option_61
option_62_txt = f"{purple}[{white}62{purple}]{white} " + option_62
option_63_txt = f"{purple}[{white}63{purple}]{white} " + option_63
option_64_txt = f"{purple}[{white}64{purple}]{white} " + option_64
option_65_txt = f"{purple}[{white}65{purple}]{white} " + option_65
option_66_txt = f"{purple}[{white}66{purple}]{white} " + option_66
option_67_txt = f"{purple}[{white}67{purple}]{white} " + option_67
option_68_txt = f"{purple}[{white}68{purple}]{white} " + option_68
option_69_txt = f"{purple}[{white}69{purple}]{white} " + option_69
option_70_txt = f"{purple}[{white}70{purple}]{white} " + option_70
option_71_txt = f"{purple}[{white}71{purple}]{white} " + option_71
option_72_txt = f"{purple}[{white}72{purple}]{white} " + option_72
option_73_txt = f"{purple}[{white}73{purple}]{white} " + option_73
option_74_txt = f"{purple}[{white}74{purple}]{white} " + option_74
option_75_txt = f"{purple}[{white}75{purple}]{white} " + option_75
option_76_txt = f"{purple}[{white}76{purple}]{white} " + option_76
option_77_txt = f"{purple}[{white}77{purple}]{white} " + option_77
option_78_txt = f"{purple}[{white}78{purple}]{white} " + option_78
option_79_txt = f"{purple}[{white}79{purple}]{white} " + option_79
option_80_txt = f"{purple}[{white}80{purple}]{white} " + option_80
option_81_txt = f"{purple}[{white}81{purple}]{white} " + option_81
option_82_txt = f"{purple}[{white}82{purple}]{white} " + option_82
option_83_txt = f"{purple}[{white}83{purple}]{white} " + option_83
option_84_txt = f"{purple}[{white}84{purple}]{white} " + option_84
option_85_txt = f"{purple}[{white}85{purple}]{white} " + option_85
option_86_txt = f"{purple}[{white}86{purple}]{white} " + option_86
option_87_txt = f"{purple}[{white}87{purple}]{white} " + option_87
option_88_txt = f"{purple}[{white}88{purple}]{white} " + option_88
option_89_txt = f"{purple}[{white}89{purple}]{white} " + option_89
option_90_txt = f"{purple}[{white}90{purple}]{white} " + option_90
option_91_txt = f"{purple}[{white}91{purple}]{white} " + option_91
option_92_txt = f"{purple}[{white}92{purple}]{white} " + option_92
option_93_txt = f"{purple}[{white}93{purple}]{white} " + option_93
option_94_txt = f"{purple}[{white}94{purple}]{white} " + option_94
option_95_txt = f"{purple}[{white}95{purple}]{white} " + option_95
option_96_txt = f"{purple}[{white}96{purple}]{white} " + option_96
option_97_txt = f"{purple}[{white}97{purple}]{white} " + option_97
option_98_txt = f"{purple}[{white}98{purple}]{white} " + option_98
option_99_txt = f"{purple}[{white}99{purple}]{white} " + option_99
option_100_txt = f"{purple}[{white}100{purple}]{white} " + option_100

option_info_txt = f"{purple}[{white}I{purple}]{white} Info"
option_site_txt = f"{purple}[{white}S{purple}]{white} Site"
option_next_txt = f"Next {purple}[{white}N{purple}]{white}"

# New single-column menu to prevent breaking
menu1 = f"""

{white}                                            {option_info_txt} ─ {option_site_txt} ─ {option_next_txt} {reset()}

{purple}        ─═━═─ Network Tools ─═━═─                   ─═━═─ Osint ─═━═─                    ─═━═─ Utilities ─═━═─{reset()}
{option_01_txt}                           {option_10_txt}                   {option_16_txt}
{option_02_txt}                       {option_11_txt}               {option_17_txt}
{option_03_txt}                        {option_12_txt}                  {option_18_txt}
{option_04_txt}                                {option_13_txt}                  {option_19_txt}
{option_05_txt}                              {option_14_txt}      {option_20_txt}
{option_06_txt}                                  {option_15_txt}                     {option_21_txt}



{purple_light}   {reset()}
"""

def get_terminal_width():
    return shutil.get_terminal_size((120, 24)).columns

def center_text(text, width=None):
    """Zentriert Text"""
    if width is None:
        width = get_terminal_width()
    clean_text = re.sub(r'\033\[[0-9;]+m', '', text)
    padding = max(0, (width - len(clean_text)) // 2)
    return " " * padding + text

def typing_effect(text, speed=0.03, color=None, centered=False):
    """Zeigt Text mit Typing-Effekt"""
    width = get_terminal_width()
    if centered:
        clean_text = re.sub(r'\033\[[0-9;]+m', '', text)
        padding = max(0, (width - len(clean_text)) // 2)
        sys.stdout.write(" " * padding)
    
    if color:
        sys.stdout.write(color)
    
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)
    
    if color:
        sys.stdout.write(reset())
    print()

def loading_animation(duration=2):
    """Zeigt eine coole Loading-Animation"""
    frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
    end_time = time.time() + duration
    i = 0
    width = get_terminal_width()
    
    while time.time() < end_time:
        text = f"{frames[i % len(frames)]} Loading Surreal..."
        clean_text = re.sub(r'\033\[[0-9;]+m', '', text)
        padding = max(0, (width - len(clean_text)) // 2)
        sys.stdout.write(f"\r{' ' * width}\r{' ' * padding}{purple}{text}{reset()}")
        sys.stdout.flush()
        time.sleep(0.1)
        i += 1
    
    sys.stdout.write("\r" + " " * width + "\r")
    sys.stdout.flush()

def progress_bar(duration=1.5, text="Initializing"):
    """Zeigt eine Progress Bar"""
    bar_length = 40
    width = get_terminal_width()
    
    for i in range(bar_length + 1):
        percent = (i / bar_length) * 100
        filled = "█" * i
        empty = "░" * (bar_length - i)
        
        # Farbverlauf in purple shades
        r = int(75 + (221 - 75) * (i / bar_length))
        g = int(0 + (160 - 0) * (i / bar_length))
        b = int(130 + (221 - 130) * (i / bar_length))
        
        bar_text = f"{text}: [{filled}{empty}] {percent:.0f}%"
        clean_bar = re.sub(r'\033\[[0-9;]+m', '', bar_text)
        padding = max(0, (width - len(clean_bar)) // 2)
        
        sys.stdout.write(f"\r{' ' * width}\r{' ' * padding}{rgb(r, g, b)}{bar_text}{reset()}")
        sys.stdout.flush()
        time.sleep(duration / bar_length)
    
    print()

def banner_animated():
    """Surreal ASCII-Art Banner mit Animation (original restored)"""
    lines = [
        "                                         .▄▄ · ▄• ▄▌▄▄▄  ▄▄▄  ▄▄▄ . ▄▄▄· ▄▄▌      ",
        "                                         ▐█ ▀. █▪██▌▀▄ █·▀▄ █·▀▄.▀·▐█ ▀█ ██•      ",
        "                                         ▄▀▀▀█▄█▌▐█▌▐▀▀▄ ▐▀▀▄ ▐▀▀▪▄▄█▀▀█ ██▪      ",
        "                                         ▐█▄▪▐█▐█▄█▌▐█•█▌▐█•█▌▐█▄▄▌▐█ ▪▐▌▐█▌▐▌    ",
        "                                          ▀▀▀▀  ▀▀▀ .▀  ▀.▀  ▀ ▀▀▀  ▀  ▀ .▀▀▀     "
    ]
    
    colors = [
        purple_dark,
        rgb(100, 20, 180),
        purple,
        purple_light,
        purple_lighter
    ]
    
    print("\n")
    width = get_terminal_width()
    for i, line in enumerate(lines):
        print(f"{colors[i]}{line}{reset()}")
        time.sleep(0.15)
    print()

def banner():
    """Surreal ASCII-Art Banner ohne Animation (original restored)"""
    lines = [
        "                                         .▄▄ · ▄• ▄▌▄▄▄  ▄▄▄  ▄▄▄ . ▄▄▄· ▄▄▌      ",
        "                                         ▐█ ▀. █▪██▌▀▄ █·▀▄ █·▀▄.▀·▐█ ▀█ ██•      ",
        "                                         ▄▀▀▀█▄█▌▐█▌▐▀▀▄ ▐▀▀▄ ▐▀▀▪▄▄█▀▀█ ██▪      ",
        "                                         ▐█▄▪▐█▐█▄█▌▐█•█▌▐█•█▌▐█▄▄▌▐█ ▪▐▌▐█▌▐▌    ",
        "                                          ▀▀▀▀  ▀▀▀ .▀  ▀.▀  ▀ ▀▀▀  ▀  ▀ .▀▀▀     "
    ]
    
    colors = [
        purple_dark,
        rgb(100, 20, 180),
        purple,
        purple_light,
        purple_lighter
    ]
    
    print("\n")
    width = get_terminal_width()
    for i, line in enumerate(lines):
        print(f"{colors[i]}{line}{reset()}")
    print()
# Zeigt Discord Namen Oben Rechts an
def display_user_tag(username):
    width = get_terminal_width()
    box_width = len(username) + 4
    spaces_count = max(0, width - box_width - 2)
    spaces = " " * spaces_count
    
    print(f"{spaces}{purple_dark}┌{'─' * box_width}┐{reset()}")
    print(f"{spaces}{purple_dark}│ {white}{username.center(box_width - 2)}{purple_dark} │{reset()}")
    print(f"{spaces}{purple_dark}└{'─' * box_width}┘{reset()}")

def get_discord_username():
    """Liest Discord-Username aus lokalen Dateien"""
    try:
        if os.name == 'nt':  # Windows
            base_paths = [
                os.path.join(os.getenv('APPDATA'), 'discord'),
                os.path.join(os.getenv('APPDATA'), 'discordcanary'),
                os.path.join(os.getenv('APPDATA'), 'discordptb')
            ]
        else:  # Linux/Mac
            base_paths = [
                os.path.join(Path.home(), '.config', 'discord'),
                os.path.join(Path.home(), '.config', 'discordcanary'),
                os.path.join(Path.home(), '.config', 'discordptb')
            ]
        
        for base_path in base_paths:
            local_storage_path = os.path.join(base_path, 'Local Storage', 'leveldb')
            
            if os.path.exists(local_storage_path):
                for file in os.listdir(local_storage_path):
                    if file.endswith(('.ldb', '.log')):
                        file_path = os.path.join(local_storage_path, file)
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                                content = f.read()
                                
                                if '"username":"' in content:
                                    start = content.find('"username":"') + len('"username":"')
                                    end = content.find('"', start)
                                    username = content[start:end]
                                    if username and 0 < len(username) < 50:
                                        return username
                        except:
                            continue
        
        return "Unknown User"
    except:
        return "Unknown User"

def credits_page():
    """Zeigt die Credits-Seite"""
    clear()
    set_title("Surreal - Credits")
    
    print("\n\n\n")
    width = get_terminal_width()
    
    lines = [
        (purple_dark, f"╔{'═' * 45}╗"),
        (rgb(90, 10, 150), f"║{' ' * 45}║"),
        (rgb(110, 30, 170), f"║{' ' * 14}{white}SURREAL{rgb(110, 30, 170)}{' ' * 24}║"),
        (rgb(130, 50, 190), f"║{' ' * 45}║"),
        (rgb(150, 70, 210), f"║{' ' * 16}{rgb(200, 200, 200)}v1.0{rgb(150, 70, 210)}{' ' * 25}║"),
        (rgb(170, 90, 230), f"║{' ' * 45}║"),
        (purple_light, f"║{'─' * 45}║"),
        (rgb(190, 110, 230), f"║{' ' * 45}║"),
        (rgb(210, 130, 230), f"║{' ' * 12}{white}Developer{rgb(210, 130, 230)}{' ' * 24}║"),
        (rgb(221, 160, 221), f"║{' ' * 17}{purple}isrt{rgb(221, 160, 221)}{' ' * 24}║"),
        (rgb(230, 170, 230), f"║{' ' * 45}║"),
        (purple_lighter, f"╚{'═' * 45}╝"),
    ]
    
    for color, line in lines:
        print(f"{color}{line}{reset()}")
        time.sleep(0.1)
    
    print("\n\n")
    time.sleep(2.5)

def run_tool(filename, tool_name):
    """Startet ein Tool aus dem src Ordner"""
    import subprocess
    clear()
    typing_effect(f"{tool_name} wird gestartet...", 0.03, purple_light, centered=True)
    time.sleep(0.5)
    
    tool_path = os.path.join("src", filename)
    
    if os.path.exists(tool_path):
        try:
            # Python-Befehl abhängig vom System
            python_cmd = "python" if os.name == 'nt' else "python3"
            # subprocess.call wartet bis das Programm beendet ist
            subprocess.call([python_cmd, tool_path])
        except Exception as e:
            clear()
            typing_effect(f"Fehler beim Starten: {str(e)}", 0.03, rgb(255, 0, 0), centered=True)
            input(f"\n{purple}Drücke Enter um fortzufahren...{reset()}")
    else:
        clear()
        typing_effect(f"{filename} nicht gefunden in src/", 0.03, rgb(255, 0, 0), centered=True)
        input(f"\n{purple}Drücke Enter um fortzufahren...{reset()}")

def startup_sequence():
    """Startup Animation beim Programmstart"""
    clear()
    set_title("Surreal - Starting")
    
    print("\n\n\n")
    loading_animation(1.5)
    progress_bar(1.5, "Initializing System")
    time.sleep(0.3)

def login(discord_user):
    """Login-Funktion OHNE Versuche-Anzeige"""
    tries = MAX_TRIES
    
    while tries > 0:
        clear()
        set_title(f"Surreal - {discord_user}")
        display_user_tag(discord_user)
        banner_animated()
        
        # Nur Password Input, keine Versuche
        password_prompt = f"{purple}Passwort ► {reset()}"
        clean_prompt = re.sub(r'\033\[[0-9;]+m', '', password_prompt)
        width = get_terminal_width()
        padding = max(0, (width - len(clean_prompt) - 20) // 2)
        sys.stdout.write(" " * padding + password_prompt)
        sys.stdout.flush()
        input_pass = input()
        
        if input_pass == PASSWORD:
            clear()
            typing_effect("\nLogin erfolgreich!", 0.05, rgb(0, 255, 0), centered=True)
            progress_bar(1, "Loading Profile")
            return True
        else:
            tries -= 1
            if tries > 0:
                typing_effect("\nFalsches Passwort!", 0.05, rgb(255, 0, 0), centered=True)
                time.sleep(1)
    
    clear()
    set_title("Surreal - Gesperrt")
    typing_effect("\nZu viele Fehlversuche! System gesperrt.", 0.05, rgb(255, 0, 0), centered=True)
    typing_effect("Das Programm wird beendet.", 0.05, rgb(255, 100, 100), centered=True)
    input("\nDrücke Enter zum Beenden...")
    exit()

def main_menu(discord_user, hostname):
    """Hauptmenü"""
    while True:
        clear()
        set_title("Surreal - Menu 1")
        display_user_tag(discord_user)
        
        # Original banner with centering
        banner_lines = [
        "                                         .▄▄ · ▄• ▄▌▄▄▄  ▄▄▄  ▄▄▄ . ▄▄▄· ▄▄▌      ",
        "                                         ▐█ ▀. █▪██▌▀▄ █·▀▄ █·▀▄.▀·▐█ ▀█ ██•      ",
        "                                         ▄▀▀▀█▄█▌▐█▌▐▀▀▄ ▐▀▀▄ ▐▀▀▪▄▄█▀▀█ ██▪      ",
        "                                         ▐█▄▪▐█▐█▄█▌▐█•█▌▐█•█▌▐█▄▄▌▐█ ▪▐▌▐█▌▐▌    ",
        "                                          ▀▀▀▀  ▀▀▀ .▀  ▀.▀  ▀ ▀▀▀  ▀  ▀ .▀▀▀     ",
            "                                                                                              ",
            f"                                                 {white}github.com/skorbjen"
        ]
        
        colors = [
            purple_dark,
            rgb(100, 20, 180),
            purple,
            purple_light,
            purple_lighter,
            reset(),  # Empty line
            white  # GitHub link
        ]
        
        width = get_terminal_width()
        for i, line in enumerate(banner_lines):
            colored_line = f"{colors[i]}{line}{reset()}"
            print(colored_line)
        
        # Menu with centered lines
        menu_lines = menu1.split('\n')
        for line in menu_lines:
            if line.strip():  # Skip empty lines if needed
                print(line)
        
        # Input mit PC-Name
        choice = input(f"{purple} ┌──({white}{hostname}{gray}@surreal{purple})─[{gray}~/Surreal/Menu-1{purple}]\n └─{white}$ {reset()} ")
        
        if choice.lower() in ['n', 'next']:
            typing_effect("Next page coming soon...", 0.03, rgb(255, 255, 0), centered=True)
            time.sleep(1)
        elif choice.lower() in ['i', 'info']:
            credits_page()
        elif choice.lower() in ['s', 'site']:
            typing_effect("Site page coming soon...", 0.03, rgb(255, 255, 0), centered=True)
            time.sleep(1)
        elif choice == "01" or choice == "1":
            # Website Analyzer
            run_tool("WebsiteAnalyzer.py", "Website Analyzer")
        elif choice == "02" or choice == "2":
            # Website Info Scanner
            run_tool("WebsiteInfoScanner.py", "Website Info Scanner")
        elif choice == "03" or choice == "3":
            # Website URL Scanner
            run_tool("WebsiteUrlScanner.py", "Website URL Scanner")
        elif choice == "04" or choice == "4":
            # IP Analyzer
            run_tool("IPAnalyzer.py", "IP Analyzer")
        elif choice == "05" or choice == "5":
            # Port Scanner
            run_tool("IPPortScanner.py", "Port Scanner")
        elif choice == "06" or choice == "6":
            # Ping Tool
            run_tool("IPPinger.py", "Ping Tool")
        elif choice == "11":
            # Username Search
            run_tool("UsernameSearch.py", "Username Search")
        elif choice == "12":
            # Email Lookup
            run_tool("EmailLookup.py", "Email Lookup")
        elif choice == "13":
            # Email Search
            run_tool("EmailSearch.py", "Email Search")
        elif choice == "14":
            # Phone Lookup
            run_tool("PhoneLookup.py", "Phone Lookup")
        elif choice == "15":
            # IP Lookup
            run_tool("IPLookup.py", "IP Lookup")
        elif choice == "16":
            # Instagram Account
            run_tool("InstagramAccount.py", "Instagram Account")
        elif choice == "0":
            clear()
            typing_effect("\nAuf Wiedersehen!", 0.05, rgb(255, 255, 0), centered=True)
            time.sleep(1)
            exit()
        else:
            typing_effect("Feature coming soon...", 0.03, rgb(255, 255, 0), centered=True)
            time.sleep(1)

if __name__ == "__main__":
    # Startup Sequence
    startup_sequence()
    
    # Discord Username auslesen
    discord_username = get_discord_username()
    
    # PC Name (Hostname)
    hostname = socket.gethostname()
    
    # Login-Screen
    if login(discord_username):
        # Hauptmenü
        main_menu(discord_username, hostname)