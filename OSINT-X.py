#!/usr/bin/env python3
# OSINT-X // Advanced Passive Recon CLI
# Author: ARGCYBERSKILLHUB
#
# Intended for domains, IPs, usernames and phone numbers you own or are
# authorized to investigate. Port scanning should only be used on authorized
    # systems.

import os
import socket
import time
import re
import shutil
import concurrent.futures
from urllib.parse import quote

try:
    import requests
except ImportError:
    requests = None

try:
    import phonenumbers
    from phonenumbers import geocoder, carrier, timezone
except ImportError:
    phonenumbers = None



# ------------------------- TERMINAL -------------------------

def clear():
    """Clear terminal screen on Windows PowerShell, CMD and Linux."""
    try:
        print("\033[2J\033[H", end="", flush=True)
    except Exception:
        pass


def term_width():
    try:
        return min(
            shutil.get_terminal_size((100, 28)).columns,
            110
        )
    except Exception:
        return 100


# ------------------------- THEME -------------------------

RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
CYAN = "\033[96m"
BLUE = "\033[94m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RED = "\033[91m"
MAGENTA = "\033[95m"
WHITE = "\033[97m"
GRAY = "\033[90m"


def c(text, color=WHITE):
    return f"{color}{text}{RESET}"

def clear():
    """Cross-platform terminal clear."""
    print("\033[2J\033[H", end="", flush=True)



def term_width():
    return min(shutil.get_terminal_size((100, 28)).columns, 110)


def pause():
    input(c("\n  [ENTER] Return to main console...", GRAY))


def progress(label, steps=24, delay=0.018):
    print(f"\n  {c(label, CYAN)}")

    for i in range(steps + 1):
        filled = "█" * i
        empty = "░" * (steps - i)
        pct = int(i / steps * 100)

        print(
            f"\r  {c(filled + empty, CYAN)} {pct:3d}%",
            end="",
            flush=True
        )

        time.sleep(delay)

    print()


# ------------------------- BANNER -------------------------

def banner():
    clear()

    art = [
               "   ██████╗ ███████╗██╗███╗   ██╗████████╗     ██╗  ██╗",
               "  ██╔═══██╗██╔════╝██║████╗  ██║╚══██╔══╝     ╚██╗██╔╝",
               "  ██║   ██║███████╗██║██╔██╗ ██║   ██║  ████║  ╚███╔╝ ",
               "  ██║   ██║╚════██║██║██║╚██╗██║   ██║         ██╔██╗ ",
               "  ╚██████╔╝███████║██║██║ ╚████║   ██║        ██╔╝ ██╗",
               "   ╚═════╝ ╚══════╝╚═╝╚═╝  ╚═══╝   ╚═╝        ╚═╝  ╚═╝",
    ]

    alien = [
               "                 .-''''-.",
               "               .'  _    _ '.",
               "              /   (o)  (o)  \\",
               "             :                :",
               "             |      __        |",
               "             :    .'  '.      :",
               "              \\   \\____/     /",
               "               '.          .'",
               "                 '-.____.-'",
               "                    /||\\",
               "                   /_||_\\",
               "                     ||",
               "                    /  \\+Coded by ARGCYBERSKILLHUB"
    ]

    print("\033[96m")
    for line in art:
        print(line)

    print("\033[95m")
    for line in alien:
        print(line)



    print(c(
        "    ┌────────────────────────────────────────────────────────────┐",
        BLUE
    ))

    print(c(
        "    │  OSINT-X  //  PASSIVE INTELLIGENCE CONSOLE                 │",
        WHITE
    ))

    print(c(
        "    │  DOMAIN • DNS • PORTS • SUBDOMAINS • USERNAME • PHONE      │",
        WHITE
    ))

    print(c(
        "    └────────────────────────────────────────────────────────────┘",
        BLUE
    ))



    print()


def startup_animation():
    clear()

    circle = [
        "◜",
        "◝",
        "◞",
        "◟",
    ]

    for _ in range(8):
        for frame in circle:
            clear()

            print("\n\n")
            print(c("                  " + frame, CYAN))
            print(c("             ╔══════════════╗", MAGENTA))
            print(c("             ║   OSINT-X    ║", GREEN))
            print(c("             ╚══════════════╝", MAGENTA))
            print()
            print(c("              SYSTEM LOADING", RED))

            time.sleep(0.10)

    clear()
   


# ------------------------- HELPERS -------------------------

def normalize_domain(value):
    value = value.strip()
    value = re.sub(r"^https?://", "", value, flags=re.I)
    value = value.split("/")[0].split(":")[0]
    return value.lower().strip()


def resolve_host(host):
    try:
        return socket.gethostbyname(host)
    except Exception:
        return None


def get_json(url, timeout=8, headers=None):
    if requests is None:
        return None

    try:
        r = requests.get(
            url,
            timeout=timeout,
            headers=headers or {
                "User-Agent": "ARG-Recon-X/3.0"
            }
        )

        r.raise_for_status()
        return r.json()

    except Exception:
        return None


def print_kv(key, value, color=WHITE):
    print(f"  {c(key.ljust(18), CYAN)} {c(str(value), color)}")


def section(title):
    width = max(4, term_width() - len(title) - 8)

    print()
    print(
        c(
            "  ╭─ " + title + " " + "─" * width + "╮",
            BLUE
        )
    )


def end_section():
    print(
        c(
            "  ╰" + "─" * max(1, term_width() - 4) + "╯",
            BLUE
        )
    )


def _dns_available():
    try:
        import dns.resolver
        return True
    except ImportError:
        return False


# ------------------------- DOMAIN -------------------------

def domain_info():
    section("DOMAIN INTELLIGENCE")

    domain = normalize_domain(input("  Target domain: "))

    if not domain:
        return

    progress("Resolving DNS", 18, 0.015)

    ip = resolve_host(domain)

    print()
    print_kv("Domain", domain)
    print_kv(
        "IPv4",
        ip or "Resolution failed",
        GREEN if ip else RED
    )

    try:
        aliases = socket.gethostbyname_ex(domain)

        print_kv("Canonical", aliases[0])
        print_kv(
            "Aliases",
            ", ".join(aliases[1]) if aliases[1] else "None"
        )

    except Exception:
        pass

    # RDAP
    if requests:
        data = get_json(
            f"https://rdap.org/domain/{quote(domain)}"
        )

        if data:
            section("RDAP REGISTRATION")

            print_kv(
                "Handle",
                data.get("handle", "N/A")
            )

            print_kv(
                "Status",
                ", ".join(data.get("status", [])) or "N/A"
            )

            events = data.get("events", [])

            for ev in events:
                if ev.get("eventAction") in (
                    "registration",
                    "expiration",
                    "last changed"
                ):
                    print_kv(
                        ev.get("eventAction", ""),
                        ev.get("eventDate", "N/A")
                    )

            nameservers = []

            for ns in data.get("nameservers", []):
                if ns.get("ldhName"):
                    nameservers.append(ns["ldhName"])

            if nameservers:
                print_kv(
                    "Nameservers",
                    ", ".join(nameservers[:8])
                )

            end_section()

    # DNS
    section("COMMON DNS RECORDS")

    try:
        import dns.resolver

        for rtype in (
            "A",
            "AAAA",
            "MX",
            "NS",
            "TXT",
            "CNAME"
        ):
            try:
                answers = dns.resolver.resolve(
                    domain,
                    rtype,
                    lifetime=4
                )

                vals = [
                    str(a).strip('"')
                    for a in answers
                ]

                print_kv(
                    rtype,
                    " | ".join(vals[:8])
                    if vals
                    else "None"
                )

            except Exception:
                print_kv(
                    rtype,
                    "None / unavailable",
                    GRAY
                )

    except ImportError:
        print_kv(
            "DNS",
            "Install dnspython for full record enumeration",
            YELLOW
        )

    end_section()
    pause()


# ------------------------- PORT SCANNER -------------------------

COMMON_PORTS = [
    20, 21, 22, 23, 25, 53, 67, 68, 69,
    80, 110, 111, 123, 135, 137, 138, 139,
    143, 161, 389, 443, 445, 465, 514, 587,
    636, 873, 993, 995, 1433, 1521, 2049,
    2375, 3000, 3306, 3389, 5000, 5432,
    5900, 5985, 6379, 6443, 8000, 8080,
    8081, 8443, 9000, 9200, 27017
]


PORT_NAMES = {
    21: "FTP",
    22: "SSH",
    23: "Telnet",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    135: "MS-RPC",
    139: "NetBIOS",
    143: "IMAP",
    161: "SNMP",
    389: "LDAP",
    443: "HTTPS",
    445: "SMB",
    465: "SMTPS",
    587: "SMTP",
    636: "LDAPS",
    873: "Rsync",
    993: "IMAPS",
    995: "POP3S",
    1433: "MSSQL",
    1521: "Oracle",
    2049: "NFS",
    2375: "Docker API",
    3000: "Dev HTTP",
    3306: "MySQL",
    3389: "RDP",
    5000: "App",
    5432: "PostgreSQL",
    5900: "VNC",
    6379: "Redis",
    6443: "Kubernetes",
    8000: "HTTP-alt",
    8080: "HTTP-proxy",
    8081: "HTTP-alt",
    8443: "HTTPS-alt",
    9000: "App",
    9200: "Elasticsearch",
    27017: "MongoDB"
}


def check_port(host, port, timeout):
    s = socket.socket(
        socket.AF_INET,
        socket.SOCK_STREAM
    )

    s.settimeout(timeout)

    try:
        result = s.connect_ex((host, port))
        return port if result == 0 else None

    except Exception:
        return None

    finally:
        s.close()


def port_scan():
    section("TCP PORT SCANNER")

    host = input(
        "  Authorized target IP/domain: "
    ).strip()

    if not host:
        return

    ip = resolve_host(host) or host

    print_kv("Resolved target", ip)

    mode = input(
        "  Scan [1] common ports  [2] custom range: "
    ).strip() or "1"

    if mode == "2":
        try:
            start = int(
                input("  Start port (1-65535): ")
            )

            end = int(
                input("  End port (1-65535): ")
            )

            if (
                not (1 <= start <= end <= 65535)
                or end - start > 2000
            ):
                print(
                    c(
                        "  Range must be 1-65535 and <= 2000 ports.",
                        RED
                    )
                )
                return

            ports = list(range(start, end + 1))

        except ValueError:
            print(c("  Invalid range.", RED))
            return

    else:
        ports = COMMON_PORTS[:]

    print(
        c(
            "  Use only on systems you own or have permission to test.",
            YELLOW
        )
    )

    workers = 40
    opened = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=workers
    ) as ex:

        futures = [
            ex.submit(check_port, ip, p, 0.55)
            for p in ports
        ]

        for fut in concurrent.futures.as_completed(futures):
            p = fut.result()

            if p:
                opened.append(p)

                print(
                    f"  {c('OPEN', GREEN)}  "
                    f"{str(p).ljust(6)} "
                    f"{PORT_NAMES.get(p, 'Unknown service')}"
                )

    opened.sort()

    section("SCAN SUMMARY")

    print_kv("Target", ip)
    print_kv("Ports checked", len(ports))
    print_kv(
        "Open ports",
        len(opened),
        GREEN if opened else GRAY
    )

    if not opened:
        print(
            c(
                "  No open TCP ports found in the selected range.",
                GRAY
            )
        )

    end_section()
    pause()


