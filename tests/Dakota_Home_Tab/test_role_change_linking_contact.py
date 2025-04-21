import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

src = "b"

@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
@pytest.mark.release_two
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Dakota Home Tab - Role Changes (Link Contact)")
@allure.story("Test linking of accounts directly from Role Changes.")
def test_role_change_linking_contact(driver, config):
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

    # Navigate to Dakota Home Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Home")

    # Print Section name
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//li[@title='Role Changes']")))
    print(f"Section Name : {btn.text}")
    btn.click()

    # Wait for records display
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "(//td[@data-label='Last Updated Date'])[1]")))
        time.sleep(1)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")

    # Locate all Contacts name
    xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-dakota-home-page-main[1]/div[1]/div[1]/div[1]/c-dakota-contact-updates[1]/div[1]/lightning-tabset[1]/div[1]/slot[1]/lightning-tab[2]/slot[1]/c-dakota-job-and-role-changes[1]/div[1]/div[1]/c-custom-datatable[1]/div[2]/div[1]/div[1]/table[1]/tbody[1]/tr/td[2]/lightning-primitive-cell-factory[1]/span[1]/div[1]/lightning-primitive-custom-cell[1]/c-custom-link-field[1]/lightning-button[1]/button[1]'''
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
            contact_name = element.text.strip()
            element.click()

            # Check if the account has right permission or not
            try:
                toast = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
                toast_message = toast.text
                # Check if the message is "You do not have permission rights to access this record."
                if toast_message == "You do not have permission rights to access this record.":
                    print(f"Permission error for account: {contact_name}. Trying next element...")
                    time.sleep(5)
                    continue  # Skip to the next element in the loop
            except (NoSuchElementException, TimeoutException) as e:
                print(f"Error: {type(e).__name__}")

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__} while clicking {element.text}")
        break


    # Click on linked contacts
    link_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Link Contact']")))
    link_btn.click()

    # Locate all 'Link' buttons
    all_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")))

    # Check if any button is enabled
    enabled_buttons = [button for button in all_buttons if button.is_enabled()]

    if not enabled_buttons:  # If all buttons are disabled
        print(f"All {len(all_buttons)} 'Link' buttons are disabled. Performing alternative action.")

        # search the element
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "(//input[@name='SearchBar'])")))
        btn.clear()
        btn.send_keys(src)
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@class='slds-button slds-button_brand'][normalize-space()='Search']")))
        btn.click()
        time.sleep(2)

        # Locate all 'Link' buttons
        all_buttons = wait.until(
            EC.presence_of_all_elements_located((By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")))

        # Check if any button is enabled
        enabled_buttons = [button for button in all_buttons if button.is_enabled()]

        if not enabled_buttons:  # If all buttons are disabled

            # Take Screenshot & Attach to Allure
            screenshot = driver.get_screenshot_as_png()
            allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

            pytest.skip("No Account found ... Skipping Testcase")

    else:
        print(f"Found {len(enabled_buttons)} enabled 'Link' buttons. Proceeding with normal actions.")
        # Add the code to execute when at least one button is enabled here

    # Click on first enabled button
    for button in enabled_buttons:
        driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", button)
        time.sleep(2)
        button.click()
        time.sleep(1)

        toast_message = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Actual Toast : {toast_message.text}")

        # Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

        assert toast_message.text.strip().lower() == "contact successfully linked", f"Contact not clicked: {toast_message.text}"
        break  # Stop after clicking the first enabled button