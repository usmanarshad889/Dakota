import json
import os
def load_config(env):
    """Load configuration based on the given environment."""
    config_path = os.path.join(os.path.dirname(__file__), f"config.{env}.json")
    with open(config_path, "r") as file:
        configs = json.load(file)

    if env not in configs:
        raise ValueError(f"Environment '{env}' not found in config.sandbox.json!")

    return configs[env]