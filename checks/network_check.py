import subprocess
from utils.logger import log


def run(config=None):
    print("\n[*] Checking network hardening (sysctl)...")

    # default rules (bisa dioverride config nanti)
    default_rules = {
        "net.ipv4.ip_forward": ("0", "HIGH"),
        "net.ipv4.conf.all.accept_redirects": ("0", "HIGH"),
        "net.ipv4.conf.all.send_redirects": ("0", "HIGH"),
        "net.ipv4.conf.all.accept_source_route": ("0", "MEDIUM"),
        "net.ipv4.conf.all.log_martians": ("1", "MEDIUM"),
        "net.ipv4.icmp_echo_ignore_broadcasts": ("1", "PASS")
    }

    # override dari config kalau ada
    rules = config.get("network", default_rules) if config else default_rules

    for param, value in rules.items():
        # handle kalau dari config formatnya beda
        if isinstance(value, tuple):
            expected, severity = value
        else:
            expected = value.get("value")
            severity = value.get("severity", "MEDIUM")

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

            actual = output.split("=")[1].strip()

            if actual == expected:
                log("PASS", f"{param} = {actual}")
            else:
                log(severity, f"{param} = {actual} (expected {expected})")

        except Exception as e:
            log("ERROR", f"{param}: {e}")