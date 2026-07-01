import os
from utils.logger import log
from utils.fixer import run_fix


def run(config, fix=False):
    print("\n[*] Checking critical file permissions...")

    passwd_expected = config.get("filesystem", {}).get("passwd_permission", "644")
    shadow_expected = config.get("filesystem", {}).get("shadow_permission", "640")

    def check(path, expected):
        try:
            st = os.stat(path)
            actual = oct(st.st_mode)[-3:]

            if actual == expected:
                log("PASS", f"{path} permission secure ({actual})")
            else:
                log("HIGH", f"{path} permission {actual} (expected {expected})")

                if fix:
                    run_fix(
                        f"chmod {expected} {path}",
                        f"Fix permission for {path}",
                        path
                    )

        except FileNotFoundError:
            log("ERROR", f"{path} not found")

        except Exception as e:
            log("ERROR", f"{path}: {e}")

    check("/etc/passwd", passwd_expected)
    check("/etc/shadow", shadow_expected)