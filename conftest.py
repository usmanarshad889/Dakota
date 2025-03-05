import pytest
import json
import os

@pytest.fixture(scope="session")
def config(request):
    """Load environment-specific configuration from config.json."""
    env = request.config.getoption("--env")
    config_file_path = os.path.join(os.path.dirname(__file__), "config", "config.json")

    if not os.path.exists(config_file_path):
        raise FileNotFoundError(f"Configuration file not found: {config_file_path}")

    with open(config_file_path, "r") as config_file:
        config_data = json.load(config_file)

    if env not in config_data:
        raise ValueError(f"Environment '{env}' not found in config.json!")

    return config_data[env]

def pytest_addoption(parser):
    """Add command-line option for selecting environment."""
    parser.addoption("--env", action="store", default="sandbox", help="Environment to run tests against (e.g., sandbox, production)")

# def pytest_addoption(parser):
#     """Add command-line options for pytest."""
#     if not any(opt.dest == "env" for opt in parser._anonymous.options):
#         parser.addoption(
#             "--env", action="store", default="sandbox",
#             help="Environment to run tests against (e.g., sandbox, production)"
#         )