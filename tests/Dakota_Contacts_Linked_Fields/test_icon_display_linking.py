import time
import random
import pytest
import allure
from test_utils import skip_broken

from allure_commons.types import AttachmentType
from faker import Faker
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


value_src = "uuu"

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

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.release_four
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Contact Linking")
@allure.story('Validate the "Dakota Contact Linked" field displays a linked icon after linking.')
@pytest.mark.all
@skip_broken
def test_icon_display_linking(driver, config):
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
    driver.get(f"{config['uat_base_url']}lightning/o/Contact/list")
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='New']")))
    time.sleep(2)
    new_button.click()
    time.sleep(2)

    # Select a record type
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_neutral slds-button slds-button_brand uiButton']")))
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

    # Define the stopping condition element (second checkbox)
    stopping_condition_locator = (By.XPATH, "(//span[@class='slds-checkbox_faux'])[2]")

    max_attempts = 5
    attempts = 0

    while attempts < max_attempts:
        driver.refresh()
        wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Contacts']"))).click() # Allow time for page to load after refresh

        try:
            # Enter search term
            name_input = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@name='searchTerm'])[2]")))
            name_input.clear()
            name_input.send_keys(search_name)

            # Click the Search button
            search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
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
        btn.send_keys(value_src)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_brand'][normalize-space()='Search']")))
        btn.click()
        time.sleep(2)

        # Locate all 'Link' buttons
        all_buttons = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")))

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

        toast_message = WebDriverWait(driver, 60).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Actual Toast Text : {toast_message.text}")

        # Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

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
    time.sleep(3)

    # Search by name
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@name='searchTerm'])[2]")))
    btn.clear()
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@name='searchTerm'])[2]")))
    btn.send_keys(search_name)
    time.sleep(5)
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    btn.click()

    # Check for SVG after exiting loop
    svg_element = driver.find_elements(By.XPATH, "//tbody/tr[1]/th[1]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-icon[1]/span[1]/lightning-primitive-icon[1]//*[name()='svg']")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

    assert len(svg_element) > 0, "Link icon not found or not visible"
    time.sleep(1)
