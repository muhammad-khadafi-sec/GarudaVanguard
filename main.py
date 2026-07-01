#!/usr/bin/env python3

import argparse
import time
import textwrap

from checks import ssh_check
from checks import firewall_check
from checks import port_check
from checks import file_permissions
from checks import world_writable
from checks import suid_check
from checks import kernel_check
from checks import core_dump
from checks import tmp_check
from checks import auth_check
from checks import network_check
from checks import service_check
from checks import cron_check

from utils.logger import summary, export_json
from utils.config import load_config


# =========================
# 🎨 BANNER
# =========================
def show_banner():
    banner = textwrap.dedent(r"""
         _________    ____  __  ______  ___        
        / ____/   |  / __ \/ / / / __ \/   |       
       / / __/ /| | / /_/ / / / / / / / /| |       
      / /_/ / ___ |/ _, _/ /_/ / /_/ / ___ |       
 _    \____/_/ _|_/_/_|_|\____/_____/_/ _|_|  ____ 
| |  / /   |  / | / / ____/ / / /   |  / __ \/ __ \
| | / / /| | /  |/ / / __/ / / / /| | / /_/ / / / /
| |/ / ___ |/ /|  / /_/ / /_/ / ___ |/ _, _/ /_/ / 
|___/_/  |_/_/ |_/\____/\____/_/  |_/_/ |_/_____/                                                    

            SECURITY HARDENING CHECKER
""")

    print("\033[96m" + banner + "\033[0m")
    print("\033[93mSecurity Hardening Tools\033[0m")
    print("\033[90mby Muhammad Khadafi\033[0m\n")


# =========================
# 🚀 RUN CHECKS
# =========================
def run_checks(config, fix=False):
    checks = [
        ("SSH", lambda: ssh_check.run(config, fix)),
        ("Auth", lambda: auth_check.run(config)),
        ("Firewall", lambda: firewall_check.run(fix)),
        ("Ports", lambda: port_check.run(config)),
        ("File Permissions", lambda: file_permissions.run(config, fix)),
        ("World Writable", lambda: world_writable.run()),
        ("SUID", lambda: suid_check.run()),
        ("Kernel", lambda: kernel_check.run(config)),
        ("Network", lambda: network_check.run(config)),
        ("Services", lambda: service_check.run(config)),
        ("Core Dump", lambda: core_dump.run()),
        ("/tmp", lambda: tmp_check.run()),
        ("Cron", lambda: cron_check.run(config)),
    ]

    total = len(checks)

    for i, (name, func) in enumerate(checks, start=1):
        print(f"\n[{i}/{total}] Running {name} Check...")
        func()

    print("\n[INFO] Use --fix to attempt automatic remediation\n")


# =========================
# 🎯 SCAN COMMAND
# =========================
def cmd_scan(args):
    show_banner()

    config = load_config()

    start = time.time()

    run_checks(config, fix=args.fix)

    summary()

    if args.json:
        export_json(args.json)

    end = time.time()
    print(f"\nScan completed in {round(end - start, 2)} seconds\n")


# =========================
# 🧠 CLI
# =========================
def main():
    parser = argparse.ArgumentParser(
        prog="garuda",
        description="Garuda Vanguard - Security Hardening Toolkit"
    )

    subparsers = parser.add_subparsers(dest="command")

    scan_parser = subparsers.add_parser("scan", help="Run security scan")
    scan_parser.add_argument("--json", metavar="FILE", help="Export JSON report")
    scan_parser.add_argument("--fix", action="store_true", help="Auto fix issues")
    scan_parser.set_defaults(func=cmd_scan)

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    args.func(args)


if __name__ == "__main__":
    main()