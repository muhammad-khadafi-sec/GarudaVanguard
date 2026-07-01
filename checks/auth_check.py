import os
from utils.logger import log


def run(config=None):
    print("\n[*] Checking authentication & account security...")

    check_uid_0()
    check_empty_password()
    check_login_defs(config)


# 🟥 1. UID 0 check
def check_uid_0():
    try:
        with open("/etc/passwd") as f:
            lines = f.readlines()

        uid0_users = []

        for line in lines:
            parts = line.split(":")
            if len(parts) > 2 and parts[2] == "0":
                uid0_users.append(parts[0])

        if len(uid0_users) == 1 and uid0_users[0] == "root":
            log("PASS", "Only root has UID 0")
        else:
            log("HIGH", f"Multiple UID 0 users detected: {uid0_users}")

    except Exception as e:
        log("ERROR", str(e))


# 🟥 2. Empty password check
def check_empty_password():
    try:
        with open("/etc/shadow") as f:
            lines = f.readlines()

        empty_users = []

        for line in lines:
            parts = line.split(":")
            if len(parts) > 1:
                password_field = parts[1]

                # kosong atau tanpa hash
                if password_field == "" or password_field == "!" or password_field == "*":
                    continue

                # edge case: truly empty
                if password_field.strip() == "":
                    empty_users.append(parts[0])

        if empty_users:
            log("HIGH", f"Users with empty password: {empty_users}")
        else:
            log("PASS", "No empty password users")

    except PermissionError:
        log("ERROR", "Permission denied reading /etc/shadow (run as root)")
    except Exception as e:
        log("ERROR", str(e))


# 🟡 3. login.defs policy
def check_login_defs(config):
    try:
        with open("/etc/login.defs") as f:
            lines = f.readlines()

        rules = config.get("auth", {}) if config else {}

        expected_max = int(rules.get("pass_max_days", 365))
        expected_min = int(rules.get("pass_min_days", 1))
        expected_warn = int(rules.get("pass_warn_age", 7))
        expected_hash = rules.get("hashing", "SHA512")

        values = {}

        for line in lines:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()
            if len(parts) >= 2:
                values[parts[0]] = parts[1]

        # 🔍 PASS_MAX_DAYS
        max_days = int(values.get("PASS_MAX_DAYS", 99999))
        if max_days <= expected_max:
            log("PASS", f"PASS_MAX_DAYS = {max_days}")
        else:
            log("MEDIUM", f"PASS_MAX_DAYS = {max_days} (expected ≤ {expected_max})")

        # 🔍 PASS_MIN_DAYS
        min_days = int(values.get("PASS_MIN_DAYS", 0))
        if min_days >= expected_min:
            log("PASS", f"PASS_MIN_DAYS = {min_days}")
        else:
            log("MEDIUM", f"PASS_MIN_DAYS = {min_days} (expected ≥ {expected_min})")

        # 🔍 PASS_WARN_AGE
        warn_days = int(values.get("PASS_WARN_AGE", 0))
        if warn_days >= expected_warn:
            log("PASS", f"PASS_WARN_AGE = {warn_days}")
        else:
            log("MEDIUM", f"PASS_WARN_AGE = {warn_days} (expected ≥ {expected_warn})")

        # 🔐 HASHING METHOD
        hash_method = values.get("ENCRYPT_METHOD", "UNKNOWN")
        if hash_method.upper() == expected_hash.upper():
            log("PASS", f"Password hashing uses {hash_method}")
        else:
            log("MEDIUM", f"Hashing = {hash_method} (expected {expected_hash})")

    except Exception as e:
        log("ERROR", str(e))