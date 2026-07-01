from utils.logger import log
from utils.fixer import run_fix


def run(config, fix=False):
    print("\n[*] Checking SSH configuration...")

    try:
        with open("/etc/ssh/sshd_config", "r") as f:
            lines = f.readlines()

        conf = {}

        # parse config (ignore comment)
        for line in lines:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) >= 2:
                conf[parts[0]] = parts[1]

        # 🔴 Root login check
        if conf.get("PermitRootLogin", "yes") == "yes":
            log("HIGH", "SSH root login is ENABLED")

            if fix:
                run_fix(
                    "sed -i 's/^PermitRootLogin.*/PermitRootLogin no/' /etc/ssh/sshd_config && systemctl restart ssh",
                    "Disable SSH root login",
                    "/etc/ssh/sshd_config"
                )
        else:
            log("PASS", "SSH root login is disabled")

        # 🟡 Password auth check
        if conf.get("PasswordAuthentication", "yes") == "yes":
            log("MEDIUM", "SSH password authentication is ENABLED")

            if fix:
                run_fix(
                    "sed -i 's/^PasswordAuthentication.*/PasswordAuthentication no/' /etc/ssh/sshd_config && systemctl restart ssh",
                    "Disable SSH password authentication",
                    "/etc/ssh/sshd_config"
                )
        else:
            log("PASS", "SSH password authentication is disabled")

    except FileNotFoundError:
        log("ERROR", "sshd_config not found (SSH may not be installed)")

    except Exception as e:
        log("ERROR", str(e))