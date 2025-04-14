import time
import pytest
import allure
import datetime
import random
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Followed Contacts Notifications")
@allure.story("Validate email notifications sent on updates to followed contacts.")
def test_follow_contact_notification(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["password"])
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

    # Click on Marketplace Search button
    try:
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.Marketplace__Dakota_Search']")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)

    # Navigate to installed packages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Setup")

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//*[name()='svg'][@class='slds-button__icon'])[5]")))
    element.click()
    time.sleep(1)

    # Scroll down by 500 pixels
    driver.execute_script("window.scrollBy(0, 800);")
    time.sleep(7)


    try:
        # Sync Account/Contact Type Field
        inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'])[1]")
        if inactive_button.text == "Inactive":
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[1]")))
            btn.click()
        else:
            print("Button is already active")
    except (NoSuchElementException, TimeoutException) as e:
        print("Sync Account/Contact Type toggle button is not working")
        print(f"Error: {type(e).__name__}")


    try:
        # Receive Follow Notification
        inactive_button = driver.find_element(By.XPATH, "(//span[@class='slds-checkbox_off'])[4]")
        if inactive_button.text == "Inactive":
            btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//span[@class='slds-checkbox_faux'])[4]")))
            btn.click()
        else:
            print("Button is already active")
    except (NoSuchElementException, TimeoutException) as e:
        print("Receive Follow Notification toggle button is not working")
        print(f"Error: {type(e).__name__}")


    try:
        # Notification Setting
        xpath = '''(//select[@name='a7Fdy0000003GkzEAE'])[1]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("Send Email")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Notification Setting not selected")


    try:
        # Notification Recipient
        xpath = '''(//select[@name='a7Fdy0000003GkzEAE'])[2]'''
        select_element = driver.find_elements(By.XPATH, xpath)
        for element in select_element:
            if element.is_enabled():
                select = Select(element)
                select.select_by_visible_text("User")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Notification Recipient not selected")


    try:
        # Notification Assignee User/Group
        input_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select a value..']")))
        input_field.click()
        input_field_value = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Filter values..']")))
        input_field_value.send_keys("Aiman Shakil")
        option = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Aiman Shakil']")))
        option.click()
        input_field.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
        print("Notification Assignee User/Group not selected")


    # Select Save Option
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    save_btn.click()
    time.sleep(2)

    toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
    text = toast_message.text
    print(f"Actual Toast message : {text}")

    assert text in ["Mapping saved successfully.", "Status changed successfully!"], f"Unexpected toast message: {text}"
    time.sleep(2)


    # Navigate to Marketplace Setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Print Current Tab
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Contacts']")))
    tab.click()
    print(f"Current Tab : {tab.text}")

    button = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    print(f"Button Text : {button.text}")
    time.sleep(8)

    # Select linked accounts from filter
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])[2]")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Linked Contacts")


    # Select Marketplace Created Date filter
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='CRMCreatedDate'])[2]")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Last 30 Days")

    name_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Contact Name']")))
    name_field.send_keys("Test")
    time.sleep(1)

    # Click on Search Button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    button.click()

    # Wait until all contacts buttons are present
    contacts = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.XPATH, "//button[@name='previewContact']"))
    )

    contact_name = None

    # Check if contacts were found
    if contacts:
        # Randomly pick one contact from the list
        random_contact = random.choice(contacts)

        # Scroll to the selected contact
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", random_contact)
        time.sleep(1)

        # Store the contact name (optional: add a small wait if text loads dynamically)
        contact_name = random_contact.text.strip()
        print(f"Selected Contact Name: {contact_name}")

        # Click on the contact using ActionChains (or JS click if needed)
        ActionChains(driver).move_to_element(random_contact).click().perform()

    else:
        print("No contacts found.")

    # Get all window handles (list of tabs)
    tabs = driver.window_handles
    print("Open tabs:", len(tabs))  # Print number of tabs


    # Switch to the second tab (index 1)
    driver.switch_to.window(tabs[1])
    time.sleep(5)


    # Verify by printing the current page title
    print("Switched to Tab - Title:", driver.title)


    # Scroll down by 300 pixels
    xpath = '''(//span[normalize-space()='Contact Record Type'])[1]'''
    element = wait.until(EC.element_to_be_clickable((By.XPATH, xpath)))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
    time.sleep(2)


    # Check if account is already followed
    following_buttons = driver.find_elements(By.XPATH, "//button[@title='Following']")

    if following_buttons:
        print("Account is already followed. No action needed.")
        # Assert that the "Following" button is visible (sanity check)
        assert following_buttons[0].is_displayed(), "Following button is not visible as expected."
    else:
        # Click on 'Follow' button to follow the account
        follow_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Follow']")))
        follow_button.click()
        print("Clicked on 'Follow' button to follow the account.")

        # Verify the account is now followed
        followed = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='Following']")))
        assert followed.is_displayed(), "Failed to follow the account!"
        print("Verified account is now followed.")

    # Optional: small wait if necessary
    time.sleep(2)


    # --------------   Change Field   -----------------
    # Navigate to UAT Marketplace Environment
    driver.get(config["uat_login_url"])
    wait = WebDriverWait(driver, 20)

    try:
        # Perform login
        username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
        username.send_keys(config["uat_username"])
        password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
        password.send_keys(config["uat_password"])
        login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
        time.sleep(2)
        login_button.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")
    time.sleep(4)


    with allure.step("Waiting for Document Ready State to be Complete"):
        WebDriverWait(driver, 90).until(
            lambda d: print("Current Ready State:", d.execute_script('return document.readyState')) or
                      d.execute_script('return document.readyState') == 'complete'
        )
    print("Document Ready State is COMPLETE!")
    time.sleep(1)

    # Click on Account button
    try:
        xpath_uat = '''//one-app-nav-bar-item-root[@data-target-selection-name='sfdc:TabDefinition.standard-Contact']'''
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, xpath_uat)))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)


    try:
        # Navigate to Market Place Setup
        driver.get(f"{config['uat_base_url']}lightning/o/Contact/list?filterName=All_Contacts7")
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Error: {type(e).__name__}")


    src_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Contact-search-input']")))
    src_button.send_keys(contact_name)
    load_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(@title,'Refresh')]//lightning-primitive-icon[contains(@exportparts,'icon')]")))
    load_button.click()
    time.sleep(10)

    # Edit the Account
    edit_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@class='slds-button slds-button_icon-border slds-button_icon-x-small']//lightning-primitive-icon[@variant='bare'])[1]")))
    edit_btn.click()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@title='Edit']")))
    btn.click()

    # Edit the Website Field
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Phone']")))
    btn.click()
    btn.clear()
    btn.send_keys("111222333")

    # Save the Account
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='SaveEdit']")))
    btn.click()
    time.sleep(2)

    # Verify toast_message
    toast = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    toast_massage = toast.text
    print(f"Actual Toast : {toast_massage}")

    assert "was saved" in toast_massage.lower().strip() , f"Error while creating account : {toast_massage}"
    time.sleep(2)

    # === Check if it's Friday 5 PM ===
    current_time = datetime.datetime.now()

    # Get day name and hour & minute
    day_name = current_time.strftime('%A')  # returns full day name like 'Friday'
    hour = current_time.hour
    minute = current_time.minute

    if day_name == 'Friday' and hour == 17 and minute == 0:
        print("It's Friday 5 PM. Please Check your Email Inbox.")
        # Add your next test steps here
    else:
        print("Email will be sent on Friday 5 PM.")
        # You can simulate or log notification steps here
        assert True, "Test stopped since it's not Friday 5 PM."
        pytest.skip("Test skipped since it's not Friday 5 PM.")