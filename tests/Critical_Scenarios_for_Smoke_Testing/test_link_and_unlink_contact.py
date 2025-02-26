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

@pytest.mark.release_one
@pytest.mark.P1
def test_link_unlink_contact(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 30)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()

    # Navigate to installed pakages setup
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")

    # Switch to Contact Tab
    contact_ele = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Contacts']")))
    contact_ele.click()

    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])[2]")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Unlinked Contacts")
    time.sleep(1)

    # Click on search button
    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@name='searchTerm'])[2]")))
        btn.clear()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        pass

    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    time.sleep(5)
    btn.click()

    try:
        # store account name
        contact_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody/tr[1]/td[2]")))
        contact_text = contact_field.text
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        pass


    # Click on first contact name checkbox
    first_box = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")))
    first_box.click()

    # Click on linked contact
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "//select[@name='MassUploadActions']")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Link Selected Contacts to Existing Contacts")


    # Click on linked account
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@class='slds-select'])[6]")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Dakota Email")


    try:
        dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//select[@class='slds-select'])[7]")))
        dropdown_option = Select(dropdown)
        dropdown_option.select_by_visible_text("Email")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        pass

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_neutral slds-button slds-button--brand '][normalize-space()='Search']"))).click()
    time.sleep(8)

    # Check if it is already mapped
    cross_icon = driver.find_elements(By.XPATH, "(//lightning-primitive-icon[@variant='bare'])[255]")

    if not cross_icon:
        # Select account name
        search_fld = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search by Name']")))
        search_fld.click()
        search_fld.send_keys("test")

        try:
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[contains(text(),'test')])[1]")))
            btn.click()
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__}")
            pass


    # Click on linked account
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