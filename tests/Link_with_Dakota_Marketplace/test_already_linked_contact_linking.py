import time
import pytest
import allure
from test_utils import skip_broken


from selenium import webdriver
from selenium.webdriver.support.ui import Select
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


@pytest.mark.release_six
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Contact Linking")
@allure.story("Ensure error handling for relinking already linked contacts.")
@pytest.mark.all
@skip_broken
def test_already_linked_contact_linking(driver, config):
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


    # Navigate to Marketplace Search
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")


    # Switch to Contact Tab
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Contacts']")))
    button.click()


    # Wait for page loading
    time.sleep(20)


    # Select Display Criteria
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])[2]")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Linked Contacts")

    time.sleep(10)


    # Click on Search Button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    btn.click()


    # Click on first account name checkbox
    first_box = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[contains(@class,'slds-checkbox_faux')])[2]")))
    first_box.click()


    # Click on linked account
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='MassUploadActions']")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Link Selected Contacts to Existing Contacts")


    # Check the Toast
    message = wait.until(EC.visibility_of_element_located((By.XPATH, "//tr[@class='slds-hint-parent tableTr']")))

    print(f"Message : {message.text.strip()}")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"ScreenShoot", attachment_type=allure.attachment_type.PNG)

    assert message.text.strip() == 'No Contacts Available to Link!' , "Error Occurred ... Testcase Failed"
    time.sleep(2)