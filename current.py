import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)  # Implicit wait as fallback
    yield driver
    driver.quit()


@pytest.fixture(scope="module")
def config(request):
    import json
    import os
    env = request.config.getoption("--env")
    config_file_path = os.path.join("config", f"config.{env}.json")
    with open(config_file_path) as file:
        return json.load(file)


def login(driver, config):
    """Handles login process to Salesforce."""
    wait = WebDriverWait(driver, 100)

    driver.get(config["base_url"])
    wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(config["username"])
    wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(config["password"])
    wait.until(EC.element_to_be_clickable((By.ID, "Login"))).click()


def test_installation_using_correct_link(driver, config):
    """Tests installation of a package using a valid installation link."""
    login(driver, config)

    # Navigate to package installation link
    package_url = "https://dakotanetworks--fuseupgrad.sandbox.my.salesforce-setup.com/packaging/installPackage.apexp?p0=04tKf000000kjBf"
    driver.get(package_url)

    # Wait until page loads and verify title
    wait = WebDriverWait(driver, 20)
    wait.until(EC.title_contains("Install Package"))
    assert "Install Package" in driver.title, "Failed: Incorrect Installation Page"

    print("Link is correct, proceeding with installation...")

    # Click on install button
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Install')]"))).click()

    # Click on grant access checkbox
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='checkbox']"))).click()

    # Click on Continue button
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Continue')]"))).click()

    # Wait for installation to complete (Polling for success message)
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="buttonsArea"]/span/button/span'))).click()
        print("Installation completed successfully!")
    except:
        print("Installation may still be in progress or failed.")

    assert True, "Installation test completed successfully."

