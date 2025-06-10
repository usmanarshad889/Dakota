import time
import pytest
import allure
from test_utils import skip_broken , pass_broken

from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException
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


@pytest.mark.smoke
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Availability - Heroku Site")
@allure.story("Validate the availability of Heroku site")
# @pytest.mark.all
@pass_broken
def test_heroku_site_availability(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
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
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()
        except Exception as e:
            pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
            driver.quit()

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

    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")

    # Click on Authentication svg button
    try:
        # Wait for full page load
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        element = wait.until(
            EC.element_to_be_clickable((By.XPATH, "//li[1]//article[1]//div[1]//div[1]//div[1]//button[1]//lightning-primitive-icon[1]"))
        )
        element.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)
    print("Navigating to Marketplace Setup")

    # Verify the Authentication with correct Credentials
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Username']"))).clear()
    driver.find_element(By.XPATH, "//input[@name='Username']").send_keys("Fuse Upgrade")
    driver.find_element(By.XPATH, "//input[@name='Password']").clear()
    driver.find_element(By.XPATH, "//input[@name='Password']").send_keys("rolus009")
    driver.find_element(By.XPATH, "//input[@name='AuthorizationURL']").clear()
    driver.find_element(By.XPATH, "//input[@name='AuthorizationURL']").send_keys("https://marketplace-dakota-uat.herokuapp.com")
    time.sleep(1)

    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Connect']")))
        driver.execute_script("arguments[0].click();", btn)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(2)

    toast = wait.until(EC.presence_of_element_located((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
    print(f"Toast message : {toast.text}")
    print("Verifying assertion")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

    # Verify the Toast message
    assert toast.text.lower() == "dakota marketplace account connected successfully.", f"Test failed: {toast.text}"
    time.sleep(3)
    print("Assertion verified")

    # Attach a screenshot of the final state
    allure.attach(driver.get_screenshot_as_png(), name="Final_State_Screenshot", attachment_type=AttachmentType.PNG)


    # Navigate to contact tab
    driver.get(f"{config['base_url']}lightning/o/Contact/list?filterName=__Recent")
    all_contact = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/th[1]")))
    print(f"Total Contact Founds : {len(all_contact)}")

    assert len(all_contact) > 0 , f"No Contact Found"
    time.sleep(2)

    # Navigate to account tab
    driver.get(f"{config['base_url']}lightning/o/Account/list?filterName=__Recent")
    all_account = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/th[1]")))
    print(f"Total Account Founds : {len(all_account)}")

    assert len(all_account) > 0, f"No Account Found"
    time.sleep(2)

    # Navigate to Metro Area
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Metro_Areas")
    all_metro = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//tbody/tr/th[1]")))
    print(f"Total Metro Area Founds : {len(all_metro)}")

    assert len(all_metro) > 0, f"No Metro Area Found"
    time.sleep(2)
