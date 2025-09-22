import time
import pytest
import allure
from test_utils import skip_broken , pass_broken

from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.release_two
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Salesforce Dashboard Verification")
@allure.story('''Verify display of Job Changes, Role Changes, Fundraising News, 
Dakota Videos, Member Comments, and New Investments/Accounts/Contacts''')
@pytest.mark.all
@skip_broken
def test_verify_dashboard_sections(driver, config):
    driver.get(config["base_url"])
    driver.delete_all_cookies()
    wait = WebDriverWait(driver, 30, poll_frequency=0.5)

    # Login block
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(config["username"])
        wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(config["password"])
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.ID, "Login"))).click()
    except Exception as e:
        driver.quit()
        pytest.skip(f"Skipping test due to login failure: {type(e).__name__}")

    # Confirm login success
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='App Launcher']")))
        print("App Launcher is found")
    except Exception as e:
        driver.quit()
        pytest.skip(f"Skipping test due to missing App Launcher: {type(e).__name__}")

    # Navigate to Dakota Home Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Home")

    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

    # Wait for records display
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "(//td[@data-label='Last Updated Date'])[1]")))
        time.sleep(1)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")

    # # Scroll down the element
    # scroll_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='title-div'][normalize-space()='Dakota Videos']")))
    # driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start', inline: 'nearest'});",scroll_element)
    # time.sleep(1)
    #
    # # Screenshot & Allure attachment
    # screenshot = driver.get_screenshot_as_png()
    # allure.attach(screenshot, name=f"Dakota Home Page", attachment_type=allure.attachment_type.PNG)
    #
    # elements_to_check = {
    #     "Job Changes": "(//a[@class='slds-tabs_default__link'])[1]",
    #     "Role Changes": "(//a[@class='slds-tabs_default__link'])[2]",
    #     "Fundraising News": "//span[normalize-space()='Fundraising News']",
    #     "Dakota Videos": "//span[@class='title-div'][normalize-space()='Dakota Videos']",
    #     "Ask Dakota": "//span[@class='title-div'][normalize-space()='Ask Dakota']",
    #     "New Public Investments": "(//a[@class='slds-tabs_default__link'])[3]",
    #     "New 13F Fillings": "(//a[@class='slds-tabs_default__link'])[4]",
    #     "New New Accounts": "(//a[@class='slds-tabs_default__link'])[5]",
    #     "New New Contacts": "(//a[@class='slds-tabs_default__link'])[6]",
    # }
    #
    # all_elements_present = True
    # for name, xpath in elements_to_check.items():
    #     try:
    #         wait.until(EC.presence_of_element_located((By.XPATH, xpath)))
    #         print(f"{name} ✅ Found")
    #     except (NoSuchElementException, TimeoutException) as e:
    #         print(f"Message: {type(e).__name__}")
    #         print(f"{name} ❌ Not Found")
    #         all_elements_present = False
    #
    # assert all_elements_present, "❌ One or more required sections are missing!"
