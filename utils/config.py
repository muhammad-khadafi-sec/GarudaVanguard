import os
import json

def load_config():
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))

        # naik ke root project kalau file ini di utils/
        project_root = os.path.dirname(base_dir)

        config_path = os.path.join(project_root, "config", "rules.json")

        print(f"[DEBUG] Loading config from: {config_path}")

        with open(config_path) as f:
            return json.load(f)

    except Exception as e:
        print(f"[ERROR] Failed to load config: {e}")
        return {}