# ------------------------- SUBDOMAINS -------------------------

DEFAULT_SUBS = """
www mail smtp pop imap ftp api dev test staging beta app admin portal
blog shop store cdn static assets ns1 ns2 mx vpn remote git gitlab
dashboard panel docs support status monitor secure login auth m
"""


def subdomain_enum():
    section("SUBDOMAIN ENUMERATOR")

    domain = normalize_domain(
        input("  Target domain: ")
    )

    if not domain:
        return

    custom = input(
        "  Custom wordlist file [ENTER = built-in]: "
    ).strip()

    words = []

    if custom:
        try:
            with open(
                custom,
                "r",
                encoding="utf-8",
                errors="ignore"
            ) as f:
                words = [
                    x.strip()
                    for x in f
                    if x.strip() and not x.startswith("#")
                ]

        except OSError as e:
            print(
                c(
                    f"  Could not read wordlist: {e}",
                    RED
                )
            )
            return

    else:
        words = DEFAULT_SUBS.split()

    print(
        c(
            f"  Checking {len(words)} labels...",
            CYAN
        )
    )

    found = []

    def resolve_sub(sub):
        fqdn = f"{sub}.{domain}"

        try:
            answers = socket.gethostbyname_ex(fqdn)
            return fqdn, answers[2]

        except Exception:
            return None

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=25
    ) as ex:

        futures = [
            ex.submit(resolve_sub, s)
            for s in words
        ]

        for fut in concurrent.futures.as_completed(futures):
            result = fut.result()

            if result:
                found.append(result)

                print(
                    f"  {c('[+]', GREEN)} "
                    f"{result[0]:35} "
                    f"{', '.join(result[1])}"
                )

    section("ENUMERATION SUMMARY")

    print_kv("Base domain", domain)
    print_kv("Candidates", len(words))
    print_kv(
        "Resolved",
        len(found),
        GREEN if found else GRAY
    )

    end_section()
    pause()


