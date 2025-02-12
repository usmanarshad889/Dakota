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
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()


@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Salesforce Dashboard Verification")
@allure.story('''Verify display of Job Changes, Role Changes, Fundraising News, 
Dakota Videos, Member Comments, and New Investments/Accounts/Contacts''')
def test_verify_dashboard_sections(driver, config):
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

    # Navigate to Dakota Home Page
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Home")

    # Scroll down the element
    scroll_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='title-div'][normalize-space()='Dakota Videos']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'});",scroll_element)
    time.sleep(1)

    elements_to_check = {
        "Job Changes": "(//a[@class='slds-tabs_default__link'])[1]",
        "Role Changes": "(//a[@class='slds-tabs_default__link'])[2]",
        "Fundraising News": "//span[normalize-space()='Fundraising News']",
        "Dakota Videos": "//span[@class='title-div'][normalize-space()='Dakota Videos']",
        "Ask Dakota": "//span[@class='title-div'][normalize-space()='Ask Dakota']",
        "New Public Investments": "(//a[@class='slds-tabs_default__link'])[3]",
        "New 13F Fillings": "(//a[@class='slds-tabs_default__link'])[4]",
        "New New Accounts": "(//a[@class='slds-tabs_default__link'])[5]",
        "New New Contacts": "(//a[@class='slds-tabs_default__link'])[6]",
    }

    all_elements_present = True
    for name, xpath in elements_to_check.items():
        try:
            wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
            print(f"{name} ✅ Found")
        except:
            print(f"{name} ❌ Not Found")
            all_elements_present = False

    screenshot_path = "salesforce_dashboard_check.png"
    driver.save_screenshot(screenshot_path)
    print(f"Screenshot saved to {screenshot_path}")

    assert all_elements_present, "❌ One or more required sections are missing!"
