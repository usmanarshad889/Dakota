import time
import pytest
import allure
import random
import string
from test_utils import skip_broken , pass_broken


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
    yield driver
    driver.quit()

@pytest.mark.release_two
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Dakota Home Tab - Job Changes (Create Contact)")
@allure.story("Test Creation of contacts directly from Job Changes.")
@pytest.mark.all
@pass_broken
def test_job_change_creation_of_account(driver, config):
    driver.get(config["base_url"])
    driver.delete_all_cookies()
    wait = WebDriverWait(driver, 30, poll_frequency=0.5)

    # Login block
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(config["username"])
        wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(config["password"])
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.ID, "Login"))).click()
    except Exception as e:
        driver.quit()
        pytest.skip(f"Skipping test due to login failure: {type(e).__name__}")

    # Confirm login success
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='App Launcher']")))
        print("App Launcher is found")
    except Exception as e:
        driver.quit()
        pytest.skip(f"Skipping test due to missing App Launcher: {type(e).__name__}")

    # Navigate to Dakota Home Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Home")

    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

    # Print Section name
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[@class='slds-tabs_default__link'])[1]")))
    print(f"Section Name : {btn.text}")

    # Wait for records display
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "(//td[@data-label='Last Updated Date'])[1]")))
        time.sleep(1)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")


    # Locate all Contacts name
    xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-dakota-home-page-main[1]/div[1]/div[1]/div[1]/c-dakota-contact-updates[1]/div[1]/lightning-tabset[1]/div[1]/slot[1]/lightning-tab[1]/slot[1]/c-dakota-job-and-role-changes[1]/div[1]/div[1]/c-custom-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr/td[2]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-primitive-custom-cell[1]/c-custom-link-field[1]/lightning-button[1]/button[1]'''
    elements = driver.find_elements(By.XPATH, xpath)

    print(f" Total elements present : {len(elements)}")

    if len(elements) == 0:
        pytest.skip("No Account or Contact found that requires creation or linking. Skipping test case.")


    # Click on first unlinked account
    for element in elements:
        try:
            # Skip elements with zero size
            size = element.size
            if size['width'] == 0 or size['height'] == 0:
                print("Skipping element with zero size")
                continue
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(2)
            account_name = element.text.strip()
            element.click()

            # Check if the account has right permission or not
            try:
                toast = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
                toast_message = toast.text
                # Check if the message is "You do not have permission rights to access this record."
                if toast_message == "You do not have permission rights to access this record.":
                    print(f"Permission error for account: {account_name}. Trying next element...")
                    time.sleep(5)
                    continue  # Skip to the next element in the loop
            except (NoSuchElementException, TimeoutException) as e:
                print(f"Error: {type(e).__name__}")

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__} while clicking {element.text}")
        break


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

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

    # Verify the Toast message
    assert "was created" in toast_message.text.lower(), f"Test failed: {toast_message.text}"
