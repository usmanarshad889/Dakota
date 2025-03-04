import json
import os

def load_config(env):
    """Load configuration for the given environment from config.json."""
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "config.json"))

    try:
        with open(config_path, "r") as file:
            configs = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Configuration file not found: {config_path}")
    except json.JSONDecodeError:
        raise ValueError(f"Invalid JSON format in config file: {config_path}")

    if env not in configs:
        raise ValueError(f"Environment '{env}' not found in config.json!")

    return configs[env]
