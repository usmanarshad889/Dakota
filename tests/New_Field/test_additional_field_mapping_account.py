import time
import random
import string
import pytest
from faker import Faker
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

field_name = "Automation " + ''.join(random.choices(string.ascii_uppercase, k=3))
print(field_name)

# Generate Random Name, Email and Phone
fake = Faker()
random_name = "Test " + fake.name()  # Add 'test' at the start of the name
email_prefix = ''.join(random.choices(string.ascii_lowercase, k=7))
random_email = f"www.{email_prefix}.com"
random_phone = ''.join(random.choices(string.digits, k=9))
# Print the generated values
print("Name:", random_name)
print("Email:", random_email)
print("Phone:", random_phone)
# Store them in variables
name_var = random_name
email_var = random_email
phone_var = random_phone

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.release_three
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Field Synchronization")
@allure.story("Validate the synchronization of the newly added field and ensure its correct mapping.")
def test_field_addition_to_account(driver, config):
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


    # Navigate to account's object field and relationship page
    package_url = f"{config['base_url']}lightning/setup/ObjectManager/Account/FieldsAndRelationships/view"
    driver.get(package_url)

    # Click on New button
    btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Custom Field']")))
    time.sleep(1)
    btn.click()

    # Switch to iframe
    iframe = wait.until(EC.element_to_be_clickable((By.XPATH, "//iframe[@title='Account: New Custom Field ~ Salesforce - Enterprise Edition']")))
    driver.switch_to.frame(iframe)
    time.sleep(1)

    # Scroll down in iframe
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[1]")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Lookup Relationship']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Date/Time']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Phone']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)

    # Click on Text field radio button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='dtypeS']")))
    btn.click()

    # scroll up
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//h3[1]")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(1)

    # Click on Next button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pbTopButtons']//input[@title='Next']")))
    btn.click()

    # Enter Field Label
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='MasterLabel']")))
    btn.send_keys(field_name)

    # Enter length
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Length']")))
    btn.send_keys("35")

    # Enter Description
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@name='Description']")))
    btn.send_keys("This is Automation field description created by Selenium Python")

    # Enter Help Text
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea[@name='InlineHelpText']")))
    btn.send_keys("Automation Test")

    # Click on Next button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pbTopButtons']//input[@title='Next']")))
    btn.click()

    # Click on Visible checkbox
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@title='Visible'])")))
    btn.click()

    # Click on Next button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pbTopButtons']//input[@title='Next']")))
    btn.click()

    # Click on Save button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='pbTopButtons']//input[@title='Save']")))
    btn.click()

    # Switch out of iframe
    driver.switch_to.default_content()
    time.sleep(1)

    # Verify the field creation
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='globalQuickfind']")))
    btn.send_keys(field_name)
    time.sleep(4)

    # Extract field context
    actual_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//tbody//tr//td[1]")))
    print(f"Actual field Text : {actual_field.text}")

    assert actual_field.text == field_name , f"Expected field was {field_name} but got {actual_field.text}"
    time.sleep(1)


    driver.get(config["uat_login_url"])
    driver.delete_all_cookies()
    wait = WebDriverWait(driver, 20)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["uat_username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["uat_password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        time.sleep(1)
        login_button.click()
        time.sleep(2)

        # Wait for URL change
        WebDriverWait(driver, 20).until(EC.url_contains("/lightning"))

    except Exception as e:
        pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")


    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)

    # Move to account Tab and click on new button
    driver.get(f"{config['uat_base_url']}lightning/o/Account/list?filterName=__Recent")
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='New']")))
    time.sleep(2)
    new_button.click()
    time.sleep(2)

    # Select a record type
    record_type = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_neutral slds-button slds-button_brand uiButton']")))
    time.sleep(2)
    record_type.click()

    # Select account name
    name_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Name']")))
    name_field.send_keys(name_var)

    # Select phone
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Phone']")))
    field.send_keys(phone_var)

    # Select website
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Website']")))
    field.send_keys(email_var)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Website']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='AUM__c']")))
    element.send_keys("10000")
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Average_Ticket_Size__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Total_Participants__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Trial_Start_Date__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Copyright__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='SEC_Registered_Date__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    element = driver.find_element(By.XPATH, "//input[@name='X100_Marketplace__c']")
    element.click()

    # click on save button
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='SaveEdit']")))
    save_btn.click()
    time.sleep(2)

    # Verify toast_message
    toast = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    toast_massage = toast.text
    print(f"Actual Toast : {toast_massage}")

    assert "was created" in toast_massage.lower().strip() , f"Error while creating account : {toast_massage}"


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
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]"))).click()

    except Exception as e:
        pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
        driver.quit()

    # Navigate to Market Place Search
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")
    time.sleep(3)

    # Define the stopping condition element
    stopping_condition_locator = (By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        # Refresh page and clear cookies
        driver.refresh()

        # Wait for search input and enter the search term
        name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='searchTerm']")))
        name_input.clear()
        name_input.send_keys(name_var)

        search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))

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

    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Link Account']")))
    new_button.click()

    # Locate all 'Link' buttons
    all_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")))

    # Check if any button is enabled
    enabled_buttons = [button for button in all_buttons if button.is_enabled()]

    if not enabled_buttons:  # If all buttons are disabled
        print(f"All {len(all_buttons)} 'Link' buttons are disabled. Performing alternative action.")

        # search the element
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='SearchBar']")))
        btn.clear()
        btn.send_keys("j")
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_brand'][normalize-space()='Search']")))
        btn.click()
        time.sleep(2)

        # Locate all 'Link' buttons
        all_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")))

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

        toast_message = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Actual Toast Text : {toast_message.text}")

        assert toast_message.text.strip() == "Account successfully linked", f"Contact not clicked: {toast_message.text}"
        break  # Stop after clicking the first enabled button

    time.sleep(2)


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
            print("Button is already active")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")


    # Scroll down by 500 pixels
    driver.execute_script("window.scrollBy(0, 500);")
    time.sleep(10)

    # Select phone with CRD
    select_element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='a7Ndy0000001H3gEAE'])[1]")))
    option = Select(select_element)
    option.select_by_visible_text(field_name)

    # Select Website with Account Description
    select_element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='a7Ndy0000001H3hEAE'])[1]")))
    option = Select(select_element)
    option.select_by_visible_text("Account Description")

    try:
        # Select Sync Option
        xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[3]/div[1]/div[1]/div[1]/select[1]'''
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
        xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[4]/div[1]/div[1]/div[1]/select[1]'''
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
        xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[5]/div[1]/div[1]/div[1]/select[1]'''
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
        xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[6]/div[1]/div[1]/div[1]/select[1]'''
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
    driver.execute_script("window.scrollBy(0, 1500);")
    time.sleep(2)

    # Select Save Option
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_btn.click()
    time.sleep(1)
    ok_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='OK']")))
    ok_btn.click()
    time.sleep(15)


    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Search the account
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Account Name']")))
    btn.clear()
    time.sleep(7)
    btn.send_keys(name_var)
    # btn.send_keys("Test Mrs. Theresa Lewis PhD")

    # Click on search button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    btn.click()

    # Click on account
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space()='{name_var}']")))
    # btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[@title='Test Mrs. Theresa Lewis PhD']")))
    btn.click()
    time.sleep(5)

    # Get all window handles (list of tabs)
    tabs = driver.window_handles
    print("Open tabs:", len(tabs))  # Print number of tabs

    # Switch to the second tab (index 1)
    driver.switch_to.window(tabs[1])
    time.sleep(3)

    # Verify by printing the current page title
    print("Switched to Tab - Title:", driver.title)

    driver.refresh()
    time.sleep(7)


    # Scroll down by 300 pixels
    xpath = '''//div[@class='slds-form-element slds-hint-parent test-id__output-root slds-form-element_edit slds-form-element_readonly is-stacked is-stacked-not-editing']//span[@class='test-id__field-label'][normalize-space()='Account Owner']'''
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", element)
    time.sleep(2)

    # Verify the Description with Website
    xpath = '''(//span[@class='test-id__field-value slds-form-element__static slds-grow word-break-ie11'])[13]'''
    des_field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    des_text = des_field.text
    print(f"Description Text : {des_text}")

    # Scroll into view
    element = driver.find_element(By.XPATH, "(//span[@class='test-id__field-value slds-form-element__static slds-grow word-break-ie11'])[13]")
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", element)

    # Scroll into view
    element = driver.find_element(By.XPATH, "//span[normalize-space()='QA Currency Field']")
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", element)
    time.sleep(1)

    automation_list = []

    # Extract automation texts
    for r in range(30, 40):
        try:
            xpath = f'''(//span[@class='test-id__field-value slds-form-element__static slds-grow word-break-ie11'])[{r}]'''
            crd_field = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))  # Ensure element exists
            crd_text = crd_field.text.strip()  # Strip extra spaces
            automation_list.append(crd_text)
            print(f"Automation Text: {crd_text}")
        except Exception as e:
            print(f"Skipping index {r} due to error: {e}")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

    # Assert if phone_var exists in the extracted automation_list
    assert phone_var in automation_list, f"Automation Text Mismatch: Expected '{phone_var}', but got '{automation_list}'"
    assert des_text == email_var, f"Description Mismatch: Expected '{email_var}', but got '{des_text}'"
    time.sleep(2)


    # Delete the field created
    # Navigate to account's object field and relationship page
    package_url = f"{config['base_url']}lightning/setup/ObjectManager/Account/FieldsAndRelationships/view"
    driver.get(package_url)

    # Enter field name
    btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//input[@id='globalQuickfind']")))
    btn.send_keys(field_name)
    time.sleep(4)

    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='rowActionsPlaceHolder slds-button slds-button--icon-border-filled']")))
        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Delete']//div[@class='slds-grid']")))
        btn.click()
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(@class,'label bBody')][normalize-space()='Delete']")))
        btn.click()
        time.sleep(5)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
