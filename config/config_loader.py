import json
import os

def load_config(env):
    """Load configuration for the given environment from config.json."""
    config_path = os.path.join(os.path.dirname(__file__), "config.json")
    with open(config_path, "r") as file:
        configs = json.load(file)

    if env not in configs:
        raise ValueError(f"Environment '{env}' not found in config.json!")

    return configs[env]