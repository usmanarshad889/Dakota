import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

# Fixture to load the configuration
@pytest.fixture(scope="module")
def config(request):
    import json
    import os
    env = request.config.getoption("--env")
    config_file_path = os.path.join("config", f"config.{env}.json")
    with open(config_file_path) as file:
        return json.load(file)

def test_installation_using_correct_link(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 10)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])

    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])

    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    time.sleep(5)

    # Navigate to correct link of installed package
    driver.get("https://dakotanetworks--fuseupgrad.sandbox.my.salesforce-setup.com/packaging/installPackage.apexp?p0=04tKf000000kjBf")
    time.sleep(15)

    if driver.title == "Install Package":
        print("Link is correct")

        # Click on install button
        driver.find_element(By.XPATH, "/html[1]/body[1]/div[4]/div[1]/div[4]/div[1]/div[2]/span[1]/div[1]/button[1]").click()
        time.sleep(3)

        # Click on grant access
        driver.find_element(By.XPATH, "//input[@class='uiInput uiInputCheckbox uiInput--default uiInput--checkbox']").click()
        time.sleep(1)

        # Click on Continue button
        driver.find_element(By.XPATH, "/html[1]/body[1]/div[3]/div[1]/div[2]/div[1]/div[3]/div[2]/div[1]/button[1]").click()
        time.sleep(100)

        try:
            driver.find_element(By.XPATH, '//*[@id="buttonsArea"]/span/button/span').click()
            time.sleep(5)
        except:
            pass
        assert True
    else:
        print("Install Package Link is not correct")
        driver.quit()
        assert False

