import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException
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

@pytest.mark.P1
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Availability - Heroku Site")
@allure.story("Validate the availability of Heroku site")
def test_heroku_site_availability(driver, config):
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

    # Navigate to installed pakages setup
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Setup")

    # Click on Authentication svg button
    try:
        # Wait for full page load
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        element = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[3]"))
        )
        element.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
        pass
    time.sleep(1)

    # Verify the Authentication with correct Credentials
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Username']"))).clear()
    driver.find_element(By.XPATH, "//input[@name='Username']").send_keys("Fuse Upgrade")
    driver.find_element(By.XPATH, "//input[@name='Password']").clear()
    driver.find_element(By.XPATH, "//input[@name='Password']").send_keys("rolus009")
    driver.find_element(By.XPATH, "//input[@name='AuthorizationURL']").clear()
    driver.find_element(By.XPATH, "//input[@name='AuthorizationURL']").send_keys("https://marketplace-dakota-uat.herokuapp.com")

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@value='Connect']"))).click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
        print("Connect button is not clicked in the first attempt")
        pass

    try:
        wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[normalize-space()='Connect'])[1]"))).click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
        print("Connect button clicked successfully in first attempt")
        pass

    time.sleep(2)

    toast = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
    print(f"Toast message : {toast.text}")

    # Verify the Toast message
    assert toast.text.lower() == "dakota marketplace account connected successfully.", f"Test failed: {toast.text}"

    # Attach a screenshot of the final state
    allure.attach(driver.get_screenshot_as_png(), name="Final_State_Screenshot", attachment_type=AttachmentType.PNG)


    # Navigate to contact tab
    driver.get(f"{config["base_url"]}lightning/o/Contact/list?filterName=__Recent")
    all_contact = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/th[1]")))
    print(f"Total Contact Founds : {len(all_contact)}")

    assert len(all_contact) > 0 , f"No Contact Found"
    time.sleep(2)

    # Navigate to account tab
    driver.get(f"{config["base_url"]}lightning/o/Account/list?filterName=__Recent")
    all_account = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/th[1]")))
    print(f"Total Account Founds : {len(all_account)}")

    assert len(all_account) > 0, f"No Account Found"
    time.sleep(2)

    # Navigate to Metro Area
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Metro_Areas")
    all_metro = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/th[1]")))
    print(f"Total Metro Area Founds : {len(all_metro)}")

    assert len(all_metro) > 0, f"No Metro Area Found"
    time.sleep(2)
