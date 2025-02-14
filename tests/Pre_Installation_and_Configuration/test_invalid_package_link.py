import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@allure.severity(allure.severity_level.MINOR)
@allure.feature("Managed Package Installation")
@allure.story("Verify errors are handled gracefully for incorrect or invalid package links")
def test_invalid_package_link(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()

    # Navigate to the package installation link
    package_url = "https://dakotanetworks--fuseupgrad.sandbox.my.salesforce-setup.com/packaging/installPackage000kjBf"
    driver.get(package_url)
    time.sleep(5)

    # Wait for the page title to load
    wait.until(EC.title_is(driver.title))

    # Assertion with screenshot on failure
    try:
        assert driver.title != "Install Package", "Package installation link is correct, expected it to be incorrect."
    except AssertionError as e:
        allure.attach(driver.get_screenshot_as_png(), name="AssertionFailure", attachment_type=AttachmentType.PNG)
        pytest.fail(str(e))