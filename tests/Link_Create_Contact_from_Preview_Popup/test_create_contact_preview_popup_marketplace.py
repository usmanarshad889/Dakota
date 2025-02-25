import time
import pytest
import allure
import random
import string
from selenium.webdriver.support.ui import Select
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Generate random phone and mobile numbers
phone = "".join(random.choices(string.digits, k=10))
mobile = "".join(random.choices(string.digits, k=10))

# Generate a random suffix
suffix = random.choice(["Jr.", "Sr.", "I", "II", "III", "IV", "V"])

# Generate a random email
email = "".join(random.choices(string.ascii_lowercase, k=7)) + "@example.com"

# Generate a random CRD number
CRD = "".join(random.choices(string.digits, k=5))

print("Phone:", phone)
print("Mobile:", mobile)
print("Suffix:", suffix)
print("Email:", email)
print("CRD:", CRD)

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
def test_create_contact_preview_popup_marketplace(driver, config):
    wait = WebDriverWait(driver, 20)

    # Navigate to login page
    driver.get(config["base_url"])

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()

    # Navigate to the contact search page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Switch to Contact Tab
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Contacts']")))
    btn.click()

    # Wait for the results to load
    time.sleep(10)

    # Select Display Criteria (Unlinked Contacts)
    criteria_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])[2]")))
    dropdown_option = Select(criteria_dropdown)
    dropdown_option.select_by_visible_text("Unlinked Contacts")
    time.sleep(3)


    # Click the Search button and print its text
    search_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")
    ))
    print(f"Button Text : {search_button.text}")
    search_button.click()

    # Click on first name
    first_name = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@name='previewContact'])[1]")))
    print(f"Contact Name : {first_name.text}")
    first_name.click()

    # Verify the "Create Account" button on preview popup
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Create Contact']")))

    assert button.text.strip() == "Create Contact" , f"Expected button was 'Create Account' but got {button.text}"
    time.sleep(1)

    # Verify the correct Creation
    button.click()

    # Select Account Name
    input_field = wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search Accounts...']")))
    input_field.clear()
    input_field.send_keys("Test Contacts")
    dropdown_option = wait.until(EC.visibility_of_element_located((By.XPATH, "(//lightning-base-combobox-item[@role='option'])[2]")))
    dropdown_option.click()

    # Select name - Salutation
    salutation_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='salutation']")))
    salutation_field.click()
    time.sleep(1)
    driver.find_element(By.XPATH, "//lightning-base-combobox-item[@data-value='Mr.']").click()

    # Enter Phone
    name_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Phone']")))
    name_field.send_keys(phone)

    # Enter Mobile
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='MobilePhone']")))
    field.send_keys(mobile)

    # Scroll down
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='MobilePhone']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    # Select Suffix
    suffix_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='suffix']")))
    suffix_input.send_keys(suffix)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='suffix']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    # Enter Email
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Email']")))
    field.send_keys(email)

    # click on save button
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_btn.click()

    time.sleep(2)

    # Wait for toast message
    toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    print(f"Toast message: {toast_message.text}")

    # Verify the Toast message
    assert "was created" in toast_message.text.lower(), f"Test failed: {toast_message.text}"
    time.sleep(2)

    # Attach a screenshot of the final state
    allure.attach(driver.get_screenshot_as_png(), name="Final_State_Screenshot", attachment_type=AttachmentType.PNG)