# ------------------------- IP INFO -------------------------

def ip_info():
    section("IP INTELLIGENCE")

    target = input(
        "  IP address or hostname: "
    ).strip()

    if not target:
        return

    ip = resolve_host(target) or target

    print_kv("Target", target)
    print_kv("Resolved IPv4", ip)

    progress(
        "Collecting public routing/geo metadata",
        20,
        0.012
    )

    data = get_json(
        f"https://ipwho.is/{quote(ip)}"
    )

    if data and data.get("success") is not False:

        fields = [
            ("continent", "Continent"),
            ("country", "Country"),
            ("region", "Region"),
            ("city", "City"),
            ("postal", "Postal"),
            ("latitude", "Latitude"),
            ("longitude", "Longitude"),
            ("isp", "ISP"),
            ("org", "Organization"),
            ("asn", "ASN"),
            ("timezone", "Timezone")
        ]

        for key, label in fields:
            if key in data:
                print_kv(
                    label,
                    data.get(key, "N/A")
                )

    else:
        print(
            c(
                "  Public IP metadata service unavailable.",
                RED
            )
        )

    try:
        hostname = socket.gethostbyaddr(ip)[0]
        print_kv("Reverse DNS", hostname)

    except Exception:
        print_kv("Reverse DNS", "None")

    end_section()

    print(
        c(
            "  Note: IP geolocation is approximate and does not identify "
            "a person's exact location.",
            YELLOW
        )
    )

    pause()


