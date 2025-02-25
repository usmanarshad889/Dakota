import time
import random
import string
import pytest
import allure
from allure_commons.types import AttachmentType
from faker import Faker
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Initialize Faker
fake = Faker()
phone = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
mobile = f"{random.randint(100,999)}-{random.randint(100,999)}-{random.randint(1000,9999)}"
mailing_address = fake.address()
account_name = fake.company()
name = fake.name()
first_name = fake.first_name()
last_name = fake.last_name()
suffix = random.choice(['Jr.', 'Sr.', 'III', 'PhD', 'MD', 'Esq.'])
email = fake.email()
title = fake.job()
contact_type = random.choice(['Personal', 'Business', 'Emergency', 'Billing'])
search_name = "Test" + " " + last_name
full_name = "Test" + " " + last_name + " " + suffix
print(full_name)

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
@pytest.mark.release_one
def test_contact_record_auto_sync(driver, config):
    driver.get("https://test.salesforce.com/")
    wait = WebDriverWait(driver, 20)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys("draftsf@draftdata.com.uat")
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys("Rolustech@99")
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()

    # Move to account Tab and click on new button
    driver.get("https://dakotanetworks--uat.sandbox.lightning.force.com/lightning/o/Contact/list")
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='New']")))
    time.sleep(2)
    new_button.click()
    time.sleep(2)

    # Select a record type
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_neutral slds-button slds-button_brand uiButton']")))
    time.sleep(2)
    new_button.click()

    # Select account name
    name_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Phone']")))
    name_field.send_keys(phone)

    # Select phone
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='MobilePhone']")))
    field.send_keys(mobile)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='city']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='LinkedIn_URL__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='GHIN__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    # SELECT Account type
    input_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search Accounts...']")))
    input_field.clear()
    input_field.send_keys("Test Contacts")
    dropdown_option = wait.until(EC.element_to_be_clickable((By.XPATH, "(//lightning-base-combobox-item[@role='option'])[2]")))
    dropdown_option.click()

    # Select account name
    salutation_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='salutation']")))
    salutation_field.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Mr.']")))
    btn.click()

    # Select First name
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='firstName']")))
    btn.send_keys("Test")
    # driver.find_element(By.XPATH, "//input[@name='middleName']").send_keys(middle_name)
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='lastName']")))
    btn.send_keys(last_name)
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='suffix']")))
    btn.send_keys(suffix)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Email']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(2)

    for r in range(1, 101):  # XPath indices start from 1
        try:
            element = driver.find_element(By.XPATH, f"(//input[@name='Marketplace_Verified_Contact__c'])[{r}]")
            element.click()
            print(f"Clicked element {r}")
            break  # Stop after the first successful click
        except NoSuchElementException:
            print(f"Element {r} not found, trying next...")

    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Email']"))).send_keys(email)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Title']"))).send_keys(title)
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Contact Type']"))).click()
    wait.until(EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Administrator']"))).click()

    # click on save button
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='SaveEdit']")))
    save_btn.click()

    time.sleep(2)

    # Verify toast_message
    toast = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    toast_massage = toast.text
    print(f"Actual Toast : {toast_massage}")

    assert "was created" in toast_massage.lower().strip() , f"Error while creating contact : {toast_massage}"
    time.sleep(1)

    # Navigate to login page of fuse app
    driver.get(config["base_url"])

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()
    time.sleep(3)

    # Navigate to Market Place Search
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")

    # Define the stopping condition element
    stopping_condition_locator = (By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        # Refresh page and clear cookies
        driver.delete_all_cookies()
        driver.refresh()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Contacts']"))).click()

        # Wait for search input and enter the search term
        name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@name='searchTerm'])[2]")))
        name_input.clear()
        name_input.send_keys(search_name)

        search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))

        # Double-click search button multiple times until condition is met
        actions = ActionChains(driver)
        for _ in range(3):
            if driver.find_elements(*stopping_condition_locator):
                print("Stopping condition met. Exiting loop.")
                break

            actions.double_click(search_element).perform()

        # If element is found, exit the while loop
        if driver.find_elements(*stopping_condition_locator):
            break

        attempts += 1  # Increment attempt counter

    # Fail test if maximum attempts reached and condition is not met
    assert attempts < max_attempts, "Test failed: Stopping condition not met after 5 attempts"

    # Check for checkboxes after exiting loop
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")
    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    time.sleep(1)


    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='slds-button slds-button_icon-border slds-button_icon-x-small'])[1]")))
    new_button.click()
    time.sleep(1)

    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Link Contact']")))
    new_button.click()


    # Locate all 'Link' buttons
    all_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")))

    # Check if any button is enabled
    enabled_buttons = [button for button in all_buttons if button.is_enabled()]

    if not enabled_buttons:  # If all buttons are disabled
        print(f"All {len(all_buttons)} 'Link' buttons are disabled. Performing alternative action.")

        # search the element
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@name='SearchBar'])")))
        btn.clear()
        btn.send_keys("g")
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_brand'][normalize-space()='Search']")))
        btn.click()
        time.sleep(2)

        # Locate all 'Link' buttons
        all_buttons = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")))

        # Check if any button is enabled
        enabled_buttons = [button for button in all_buttons if button.is_enabled()]

    else:
        print(f"Found {len(enabled_buttons)} enabled 'Link' buttons. Proceeding with normal actions.")
        # Add the code to execute when at least one button is enabled here

    # Click on first enabled button
    for button in enabled_buttons:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        time.sleep(2)
        button.click()
        time.sleep(2)

        toast_message = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Actual Toast Text : {toast_message.text}")

        assert toast_message.text.strip() == "Contact successfully linked", f"Contact not clicked: {toast_message.text}"
        break  # Stop after clicking the first enabled button

    for r in range(1, 3):
        try:
            cancel_btn = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"(//lightning-primitive-icon[@size='small']//*[name()='svg'])[{r}]")))
            cancel_btn.click()
            print(f"Clicked on cancel button {r}")
            break  # Exit loop after the first successful click
        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__} while trying button {r}")
            pass
    time.sleep(3)


    # Navigate to Market Place Setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")


    element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[4]")))
    element.click()
    time.sleep(1)


    try:
        # Click on Auto Sync Field Updates
        inactive_button = driver.find_element(By.XPATH, "//span[@class='slds-checkbox_off']")
        if inactive_button.text == "Inactive":
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='slds-checkbox_faux']")))
            btn.click()
        else:
            pass
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
    time.sleep(2)


    # Switch to contacts mapping
    contact_fld = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Contacts']")))
    contact_fld.click()
    time.sleep(1)

    # Scroll down by 500 pixels
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(10)


    # Select Website with Account Description
    select_element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='a7Ndy0000001H41EAE'])[1]")))
    option = Select(select_element)
    option.select_by_visible_text("Title")

    # Select phone with CRD
    select_element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='a7Ndy0000001H42EAE'])[1]")))
    option = Select(select_element)
    option.select_by_visible_text("CRD #")


    try:
        # Select Sync Option
        xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/table[1]/tr/td[3]/div[1]/div[1]/div[1]/select[1]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Update")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Sync Option not selected")
    time.sleep(1)


    try:
        # Select Sync Option
        xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/table[1]/tr/td[4]/div[1]/div[1]/div[1]/select[1]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Create Task")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Notification Setting field not selected")
    time.sleep(1)


    try:
        # Select Sync Option
        xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/table[1]/tr/td[5]/div[1]/div[1]/div[1]/select[1]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Owner")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Notification Recipient field not selected")
    time.sleep(1)


    try:
        # Select Sync Option
        xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[2]/div[1]/div[1]/table[1]/tr/td[6]/div[1]/div[1]/div[1]/select[1]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Aiman Shakil")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Notification Assignee User/Group not selected")
    time.sleep(1)


    # Scroll down by 1500 pixels
    driver.execute_script("window.scrollBy(0, 2500);")
    time.sleep(2)

    # Select Save Option
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@id='contacts']//button[@class='slds-button slds-button--brand slds-button--small'][normalize-space()='Save']")))
    save_btn.click()
    time.sleep(1)
    ok_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='OK']")))
    ok_btn.click()
    time.sleep(15)

    # try:
    #     toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    #     print(f"Actual Toast Text : {toast_message.text}")
    #     assert toast_message == "Mapping saved successfully." , f"Error while mapping : {toast_message}"
    # except (NoSuchElementException, TimeoutException) as e:
    #     print(f"Error: {type(e).__name__}")
    #     pass
    # time.sleep(2)

    # Navigate to installed pakages setup
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Dakota_Search")

    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Contacts']"))).click()

    # Wait for search input and enter the search term
    name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@name='searchTerm'])[2]")))
    name_input.clear()
    time.sleep(7)
    name_input.send_keys(search_name)

    search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    search_element.click()

    # Click on account
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@title='{full_name}']")))
    btn.click()
    time.sleep(5)

    # Get all window handles (list of tabs)
    tabs = driver.window_handles
    print("Open tabs:", len(tabs))  # Print number of tabs

    # Switch to the second tab (index 1)
    driver.switch_to.window(tabs[1])
    time.sleep(5)

    # Verify by printing the current page title
    print("Switched to Tab - Title:", driver.title)


    # Scroll down by 300 pixels
    xpath = '''//span[normalize-space()='Contact Record Type']'''
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(2)

    # Verify the CRD with phone
    xpath = '''(//span[@class='test-id__field-value slds-form-element__static slds-grow word-break-ie11'])[9]'''
    crd_field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    crd_text = crd_field.text
    print(f"CRD Text : {crd_text}")

    # Verify the Description with Website
    xpath = '''(//span[@class='test-id__field-value slds-form-element__static slds-grow word-break-ie11'])[8]'''
    title_field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    title_text = title_field.text
    print(f"Description Text : {title_text}")

    # Assertions with Correct Messages
    assert crd_text == phone, f"CRD Mismatch: Expected '{phone}', but got '{crd_text}'"
    assert title_text == email, f"Description Mismatch: Expected '{email}', but got '{title_text}'"
    time.sleep(3)
