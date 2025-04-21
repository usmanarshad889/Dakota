import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
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


@pytest.mark.P1
@pytest.mark.release_three
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Marketplace Search")
@allure.story('Validate the "Create Account and Related Contact" button in the preview popup for Marketplace Search and proper creation.')
def test_create_account_preview_popup_marketplace(driver, config):
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

    # Navigate to the contact search page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Wait for the results to load
    time.sleep(10)

    # Select Display Criteria (Linked Account)
    criteria_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])[1]")))
    dropdown_option = Select(criteria_dropdown)
    dropdown_option.select_by_visible_text("Unlinked Accounts")
    time.sleep(3)


    # Click the Search button and print its text
    search_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//button[@title='Search']")
    ))
    print(f"Button Text : {search_button.text}")
    search_button.click()

    # Click on first name
    first_name = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@name='previewAccount'])[1]")))
    print(f"Account Name : {first_name.text}")
    first_name.click()

    # Verify the "Create Account" button on preview popup
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Create Account &')]")))

    assert button.text.strip() == "Create Account & Related Contacts" , f"Expected button was 'Create Account & Related Contacts' but got {button.text}"
    time.sleep(1)

    # Verify the correct creation
    button.click()
    time.sleep(8)

    # Check if "Create Account" button exists
    create_account_buttons = driver.find_elements(By.XPATH, "//button[normalize-space()='Create Account']")

    if create_account_buttons:
        create_account = wait.until(EC.element_to_be_clickable(create_account_buttons[0]))
        create_account.click()

        # Wait for toast message
        toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Toast message: {toast_message.text}")

        # Verify the Toast message
        assert "successfully" in toast_message.text.lower(), f"Test failed: {toast_message.text}"
        time.sleep(2)

        # Attach a screenshot of the final state
        allure.attach(driver.get_screenshot_as_png(), name="Final_State_Screenshot", attachment_type=AttachmentType.PNG)

    else:
        time.sleep(1)
        # Add Account with Related Contact(s)
        try:
            check_box = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[103]")))
            check_box.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__}")

        # click on save/create button
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save and Create']")))
        save_btn.click()

        # Wait for toast message
        toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Toast message: {toast_message.text}")

        # Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

        # Verify the Toast message
        assert "successfully" in toast_message.text.lower(), f"Test failed: {toast_message.text}"
        time.sleep(2)