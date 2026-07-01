import subprocess
from utils.logger import log
from utils.fixer import run_fix


def run(fix=False):
    print("\n[*] Checking firewall status (UFW)...")

    try:
        result = subprocess.run(
            ["ufw", "status"],
            capture_output=True,
            text=True
        )

        output = result.stdout.strip()

        if not output:
            log("ERROR", "No output from UFW command")
            return

        if "Status: inactive" in output:
            log("HIGH", "UFW is DISABLED")

            if fix:
                run_fix(
                    "ufw enable",
                    "Enable UFW firewall"
                )

        elif "Status: active" in output:
            lines = output.split("\n")

            if len(lines) <= 1:
                log("MEDIUM", "UFW active but NO rules configured")
            else:
                log("PASS", "UFW active with rules configured")

        else:
            log("ERROR", "Unable to determine UFW status")

    except FileNotFoundError:
        log("ERROR", "UFW is not installed")

    except Exception as e:
        log("ERROR", str(e))