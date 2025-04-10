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

@pytest.mark.release_one
@pytest.mark.P1
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Search Functionality - Contact filter")
@allure.story("Validate contacts page filter are working correctly.")
def test_search_functionality_contact_fields(driver, config):
    driver.get(config["uat_login_url"])
    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["uat_username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["uat_password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        time.sleep(2)
        login_button.click()
        time.sleep(3)

        # Wait for URL change
        wait.until(EC.url_contains("lightning.force.com"))

        # Verify Login
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()

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


    # Move to account Tab and click on new button
    driver.get(f"{config['uat_base_url']}lightning/o/Contact/list")
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

    # Select city
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='city']")))
    field.send_keys("Miami")

    # Select state
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='province']")))
    field.send_keys("Florida")

    # Select country
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='country']")))
    field.send_keys("United States")

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
    print(dropdown_option.text)
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

    # Select Asset Class Coverage
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='Asset Class Coverage']")))
    btn.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//lightning-base-combobox-item[@data-value='Commodities']")))
    btn.click()

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Territory']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    # Select Channel Focus
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Banks']")))
    btn.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@title='Move to Chosen'])[3]")))
    btn.click()

    # Select Metro Area
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search Metro Areas...']")))
    field.click()
    field.send_keys("Bosto")
    time.sleep(5)
    values = driver.find_elements(By.XPATH, "(//lightning-base-combobox-item[@role='option'])")
    index_to_use = None  # Store index of "Boston"
    for index, s in enumerate(values, start=1):
        # print(f"{index}: {s.text.strip()}")
        # If "Boston" is found anywhere in the list, store its index
        if "Boston" in s.text.strip():
            index_to_use = index
            break  # Stop searching after finding the first "Boston"
    # Click the element if "Boston" was found
    if index_to_use is not None:
        print(f"Using index {index_to_use} to click 'Boston'.")
        try:
            element = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"(//lightning-base-combobox-item[@role='option'])[{index_to_use}]")))
            first_line = element.text.splitlines()[0] if element.text.strip() else "No text found"
            # print(f"First line of selected element: {first_line}")
            element.click()
        except Exception as e:
            print(f"Error: {type(e).__name__}")
    else:
        print("Boston was not found in the list.")
    time.sleep(1)

    # click on save button
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='SaveEdit']")))
    save_btn.click()
    time.sleep(2)

    # Verify toast_message
    toast = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    toast_massage = toast.text
    print(f"Actual Toast : {toast_massage}")

    assert "was created" in toast_massage.lower().strip() , f"Error while creating contact : {toast_massage}"
    time.sleep(2)

    # Navigate to login page of fuse app
    driver.get(config["base_url"])

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



    # Navigate to Market Place Search
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Define the stopping condition element
    stopping_condition_locator = (By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        # Refresh page and clear cookies
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

    # Verify Contact name filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Contact Name", attachment_type=allure.attachment_type.PNG)

    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("Contact name filter verified")
    time.sleep(1)


    # Verify account name filter
    acc_name = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='accountName']")))
    acc_name.send_keys("test")
    acc_name.click()
    search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    search_element.click()

    # Verify Account name filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Account Name", attachment_type=allure.attachment_type.PNG)

    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("Account name filter verified")
    time.sleep(1)


    # Verify Coverage Area
    cov_area = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Select Coverage Area(s)'])")))
    cov_area.click()
    value_field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Filter values..'])[5]")))
    value_field.send_keys("Commodities")
    com_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[@data-name='Commodities'])")))
    com_value.click()

    search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    search_element.click()

    # Verify Coverage Area filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Coverage Area", attachment_type=allure.attachment_type.PNG)

    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("Coverage Area filter is verified")
    time.sleep(1)


    # Verify Channel Focus
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select Channel Focus']")))
    btn.click()
    value_field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Filter values..'])[6]")))
    value_field.send_keys("Banks")
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[@data-name='Banks'])")))
    btn.click()

    search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    search_element.click()

    # Verify Channel Focus filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Channel Focus", attachment_type=allure.attachment_type.PNG)

    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("Channel Focus filter is verified")
    time.sleep(1)


    # Verify Metro Area Filter
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Select Metro Area(s)')])[2]")))
    btn.click()
    value_field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[7]")))
    value_field.send_keys("Boston")
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[@data-name='Boston'])[2]")))
    btn.click()
    time.sleep(1)

    wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Contacts']"))).click()
    time.sleep(1)

    search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    search_element.click()

    # Verify Metro Area filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Metro Area", attachment_type=allure.attachment_type.PNG)

    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("Metro Area filter is verified")
    time.sleep(1)


    # # Verify State Filter
    # btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Select State(s)')])[2]")))
    # btn.click()
    # value_field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[9]")))
    # value_field.send_keys("Florida")
    # btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[@data-name='Florida'])[2]")))
    # btn.click()
    #
    # search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    # search_element.click()
    #
    # # Verify State filter
    # checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    # # Take Screenshot & Attach to Allure
    # screenshot = driver.get_screenshot_as_png()
    # allure.attach(screenshot, name=f"State", attachment_type=allure.attachment_type.PNG)

    # assert len(checkboxes) > 0, "Checkbox not found or not visible"
    # print("State filter is verified")
    # time.sleep(1)


    # Verify Contact Type Filter
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Select Type(s)')])[2]")))
    btn.click()
    value_field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[10]")))
    value_field.send_keys("Administrator")
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[@data-name='Administrator'])")))
    btn.click()

    search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    search_element.click()

    # Verify Contact Type filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Contact Type", attachment_type=allure.attachment_type.PNG)

    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    print("Contact Type filter is verified")
    time.sleep(1)
