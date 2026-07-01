import os
from utils.logger import log


def run(config=None):
    print("\n[*] Checking cron configuration...")

    rules = config.get("cron", {}) if config else {}

    allowed_perms = rules.get(
        "allowed_permissions",
        ["600", "640", "700", "750"]
    )

    require_allow = rules.get("require_cron_allow", True)
    check_world = rules.get("check_world_writable", True)

    check_cron_permissions(allowed_perms)
    check_cron_access(require_allow)
    if check_world:
        check_cron_world_writable()


# 🟥 1. cron permissions
def check_cron_permissions(allowed_perms):
    paths = [
        "/etc/crontab",
        "/etc/cron.hourly",
        "/etc/cron.daily",
        "/etc/cron.weekly",
        "/etc/cron.monthly"
    ]

    for path in paths:
        try:
            if not os.path.exists(path):
                continue

            st = os.stat(path)
            perm = oct(st.st_mode)[-3:]

            if perm in allowed_perms:
                log("PASS", f"{path} permission secure ({perm})")
            else:
                log("HIGH", f"{path} permission {perm} (expected {allowed_perms})")

        except Exception as e:
            log("ERROR", f"{path}: {e}")


# 🟥 2. cron allow/deny
def check_cron_access(require_allow):
    try:
        allow_exists = os.path.exists("/etc/cron.allow")
        deny_exists = os.path.exists("/etc/cron.deny")

        if allow_exists:
            log("PASS", "cron.allow is configured")
        elif deny_exists:
            log("MEDIUM", "cron.deny exists (less secure)")
        else:
            if require_allow:
                log("HIGH", "cron.allow missing (no strict access control)")
            else:
                log("MEDIUM", "No cron access control file found")

    except Exception as e:
        log("ERROR", str(e))


# 🟡 3. world writable
def check_cron_world_writable():
    try:
        risky = []

        paths = [
            "/etc/crontab",
            "/etc/cron.d"
        ]

        for path in paths:
            if not os.path.exists(path):
                continue

            st = os.stat(path)
            perm = oct(st.st_mode)[-3:]

            if perm.endswith("2"):
                risky.append(path)

        if risky:
            log("HIGH", f"World-writable cron paths: {risky}")
        else:
            log("PASS", "No world-writable cron files")

    except Exception as e:
        log("ERROR", str(e))