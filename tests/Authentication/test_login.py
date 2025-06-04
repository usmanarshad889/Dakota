import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from test_utils import skip_broken

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.test_demo
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Login - Correct Credentials")
@allure.story("Validate successful login functionality with correct credentials.")
@skip_broken
def test_authentication_correct_credentials(driver, config):


    # Navigate to login page
    driver.get(config["base_url"])
    driver.delete_all_cookies()
    wait = WebDriverWait(driver, 20, poll_frequency=0.5)


    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    time.sleep(2)
    login_button.click()
    time.sleep(3)
