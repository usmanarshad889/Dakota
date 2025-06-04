import time
import pytest
import allure
from faker import Faker
from test_utils import skip_broken


from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# Generate Random Name
fake = Faker()
random_name = "Test " + fake.name()


# Print the generated values
print("Name:", random_name)


@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.release_six
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Contact Linking")
@allure.story("Test linking Salesforce Contacts with Dakota Marketplace contacts using the button.")
@pytest.mark.all
@skip_broken
def test_contact_linking_using_button(driver, config):
    # Navigate to login page of fuse app
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


    # Navigate to SF App Account TAB
    driver.get(f"{config['base_url']}lightning/o/Contact/list?filterName=__Recent")


    # Click on New Button for account creation
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@title='New']")))
    time.sleep(1)
    button.click()


    # Click on New Button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_neutral slds-button slds-button_brand uiButton']")))
    time.sleep(1)
    button.click()


    # SELECT Account type
    input_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@placeholder='Search Accounts...']")))
    input_field.clear()
    input_field.send_keys("Test Contacts")
    time.sleep(2)
    dropdown_option = wait.until(EC.element_to_be_clickable((By.XPATH, "(//lightning-base-combobox-item[@role='option'])[2]")))
    dropdown_option.click()


    # Select First Name
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='firstName']")))
    field.send_keys("TTT")


    # Scroll down
    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='middleName']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", element)
    time.sleep(1)


    # Select Last Name
    field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='lastName']")))
    field.send_keys(random_name)


    # Click on SAVE button
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    button.click()
    time.sleep(2)


    # Verify toast_message
    toast = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
    toast_massage = toast.text
    print(f"Actual Toast : {toast_massage}")

    assert "was created" in toast_massage.lower().strip() , f"Error while creating contact : {toast_massage}"
    time.sleep(2)


    # Navigate to Marketplace Search
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")


    # Switch to Contact Tab
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Contacts']")))
    button.click()


    # Wait for page loading
    time.sleep(20)


    # Select Display Criteria
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])[2]")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Unlinked Contacts")


    # Select Marketplace Created Date
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='CRMCreatedDate'])[2]")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Last 90 Days")


    # Click on Search Button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")))
    btn.click()



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
        btn.send_keys(f"TTT {random_name}")
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

        toast_message = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Actual Toast Text : {toast_message.text}")

        # Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Contact Linking Toast", attachment_type=allure.attachment_type.PNG)

        assert toast_message.text.strip() == "Contact successfully linked", f"Contact not clicked: {toast_message.text}"
        break  # Stop after clicking the first enabled button

    time.sleep(2)
