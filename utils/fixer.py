import subprocess
import shutil
import os
from datetime import datetime

BACKUP_DIR = "/tmp/garuda_backup"


def ensure_backup_dir():
    if not os.path.exists(BACKUP_DIR):
        os.makedirs(BACKUP_DIR)


def backup_file(path):
    try:
        ensure_backup_dir()

        filename = os.path.basename(path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        backup_path = os.path.join(
            BACKUP_DIR, f"{filename}.{timestamp}.bak"
        )

        shutil.copy2(path, backup_path)

        print(f"[BACKUP] {path} → {backup_path}")

        return backup_path

    except Exception as e:
        print(f"[ERROR] Backup failed: {e}")
        return None


def confirm(action):
    ans = input(f"[FIX] {action}? (y/n): ").lower()
    return ans == "y"


def run_fix(command, description, file_to_backup=None):
    if confirm(description):

        if file_to_backup:
            backup_file(file_to_backup)

        try:
            subprocess.run(command, shell=True, check=True)
            print(f"[FIXED] {description}")
        except Exception as e:
            print(f"[ERROR] Failed to fix: {e}")

    else:
        print(f"[SKIP] {description}")