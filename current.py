import time
import random
import pytest
from faker import Faker
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Initialize Faker for random data generation
fake = Faker()

# Generate random data
def generate_contact_data():
    return {
        "phone": f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        "mobile": f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}",
        "account_name": fake.company(),
        "first_name": "Test",
        "last_name": fake.last_name(),
        "suffix": random.choice(['Jr.', 'Sr.', 'III', 'PhD', 'MD', 'Esq.']),
        "email": fake.email(),
        "title": fake.job(),
        "contact_type": random.choice(['Personal', 'Business', 'Emergency', 'Billing']),
    }

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
@pytest.mark.release_two
def test_create_contact_single_record(driver, config):
    wait = WebDriverWait(driver, 20)
    contact = generate_contact_data()
    search_name = f"Test {contact['last_name']}"

    # Salesforce login
    driver.get("https://test.salesforce.com/")
    wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys("draftsf@draftdata.com.uat")
    wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys("Rolustech@99")
    wait.until(EC.element_to_be_clickable((By.ID, "Login"))).click()

    # Navigate to Contact creation page
    driver.get("https://dakotanetworks--uat.sandbox.lightning.force.com/lightning/o/Contact/list")
    wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='New']"))).click()
    time.sleep(2)

    # Select record type
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_neutral slds-button slds-button_brand uiButton']"))).click()

    # Fill out contact form
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Phone']"))).send_keys(contact['phone'])
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='MobilePhone']"))).send_keys(contact['mobile'])

    fields_to_scroll = ["city", "LinkedIn_URL__c", "GHIN__c"]
    for field_name in fields_to_scroll:
        element = wait.until(EC.presence_of_element_located((By.XPATH, f"//input[@name='{field_name}']")))
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        time.sleep(1)

    # Account selection
    input_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search Accounts...']")))
    input_field.clear()
    input_field.send_keys("Test Contacts")
    wait.until(EC.element_to_be_clickable((By.XPATH, "(//lightning-base-combobox-item[@role='option'])[2]"))).click()

    # Personal details
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='salutation']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Mr.']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='firstName']"))).send_keys(contact['first_name'])
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='lastName']"))).send_keys(contact['last_name'])
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='suffix']"))).send_keys(contact['suffix'])

    email_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Email']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", email_element)
    time.sleep(2)

    for idx in range(1, 101):
        try:
            checkbox = driver.find_element(By.XPATH, f"(//input[@name='Marketplace_Verified_Contact__c'])[{idx}]")
            checkbox.click()
            break
        except NoSuchElementException:
            continue

    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Email']"))).send_keys(contact['email'])
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Title']"))).send_keys(contact['title'])

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Contact Type']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Administrator']"))).click()

    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='SaveEdit']"))).click()
    time.sleep(2)

    toast = wait.until(EC.visibility_of_element_located((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    assert "was created" in toast.text.lower(), f"Error creating contact: {toast.text}"

    driver.get(config["base_url"])
    wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(config["username"])
    wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(config["password"])
    wait.until(EC.element_to_be_clickable((By.ID, "Login"))).click()
    time.sleep(3)

    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    max_attempts = 5
    for attempt in range(max_attempts):
        driver.delete_all_cookies()
        driver.refresh()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Contacts']"))).click()

        search_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@name='searchTerm'])[2]")))
        search_input.clear()
        search_input.send_keys(search_name)
        search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))

        ActionChains(driver).double_click(search_button).perform()
        time.sleep(2)

        if driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]"):
            break
    else:
        assert False, "Stopping condition not met after 5 attempts"

    assert driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]"), "No checkboxes found after search"
