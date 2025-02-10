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

def test_installation_users_list(driver, config):
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
    time.sleep(5)

    # Navigate to correct link of installed package
    driver.get("https://dakotanetworks--fuseupgrad.sandbox.my.salesforce-setup.com/packaging/installPackage.apexp?p0=04tKf000000kjBf")
    time.sleep(15)

    if driver.title == "Install Package":
        print("Link is correct")
    else:
        print("Link is not correct and unable to test the testcase")
        assert False

    #  Copy All users text
    admin_user = driver.find_element(By.XPATH, "//div[contains(text(),'Install for Admins Only')]")
    all_user = driver.find_element(By.XPATH, "//div[contains(text(),'Install for All Users')]")
    specific_user = driver.find_element(By.XPATH, "//div[contains(text(),'Install for Specific Profiles...')]")

    # Verify users
    if admin_user.text.lower() == "install for admins only" and all_user.text.lower() == "install for all users" and specific_user.text.lower() == "install for specific profiles...":
        print("Package can be install for following users ...\n")
        print(f"1. {admin_user.text}")
        print(f"2. {all_user.text}")
        print(f"3. {specific_user.text}")
        assert True

    else:
        print("Test Case Fail")
        assert False

    driver.quit()