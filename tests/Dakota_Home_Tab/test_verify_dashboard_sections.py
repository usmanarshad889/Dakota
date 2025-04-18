import time
import pytest
import allure
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
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
@pytest.mark.release_two
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Salesforce Dashboard Verification")
@allure.story('''Verify display of Job Changes, Role Changes, Fundraising News, 
Dakota Videos, Member Comments, and New Investments/Accounts/Contacts''')
def test_verify_dashboard_sections(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    driver.delete_all_cookies()
    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        time.sleep(2)
        login_button.click()
        time.sleep(3)

        # Wait for URL change
        wait.until(EC.url_contains("lightning.force.com"))

        # Verify Login
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]"))).click()

    except Exception as e:
        pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
        driver.quit()


    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)

    # Navigate to Dakota Home Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Home")

    # Wait for records display
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "(//td[@data-label='Last Updated Date'])[1]")))
        time.sleep(1)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")

    # Scroll down the element
    scroll_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='title-div'][normalize-space()='Dakota Videos']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start', inline: 'nearest'});",scroll_element)
    time.sleep(1)

    # Screenshot & Allure attachment
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Dakota Home Page", attachment_type=allure.attachment_type.PNG)

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
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Message: {type(e).__name__}")
            print(f"{name} ❌ Not Found")
            all_elements_present = False

    assert all_elements_present, "❌ One or more required sections are missing!"
