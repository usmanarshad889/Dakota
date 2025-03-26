import time
import pytest
import allure
import random
import string

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
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
@pytest.mark.release_two
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Dakota Home Tab - Role Changes (Create Contact)")
@allure.story("Test Creation of contacts directly from Role Changes.")
def test_role_change_creation_of_account(driver, config):
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

    # Print Section name
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Role Changes']")))
    print(f"Section Name : {btn.text}")
    btn.click()

    # Locate all Contacts name
    xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-dakota-home-page-main[1]/div[1]/div[1]/div[1]/c-dakota-contact-updates[1]/div[1]/lightning-tabset[1]/div[1]/slot[1]/lightning-tab[2]/slot[1]/c-dakota-job-and-role-changes[1]/div[1]/div[1]/c-custom-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr/td[2]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-primitive-custom-cell[1]/c-custom-link-field[1]/lightning-button[1]/button[1]'''
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    if not elements:
        pytest.skip("No elements found. Skipping test case.")

    # Click on first found contact
    for element in elements:
        try:
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(1)
            contact_name = element.text.strip()
            element.click()
            print(f"Clicked Contact Name: {contact_name}")
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__} while clicking {element.text}")
        break  # Click only the first element


    # Click on Create Contact
    link_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Create Contact']")))
    link_btn.click()

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

    # # Enter CRD
    # field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='CRD__c']")))
    # field.send_keys(CRD)
    #
    # # Select Contact Type
    # wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Contact Type']"))).click()
    # time.sleep(1)
    # wait.until(EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Administrator']"))).click()
    #
    # # Select Asset Class Coverage
    # wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Asset Class Coverage']"))).click()
    # time.sleep(1)
    # wait.until(EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Alternatives']"))).click()
    #
    # element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='GHIN__c']")))
    # driver.execute_script("arguments[0].scrollIntoView();", element)
    #
    # element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Secondary_Metro_Area__c']")))
    # driver.execute_script("arguments[0].scrollIntoView();", element)
    #
    # element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='QA_Last_Name_Field__c']")))
    # driver.execute_script("arguments[0].scrollIntoView();", element)
    #
    # element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='QA_Number_Field__c']")))
    # driver.execute_script("arguments[0].scrollIntoView();", element)
    #
    # element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='postalCode']")))
    # driver.execute_script("arguments[0].scrollIntoView();", element)
    #
    # element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='QA_Text_Permission_Test__c']")))
    # driver.execute_script("arguments[0].scrollIntoView();", element)
    #
    #
    # # Click Marketplace Verified Contact
    # marketplace_contact = wait.until(
    #     EC.element_to_be_clickable((By.XPATH, "(//input[@name='Marketplace_Verified_Contact__c'])[1]")))
    # marketplace_contact.click()

    # click on save button
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_btn.click()

    time.sleep(2)

    # Wait for toast message
    toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    print(f"Toast message: {toast_message.text}")

    # Verify the Toast message
    assert "was created" in toast_message.text.lower(), f"Test failed: {toast_message.text}"

    # Attach a screenshot of the final state
    allure.attach(driver.get_screenshot_as_png(), name="Final_State_Screenshot", attachment_type=AttachmentType.PNG)
