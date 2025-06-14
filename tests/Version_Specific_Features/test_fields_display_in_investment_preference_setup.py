import time
import pytest
import allure
from test_utils import skip_broken , pass_broken

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


@pytest.mark.all
@pytest.mark.release_six
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Marketplace Setup")
@allure.story("Validate the display of the Investment field and its related fields in Marketplace Setup.")
@pass_broken
def test_fields_display_in_investment_preference_setup(driver, config):
    # Navigate to login page of fuse app
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

    toast = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
    print(f"Toast message : {toast.text}")

    # Verify the Toast message
    assert toast.text.lower() == "dakota marketplace account connected successfully.", f"Test failed: {toast.text}"
    time.sleep(3)


    # Click on Mapping SVG
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[2]//article[1]//div[1]//div[1]//div[1]//button[1]//lightning-primitive-icon[1]")))
    element.click()
    time.sleep(1)


    try:
        # Click on Auto Sync Field Updates
        inactive_button = driver.find_element(By.XPATH, "//span[@class='slds-checkbox_off']")
        if inactive_button.text == "Inactive":
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_faux']")))
            btn.click()
        else:
            print("Button is already active")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")


    # Click on Contacts Tab
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Investment Preference']")))

    print(f"Is Investment Preference Field Displayed : {button.is_displayed()}")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Display of Investment Preference Button", attachment_type=allure.attachment_type.PNG)

    assert button.is_displayed() , f"Investment Preference Button is not Present"

    button.click()
    time.sleep(1)

    # Scroll down by 400 pixels
    driver.execute_script("window.scrollBy(0, 400);")


    # Wait for page to fully load
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[@title='Platform Details']")))
    time.sleep(1)


    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Investment Preference Fields ", attachment_type=allure.attachment_type.PNG)


    # Expected fields
    expected_fields = [
        'Platform Details',
        'Investment Structures',
        'Consultants',
        'Equities',
        'Fixed Income',
        'Alternatives',
        'Additional Webpages'
    ]

    # Locate all present fields
    all_present_fields = driver.find_elements(By.XPATH, "//span[@class='slds-accordion__summary-content']")

    # Extract text from the located elements
    actual_fields = [field.text.strip() for field in all_present_fields]

    print(f"Actual Displayed fields : {actual_fields}")

    # Assertion to check if all expected fields are present
    assert set(expected_fields).issubset(
        set(actual_fields)), f"Missing fields: {set(expected_fields) - set(actual_fields)}"

