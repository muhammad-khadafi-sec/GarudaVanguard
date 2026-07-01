import subprocess
from utils.logger import log

def run(config):
    print("\n[*] Checking kernel security parameters...")

    rules = config.get("kernel", {})

    for param, expected in rules.items():
        try:
            result = subprocess.run(
                ["sysctl", param],
                capture_output=True,
                text=True
            )

            output = result.stdout.strip()

            if "=" not in output:
                log("ERROR", f"Failed to read {param}")
                continue

            value = output.split("=")[1].strip()

            if value == expected:
                log("PASS", f"{param} = {value}")
            else:
                log("HIGH", f"{param} = {value} (expected {expected})")

        except Exception as e:
            log("ERROR", f"{param}: {e}")