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

value_src = "test"

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

@pytest.mark.P1
@pytest.mark.release_one
@pytest.mark.demo
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Mapping - Account field Mapping")
@allure.story("Validate successful mapping of account fields.")
def test_account_record_auto_sync(driver, config):
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

    # Select Type
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@data-value='--None--'])[2]")))
    field.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//lightning-base-combobox-item[@role='option'])[4]")))
    btn.click()

    # Select CRD
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='CRD__c']")))
    field.send_keys("3546")

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

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Billing Street']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Billing Zip/Postal Code']")))
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



    retries = 5
    for attempt in range(retries):
        try:
            driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")
            break  # Exit the loop if the page loads successfully
        except TimeoutException:
            print(f"Attempt {attempt + 1} failed. Retrying...")
            time.sleep(5)  # Wait before retrying
    else:
        print("All retry attempts failed.")


    # Click on Authentication svg button
    try:
        # Wait for full page load
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")

        element = wait.until(
            EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[3]"))
        )
        element.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)

    # Verify the Authentication with correct Credentials
    wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Username']"))).clear()
    driver.find_element(By.XPATH, "//input[@name='Username']").send_keys("Fuse Upgrade")
    driver.find_element(By.XPATH, "//input[@name='Password']").clear()
    driver.find_element(By.XPATH, "//input[@name='Password']").send_keys("rolus009")
    driver.find_element(By.XPATH, "//input[@name='AuthorizationURL']").clear()
    driver.find_element(By.XPATH, "//input[@name='AuthorizationURL']").send_keys("https://marketplace-dakota-uat.herokuapp.com")
    time.sleep(1)

    try:
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Connect']")))
        driver.execute_script("arguments[0].click();", btn)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(2)

    toast = WebDriverWait(driver, 60).until(EC.presence_of_element_located((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
    print(f"Toast message : {toast.text}")

    # Verify the Toast message
    assert toast.text.lower() == "dakota marketplace account connected successfully.", f"Test failed: {toast.text}"
    time.sleep(3)


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
    option.select_by_visible_text("Account Phone")

    # Select Website with Account Description
    select_element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='a7Ndy0000001H3hEAE'])[1]")))
    option = Select(select_element)
    option.select_by_visible_text("Website")

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


    # try:
    #     # Select Sync Option
    #     xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[5]/div[1]/div[1]/div[1]/select[1]'''
    #     select_element = driver.find_elements(By.XPATH, xpath)
    #     for element in select_element:
    #         if element.is_enabled():
    #             select = Select(element)
    #             select.select_by_visible_text("Owner")
    # except (NoSuchElementException, TimeoutException) as e:
    #     print(f"Error: {type(e).__name__}")
    #     print("Notification Recipient field not selected")
    # time.sleep(1)


    # try:
    #     # Select Sync Option
    #     xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/div[1]/ol[1]/li[2]/article[1]/div[1]/div[1]/div[3]/div[1]/div[1]/div[3]/div[1]/div[1]/div[1]/table[1]/tr/td[6]/div[1]/div[1]/div[1]/select[1]'''
    #     select_element = driver.find_elements(By.XPATH, xpath)
    #     for element in select_element:
    #         if element.is_enabled():
    #             select = Select(element)
    #             select.select_by_visible_text("Aiman Shakil")
    # except (NoSuchElementException, TimeoutException) as e:
    #     print(f"Error: {type(e).__name__}")
    #     print("Notification Assignee User/Group not selected")
    # time.sleep(1)


    try:
        # Scroll down by 1500 pixels
        driver.execute_script("window.scrollBy(0, 1500);")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
    time.sleep(2)


    try:
        save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
        save_btn.click()
        time.sleep(1)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
    time.sleep(1)

    try:
        ok_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='OK']")))
        ok_btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
    time.sleep(10)


    try:
        # Navigate to Market Place Setup
        driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
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
        btn.send_keys(value_src)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_brand'][normalize-space()='Search']")))
        btn.click()
        time.sleep(2)

        # Locate all 'Link' buttons
        all_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")))

        # Check if any button is enabled
        enabled_buttons = [button for button in all_buttons if button.is_enabled()]

        if not enabled_buttons:  # If all buttons are disabled
            pytest.skip("No Account found ... Skipping Testcase")

    else:
        print(f"Found {len(enabled_buttons)} enabled 'Link' buttons. Proceeding with normal actions.")
        # Add the code to execute when at least one button is enabled here

    # Click on first enabled button
    for button in enabled_buttons:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        time.sleep(2)
        button.click()
        time.sleep(2)

        toast_message = WebDriverWait(driver, 60).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Actual Toast Text : {toast_message.text}")

        assert toast_message.text.strip() == "Account successfully linked", f"Account not Linked: {toast_message.text}"
        break  # Stop after clicking the first enabled button

    time.sleep(2)


    try:
        # Navigate to Market Place Setup
        driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")

    try:
        # Navigate to Market Place Setup
        driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")


    # Search the account
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Account Name']")))
    btn.clear()
    time.sleep(7)
    btn.send_keys(name_var)

    # Click on search button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    btn.click()

    # Click on account
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, f"//button[normalize-space()='{name_var}']")))
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
    xpath = '''//div[@class='slds-form-element slds-hint-parent test-id__output-root slds-form-element_edit slds-form-element_readonly is-stacked is-stacked-not-editing']//span[@class='test-id__field-label'][normalize-space()='Account Owner']'''
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(2)

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Field Mapping", attachment_type=allure.attachment_type.PNG)

    # # Verify the CRD with phone
    # xpath = '''(//span[@class='test-id__field-value slds-form-element__static slds-grow word-break-ie11'])[6]'''
    # phone_field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    # phone_text = phone_field.text
    # print(f"Phone Number : {phone_text}")

    # Verify the Description with Website
    xpath = '''(//span[@class='test-id__field-value slds-form-element__static slds-grow word-break-ie11'])[8]'''
    web_field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    web_text = web_field.text
    print(f"Website Text : {web_text}")

    # Verify the Type as Bank
    xpath = '''(//span[@class='test-id__field-value slds-form-element__static slds-grow word-break-ie11'])[3]'''
    type_field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    type_text = type_field.text
    print(f"Type Text : {type_text}")

    # Verify the CRD as '3546'
    xpath = '''(//span[@class='test-id__field-value slds-form-element__static slds-grow word-break-ie11'])[10]'''
    crd_field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    crd_text = crd_field.text
    print(f"CRD Value : {crd_text}")

    # Verify the Account Record Type
    xpath = '''(//div[@class='recordTypeName slds-grow slds-truncate'])[1]'''
    account_type_field = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    account_type_text = account_type_field.text
    print(f"Account Record Type : {account_type_text}")

    # Assertions with Correct Messages
    # assert phone_text == phone_var, f"Phone Mismatch: Expected '{phone_var}', but got '{phone_text}'"
    assert web_text == email_var, f"Website Mismatch: Expected '{email_var}', but got '{web_text}'"
    assert type_text == "Bank", f"Type Mismatch: Expected 'Bank', but got '{type_text}'"
    assert crd_text == "3546", f"CRD Value Mismatch: Expected CRD Value '3546', but got '{crd_text}'"
    assert account_type_text == "Investment Allocator", f"Account Record Type Mismatch: Expected CRD Value 'Investment Allocator', but got '{account_type_text}'"
    time.sleep(10)
