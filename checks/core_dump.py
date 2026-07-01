from utils.logger import log

def run():
    print("\n[*] Checking core dump restriction...")

    try:
        with open("/etc/security/limits.conf") as f:
            content = f.read()

        if "* hard core 0" in content:
            log("PASS", "Core dumps are restricted")
        else:
            log("MEDIUM", "Core dumps are NOT restricted")

    except FileNotFoundError:
        log("ERROR", "limits.conf not found")

    except Exception as e:
        log("ERROR", str(e))