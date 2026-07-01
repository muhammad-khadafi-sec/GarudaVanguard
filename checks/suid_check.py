import subprocess
from utils.logger import log

def run(config=None):
    print("\n[*] Checking SUID files...")

    try:
        result = subprocess.run(
            ["find", "/", "-xdev", "-perm", "-4000"],
            capture_output=True,
            text=True
        )

        files = result.stdout.strip().split("\n")

        if files == [""] or not files:
            log("PASS", "No SUID files found")
            return

        total = len(files)

        # bisa nanti dimasukin ke config
        dangerous = ["bash", "sh", "dash"]

        found_dangerous = []

        for f in files:
            for d in dangerous:
                if f.endswith(d):
                    found_dangerous.append(f)

        if found_dangerous:
            log("HIGH", f"Dangerous SUID binaries: {found_dangerous[:3]}")

        if total > 50:
            log("MEDIUM", f"High number of SUID files: {total}")
        else:
            log("INFO", f"SUID files count: {total}")

    except Exception as e:
        log("ERROR", str(e))