# ------------------------- USERNAME -------------------------
PLATFORMS = [
    # Code / developer
    ("GitHub", "https://github.com/{}"),
    ("GitLab", "https://gitlab.com/{}"),
    ("Bitbucket", "https://bitbucket.org/{}"),
    ("Codeberg", "https://codeberg.org/{}"),
    ("SourceForge", "https://sourceforge.net/u/{}/"),
    ("Stack Overflow", "https://stackoverflow.com/users/{}"),
    ("Dev.to", "https://dev.to/{}"),
    ("HackerRank", "https://www.hackerrank.com/{}"),
    ("LeetCode", "https://leetcode.com/{}"),
    ("CodePen", "https://codepen.io/{}"),
    ("Replit", "https://replit.com/@{}"),
    ("Kaggle", "https://www.kaggle.com/{}"),
    ("Docker Hub", "https://hub.docker.com/u/{}"),

    # Social
    ("Reddit", "https://www.reddit.com/user/{}"),
    ("X", "https://x.com/{}"),
    ("Instagram", "https://www.instagram.com/{}/"),
    ("Facebook", "https://www.facebook.com/{}"),
    ("Pinterest", "https://www.pinterest.com/{}/"),
    ("Threads", "https://www.threads.net/@{}"),
    ("Tumblr", "https://{}.tumblr.com/"),
    ("Mastodon", "https://mastodon.social/@{}"),
    ("Bluesky", "https://bsky.app/profile/{}"),

    # Media / streaming
    ("YouTube", "https://www.youtube.com/@{}"),
    ("Twitch", "https://www.twitch.tv/{}"),
    ("Vimeo", "https://vimeo.com/{}"),
    ("SoundCloud", "https://soundcloud.com/{}"),
    ("Mixcloud", "https://www.mixcloud.com/{}"),
    ("Bandcamp", "https://{}.bandcamp.com/"),

    # Professional
    ("LinkedIn", "https://www.linkedin.com/in/{}"),
    ("About.me", "https://about.me/{}"),
    ("Gravatar", "https://gravatar.com/{}"),

    # Writing / publishing
    ("Medium", "https://medium.com/@{}"),
    ("WordPress", "https://{}.wordpress.com/"),
    ("Substack", "https://{}.substack.com/"),
    ("Ghost", "https://{}.ghost.io/"),

    # Design / creative
    ("Behance", "https://www.behance.net/{}"),
    ("Dribbble", "https://dribbble.com/{}"),
    ("DeviantArt", "https://www.deviantart.com/{}"),
    ("ArtStation", "https://www.artstation.com/{}"),
    ("Flickr", "https://www.flickr.com/people/{}"),

    # Gaming
    ("Steam", "https://steamcommunity.com/id/{}"),
    ("Chess.com", "https://www.chess.com/member/{}"),
    ("Lichess", "https://lichess.org/@/{}"),
    ("Speedrun", "https://www.speedrun.com/users/{}"),

    # Knowledge / identity
    ("Keybase", "https://keybase.io/{}"),
    ("Gravatar", "https://gravatar.com/{}"),
]


