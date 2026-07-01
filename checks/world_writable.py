import subprocess
from utils.logger import log

def run(config=None):
    print("\n[*] Checking world-writable files...")

    try:
        result = subprocess.run(
            ["find", "/", "-xdev", "-type", "f", "-perm", "-0002"],
            capture_output=True,
            text=True
        )

        files = result.stdout.strip().split("\n")

        if files == [""] or not files:
            log("PASS", "No world-writable files found")
        else:
            log("HIGH", f"World-writable files detected: {files[:5]}")

    except Exception as e:
        log("ERROR", str(e))