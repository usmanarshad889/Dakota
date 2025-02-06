import pytest
import json
import os

@pytest.fixture(scope="session")
def config(request):
    """Load environment-specific configuration."""
    env = request.config.getoption("--env")
    config_file_path = os.path.join("config", f"config.{env}.json")

    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

    with open(config_file_path, "r") as config_file:
        config_data = json.load(config_file)

    return config_data

def pytest_addoption(parser):
    """Add command-line option for selecting environment."""
    parser.addoption("--env", action="store", default="sandbox", help="Environment to run tests against (e.g., sandbox, production)")