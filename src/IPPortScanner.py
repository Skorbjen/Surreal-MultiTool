# Ip-Port-Scanner by isrt

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

BEFORE = f"{purple}[{white}PORT{purple}]"
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

def surreal_prompt_port():
    width = 120
    try:
        import shutil
        width = shutil.get_terminal_size((120, 24)).columns
    except Exception:
        pass

    prompt = f"{purple}[{white}PORT SCANNER{purple}] {white}IP ► {reset()}"
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

def Error(msg):
    # Fehlermeldung im Surreal-Style
    print(f"\n{purple}[{red}ERROR{purple}] {white}{msg}{reset()}")

# ===== Scanner-Logik =====

port_protocol_map = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS", 69: "TFTP",
    80: "HTTP", 110: "POP3", 123: "NTP", 143: "IMAP", 194: "IRC", 389: "LDAP",
    443: "HTTPS", 161: "SNMP", 3306: "MySQL", 5432: "PostgreSQL", 6379: "Redis",
    1521: "Oracle DB", 3389: "RDP"
}

def IdentifyProtocol(ip, port):
    if port in port_protocol_map:
        return port_protocol_map[port]
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.8)
            sock.connect((ip, port))
            sock.send(b"GET / HTTP/1.1\r\nHost: {}\r\n\r\n".format(ip).encode('utf-8'))
            response = sock.recv(100).decode('utf-8', errors='ignore')
            if "HTTP" in response: return "HTTP"
            return "Unknown"
    except Exception:
        return "Unknown"

def ScanPort(ip, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(0.4)
            result = sock.connect_ex((ip, port))
            if result == 0:
                protocol = IdentifyProtocol(ip, port)
                print(f"{BEFORE} {white}Port: {purple_light}{port:<5}{reset} {white}Status: {white}Open{reset} {white}Protocol: {purple_lighter}{protocol}{reset}")
    except Exception:
        pass

def PortScanner(ip):
    print(f"\n{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────\n")
    with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
        executor.map(lambda port: ScanPort(ip, port), range(1, 65536))
    print(f"\n{white}────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────")

def is_valid_ip(target):
    # Regex für einfache IP-Validierung
    ip_pattern = re.compile(r"^(?:[0-9]{1,3}\.){3}[0-9]{1,3}$")
    if ip_pattern.match(target):
        return True
    # Falls es ein Hostname ist (z.B. google.com), versuchen wir ihn aufzulösen
    try:
        socket.gethostbyname(target)
        return True
    except socket.gaierror:
        return False

def main():
    try:
        clear()
        set_title("Surreal - Port Scanner")

        frame_top()
        ip = surreal_prompt_port()
        frame_bottom()

        if not ip.strip():
            Error("Eingabe darf nicht leer sein.")
            Continue()
            return

        # Validierung mit Design-Feedback
        typing_effect(
            f"{BEFORE} {current_time_hour()} {AFTER} {WAIT} Validating Target..",
            0.03,
            purple,
            centered=True,
        )

        if not is_valid_ip(ip):
            Error(f"Ungültige IP oder Hostname: {white}{ip}")
            Continue()
            return

        typing_effect(
            f"{BEFORE} {current_time_hour()} {AFTER} {WAIT} Initiating Deep Scan..",
            0.03,
            purple,
            centered=True,
        )

        PortScanner(ip)
        Continue()

    except Exception as e:
        Error(str(e))

if __name__ == "__main__":
    main()