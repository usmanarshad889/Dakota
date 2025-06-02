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
    yield driver
    driver.quit()


@pytest.mark.release_seven
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Contact Linking")
@allure.story('Ensure the "Dakota Contact CRD" field is available for linking contacts.')
def test_crd_field_display_for_linking_contact(driver, config):
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


    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Select the Contacts tab and print its text
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Contacts']")))
    print(f"Current Tab : {tab.text}")
    tab.click()

    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])[2]")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Unlinked Contacts")
    time.sleep(20)


    # Click the Search button and print its text
    search_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")
    ))
    search_button.click()

    # Click on ALL CHECKBOX
    all_box = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[contains(@class,'slds-checkbox_faux')])[2]")))
    all_box.click()

    # Click on linked account
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='MassUploadActions']")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Link Selected Contacts to Existing Contacts")
    time.sleep(5)

    # Click on linked account
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@class='slds-select'])[6]")))
    time.sleep(1)
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Dakota CRD#")

    try:
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@class='slds-select'])[7]")))
        dropdown_option = Select(dropdown)
        dropdown_option.select_by_visible_text("CRD #")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'slds-button slds-button_neutral slds-button slds-button--brand')][normalize-space()='Search']"))).click()
    time.sleep(8)


    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Display of CRD#", attachment_type=allure.attachment_type.PNG)


    # Click on linked contacts
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Link Contacts']")))
    btn.click()

    time.sleep(2)

    toast_message = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    print(f"Actual Toast Text : {toast_message.text}")

    valid_messages = [
        "Contact(s) linking is in progress.",
        "No contact to link."
    ]

    toast_text = toast_message.text.strip()
    assert toast_text in valid_messages, f"Unexpected Toast Message: {toast_text}"
    time.sleep(2)