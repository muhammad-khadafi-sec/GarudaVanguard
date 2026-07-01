import subprocess
from utils.logger import log


def run(config=None):
    print("\n[*] Checking running services...")

    try:
        result = subprocess.run(
            ["systemctl", "list-units", "--type=service", "--state=running"],
            capture_output=True,
            text=True
        )

        lines = result.stdout.split("\n")

        services = []

        for line in lines:
            parts = line.split()
            if len(parts) > 0 and ".service" in parts[0]:
                services.append(parts[0].replace(".service", ""))

        if not services:
            log("ERROR", "Unable to detect running services")
            return

        # 🔥 default rules (bisa override config)
        default_rules = {
            "dangerous": ["telnet", "rsh", "rexec"],
            "unnecessary": ["avahi-daemon", "cups", "bluetooth", "rpcbind"]
        }

        rules = config.get("services", default_rules) if config else default_rules

        dangerous = rules.get("dangerous", [])
        unnecessary = rules.get("unnecessary", [])

        found_dangerous = []
        found_unnecessary = []

        for svc in services:
            for d in dangerous:
                if d in svc:
                    found_dangerous.append(svc)

            for u in unnecessary:
                if u in svc:
                    found_unnecessary.append(svc)

        # 🔴 dangerous services
        if found_dangerous:
            log("HIGH", f"Dangerous services running: {found_dangerous}")
        else:
            log("PASS", "No dangerous services detected")

        # 🟡 unnecessary services
        if found_unnecessary:
            log("MEDIUM", f"Unnecessary services running: {found_unnecessary}")
        else:
            log("PASS", "No unnecessary services detected")

        # 🟢 info total
        log("INFO", f"Total running services: {len(services)}")

    except FileNotFoundError:
        log("ERROR", "systemctl not available")

    except Exception as e:
        log("ERROR", str(e))