from utils.logger import log
import subprocess

def run(config):
    print("\n[*] Checking open ports...")

    try:
        result = subprocess.run(
            ["ss", "-tuln"],
            capture_output=True,
            text=True
        )

        lines = result.stdout.split("\n")

        rules = config.get("ports", {})
        allowed_ports = rules.get("allowed", [])
        dangerous_ports = rules.get("dangerous", {})

        found_ports = set()

        for line in lines:
            parts = line.split()
            if len(parts) < 5:
                continue

            local_address = parts[4]

            if ":" in local_address:
                port = local_address.split(":")[-1]

                if port.isdigit():
                    found_ports.add(port)

        if not found_ports:
            log("PASS", "No open ports detected")
            return

        for port in sorted(found_ports):
            if port in dangerous_ports:
                log("HIGH", f"Port {port} open - {dangerous_ports[port]}")
            elif port in allowed_ports:
                log("INFO", f"Port {port} open (allowed)")
            else:
                log("MEDIUM", f"Port {port} open (not in allowed list)")

    except Exception as e:
        log("ERROR", str(e))