def username_check():
    section("USERNAME PRESENCE CHECK")

    username = input(
        "  Username: "
    ).strip().lstrip("@")

    if not username:
        return

    if not requests:
        print(
            c(
                "  Install requests first.",
                RED
            )
        )
        pause()
        return

    print(
        c(
            "  Checking public profile URLs only...",
            CYAN
        )
    )

    def check(item):
        name, url = item

        try:
            r = requests.get(
                url.format(quote(username)),
                timeout=5,
                allow_redirects=True,
                headers={
                    "User-Agent": "ARG-Recon-X/3.0"
                }
            )

            exists = r.status_code == 200

            return (
                name,
                r.status_code,
                r.url,
                exists
            )

        except Exception:
            return (
                name,
                None,
                url.format(quote(username)),
                False
            )

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=8
    ) as ex:

        for name, status, url, exists in ex.map(
            check,
            PLATFORMS
        ):

            if exists:
                print(
                    f"  {c('[FOUND]', GREEN)} "
                    f"{name:12} {url}"
                )
            else:
                print(
                    f"  {c('[----]', GRAY)} "
                    f"{name:12} "
                    f"status={status or 'timeout'}"
                )

    print(
        c(
            "\n  Results indicate URL accessibility, "
            "not proof of identity or account ownership.",
            YELLOW
        )
    )

    pause()


# ------------------------- PHONE -------------------------

def phone_info():
    section("PHONE NUMBER METADATA")

    raw = input(
        "  Number with country code (example +91XXXXXXXXXX): "
    ).strip()

    if not raw:
        return

    if phonenumbers is None:
        print(
            c(
                "  Missing dependency: pip install phonenumbers",
                RED
            )
        )
        pause()
        return

    try:
        number = phonenumbers.parse(
            raw,
            None
        )

        valid = phonenumbers.is_valid_number(number)
        possible = phonenumbers.is_possible_number(number)

        print_kv(
            "International",
            phonenumbers.format_number(
                number,
                phonenumbers.PhoneNumberFormat.INTERNATIONAL
            )
        )

        print_kv(
            "E.164",
            phonenumbers.format_number(
                number,
                phonenumbers.PhoneNumberFormat.E164
            )
        )

        print_kv(
            "Country code",
            number.country_code
        )

        print_kv(
            "Valid format",
            valid,
            GREEN if valid else RED
        )

        print_kv(
            "Possible",
            possible,
            GREEN if possible else YELLOW
        )

        print_kv(
            "Region",
            geocoder.description_for_number(
                number,
                "en"
            ) or "Unknown"
        )

        print_kv(
            "Carrier",
            carrier.name_for_number(
                number,
                "en"
            ) or "Unknown"
        )

        tz = timezone.time_zones_for_number(number)

        print_kv(
            "Time zones",
            ", ".join(tz) if tz else "Unknown"
        )

        print_kv(
            "Type",
            str(
                phonenumbers.number_type(number)
            ).split(".")[-1]
        )

    except Exception as e:
        print(
            c(
                f"  Parse error: {e}",
                RED
            )
        )

    print(
        c(
            "\n  This module returns public numbering metadata; "
            "it does not reveal private subscriber identity, "
            "live location, or messages.",
            YELLOW
        )
    )

    pause()


