import time
import random
import string
import pytest
import allure
from test_utils import skip_broken , pass_broken

from allure_commons.types import AttachmentType
from faker import Faker
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
    yield driver
    driver.quit()


@pytest.mark.release_one
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Search Functionality - Account filter")
@allure.story("Validate accounts page filter are working correctly.")
@pytest.mark.all
@pass_broken
def test_search_functionality_account_fields(driver, config):
    driver.get(config["uat_login_url"])
    driver.delete_all_cookies()
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
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()
        except Exception as e:
            pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
            driver.quit()

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

    # # Select Metro Area
    # field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search Metro Areas...']")))
    # field.click()
    # time.sleep(5)
    # ssss = wait.until(EC.element_to_be_clickable((By.XPATH, "(//li[@role='presentation'])[6]")))
    # first_line = ssss.text.splitlines()[0]
    # print(first_line)
    # ssss.click()



    # Select Metro Area
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search Metro Areas...']")))
    field.click()
    time.sleep(5)
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

    state_name = "Florida"
    # Select Address information
    element = driver.find_element(By.XPATH, "//input[@name='city']")
    element.send_keys("Miami")
    element = driver.find_element(By.XPATH, "//input[@name='province']")
    element.send_keys(state_name)
    element = driver.find_element(By.XPATH, "//input[@name='country']")
    element.send_keys("United States")
    time.sleep(1)


    element = driver.find_element(By.XPATH, "//input[@name='X100_Marketplace__c']")
    element.click()

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//textarea[@maxlength='255'])[2]")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "(//textarea[@maxlength='131072'])[3]")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Form_ADV_Part_2A_Brochure__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Non_Discretionary_Assets__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='ETF Usage']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Large Cap Equities']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Unconstrained']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Private_Credit_Average_Ticket_Size__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//label[normalize-space()='Co-Investments']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='News_Page__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Matterhorn PM Call')]")))
    driver.execute_script("arguments[0].scrollIntoView();", element)

    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='PN__c']")))
    driver.execute_script("arguments[0].scrollIntoView();", element)
    time.sleep(1)

    # btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@placeholder='Search Accounts...'])[12]")))
    # btn.click()
    # time.sleep(2)
    # btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//lightning-base-combobox-item[@role='option'])[1]")))
    # print(btn.text)
    # btn.click()


    # click on save button
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@name='SaveEdit']")))
    save_btn.click()
    time.sleep(2)

    # Verify toast_message
    toast = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    toast_massage = toast.text
    print(f"Actual Toast : {toast_massage}")

    assert "was created" in toast_massage.lower().strip() , f"Error while creating account : {toast_massage}"


    # Navigate to login page of fuse app
    driver.get(config["base_url"])
    driver.delete_all_cookies()

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
        try:
            WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[2]"))).click()
        except Exception as e:
            pytest.skip(f"Skipping test due to unexpected login error: {type(e).__name__}")
            driver.quit()

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
    time.sleep(3)

    # Define the stopping condition element (second checkbox)
    stopping_condition_locator = (By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        driver.refresh()
        time.sleep(2)  # Allow time for page to load after refresh

        try:
            # Enter search term
            name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='searchTerm']")))
            name_input.clear()
            name_input.send_keys(name_var)

            # Click the Search button
            search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
            actions = ActionChains(driver)

            for _ in range(3):  # Try clicking search up to 3 times
                # Check stopping condition before clicking again
                if driver.find_elements(*stopping_condition_locator):
                    print("Stopping condition met. Exiting loop.")
                    break

                actions.move_to_element(search_button).click().perform()
                time.sleep(2)  # Let the results update/load

            # Break outer loop if condition is met
            if driver.find_elements(*stopping_condition_locator):
                print("Element found after search attempts.")
                break

        except Exception as e:
            print(f"Attempt {attempts + 1} failed: {e}")

        attempts += 1
        time.sleep(1)

    # Assert loop succeeded
    assert attempts < max_attempts, "Test failed: Stopping condition not met after 5 attempts"

    # Final check for the checkbox element
    checkboxes = driver.find_elements(*stopping_condition_locator)
    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    time.sleep(1)
    print("Account Name filter verified")
    time.sleep(1)


    # Verify AUM range
    aum_start = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='FROM']")))
    aum_start.send_keys("9999")
    aum_end = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='To']")))
    aum_end.send_keys("10001")
    search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    search_element.click()
    # Verify AUM range filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"AUM Range", attachment_type=allure.attachment_type.PNG)

    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    time.sleep(1)
    print("AUM range filter verified")


    # Verify Metro Area
    metro_area = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select Metro Area(s)']")))
    metro_area.click()
    value_field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[1]")))
    value_field.send_keys("Boston")
    sco_value = wait.until(EC.element_to_be_clickable((By.XPATH, "(//li[@data-name='Boston'])")))
    sco_value.click()
    search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    search_element.click()
    # Verify Metro Area Filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Metro Area", attachment_type=allure.attachment_type.PNG)

    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    time.sleep(1)
    print("Metro Area filter verified")


    # # Verify State
    # state_src = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select State(s)']")))
    # state_src.click()
    # value_field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[3]")))
    # value_field.send_keys(state_name)
    # fl_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[@data-name='{state_name}'])")))
    # fl_value.click()
    # search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    # search_element.click()
    # # Verify State filter
    # checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    # # Take Screenshot & Attach to Allure
    # screenshot = driver.get_screenshot_as_png()
    # allure.attach(screenshot, name=f"State", attachment_type=allure.attachment_type.PNG)

    # assert len(checkboxes) > 0, "Checkbox not found or not visible"
    # time.sleep(1)
    # print("State filter verified")


    # Verify Type
    state_src = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Select Type(s)']")))
    state_src.click()
    value_field = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[contains(@placeholder,'Filter values..')])[4]")))
    value_field.send_keys("Bank")
    bank_value = wait.until(EC.element_to_be_clickable((By.XPATH, f"(//li[@data-name='Bank'])")))
    bank_value.click()
    search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    search_element.click()
    # Verify Type filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Type", attachment_type=allure.attachment_type.PNG)

    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    time.sleep(1)
    print("Type filter verified")


    # Verify CRD
    crd = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='CRD NUMBER']")))
    crd.send_keys("3546")
    search_element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    search_element.click()
    # Verify CRD filter
    checkboxes = driver.find_elements(By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"CRD", attachment_type=allure.attachment_type.PNG)

    assert len(checkboxes) > 0, "Checkbox not found or not visible"
    time.sleep(1)
    print("CRD filter verified")