import subprocess
from utils.logger import log

def run(config=None):
    print("\n[*] Checking /tmp mount options...")

    try:
        result = subprocess.run(["mount"], capture_output=True, text=True)
        mounts = result.stdout

        if "/tmp" not in mounts:
            log("MEDIUM", "/tmp is not a separate partition")
            return

        if "noexec" in mounts and "nosuid" in mounts:
            log("PASS", "/tmp mounted securely (noexec, nosuid)")
        else:
            log("MEDIUM", "/tmp missing secure mount options")

    except Exception as e:
        log("ERROR", str(e))