# ------------------------- SYSTEM -------------------------

def about():
    section("MODULE STATUS")

    modules = [
        ("Domain / RDAP", True),
        ("DNS records", True),
        ("TCP scanner", True),
        ("Subdomain resolver", True),
        ("IP metadata", requests is not None),
        ("Username presence", requests is not None),
        ("Phone metadata", phonenumbers is not None),
        ("DNS advanced", _dns_available()),
    ]

    for name, ok in modules:
        status = "ONLINE" if ok else "MISSING"
        color = GREEN if ok else RED

        print(
            f"  {c(status.ljust(20), color)} {name}"
        )

    end_section()

    print(
        c(
            "\n  OSINT-X is a public-information / network-audit console.",
            CYAN
        )
    )

    print(
        c(
            "  It intentionally does not perform credential attacks, "
            "private-data lookup, or",
            GRAY
        )
    )

    print(
        c(
            "  unauthorized access.",
            GRAY
        )
    )

    pause()


# ------------------------- MAIN MENU -------------------------

def main_menu():

    while True:

        banner()

        print(
            c(
                "  ┌──────────────────── COMMAND MATRIX ────────────────────┐",
                BLUE
            )
        )

        options = [
            ("01", "DOMAIN", "Domain / RDAP / DNS information"),
            ("02", "PORTSCAN", "Authorized TCP port scanning"),
            ("03", "SUBDOMAIN", "Passive DNS-style wordlist enumeration"),
            ("04", "PHONE", "Phone-number metadata"),
            ("05", "USERNAME", "Public username presence check"),
            ("06", "IPINFO", "IP / ASN / ISP / geo metadata"),
            ("07", "STATUS", "Module and dependency status"),
            ("00", "EXIT", "Close console"),
        ]

        for n, name, desc in options:
            print(
                f"  {c(n, MAGENTA)}  "
                f"{c(name.ljust(12), WHITE)} "
                f"{c('» ' + desc, GRAY)}"
            )

        print(
            c(
                "  └─────────────────────────────────────────────────────────┘",
                BLUE
            )
        )

        choice = input(
            c("\n  OSINT-X > ", GREEN)
        ).strip().lower()

        if choice in ("1", "01", "domain"):
            domain_info()

        elif choice in ("2", "02", "portscan", "port"):
            port_scan()

        elif choice in ("3", "03", "subdomain", "sub"):
            subdomain_enum()

        elif choice in ("4", "04", "phone"):
            phone_info()

        elif choice in ("5", "05", "username", "user"):
            username_check()

        elif choice in ("6", "06", "ip", "ipinfo"):
            ip_info()

        elif choice in ("7", "07", "status", "about"):
            about()

        elif choice in ("0", "00", "exit", "quit"):
            clear()

            print(
                c(
                    "\n  [ OSINT-X ] Console terminated.",
                    CYAN
                )
            )

            print(
                c(
                    "  Coded by ARGCYBERSKILLHUB\n",
                    GRAY
                )
            )

            break

        else:
            print(
                c(
                    "  Unknown command. Select a number from the matrix.",
                    RED
                )
            )

            time.sleep(0.7)


# ------------------------- ENTRY POINT -------------------------

if __name__ == "__main__":
    try:
        startup_animation()
        main_menu()

    except KeyboardInterrupt:
        clear()

        print(
            c(
                "\n  [CTRL+C] Console terminated.\n",
                YELLOW
            )
        )
def banner():
    clear()

    # ... banner print code ...

    print()
