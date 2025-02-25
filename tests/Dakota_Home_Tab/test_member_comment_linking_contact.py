import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Dakota Home Tab - Ask Dakota, Link Contact")
@allure.story("Test linking of contact directly from member comment")
def test_role_change_linking_contact(driver, config):
    # Navigate to login page
    driver.get(config["base_url"])
    wait = WebDriverWait(driver, 20)

    # Perform login
    username = wait.until(EC.element_to_be_clickable((By.ID, "username")))
    username.send_keys(config["username"])
    password = wait.until(EC.element_to_be_clickable((By.ID, "password")))
    password.send_keys(config["password"])
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "Login")))
    login_button.click()

    # Navigate to Dakota Home Page
    driver.get(f"{config["base_url"]}lightning/n/Marketplace__Home")

    # Print Section name
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='title-div'][normalize-space()='Ask Dakota']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", btn)
    time.sleep(1)
    print(f"Section Name : {btn.text}")

    # Click on View all button
    view_all = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'View All')])[2]")))
    view_all.click()

    # Locate all Contact Names
    xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-comments-relatedto-acc-con-homepage-view-all[1]/article[1]/div[2]/div[1]/div/div[1]/div[2]/p[2]/b[1]/a[1]'''
    elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, xpath)))

    # Click on first unlinked account
    for element in elements:
        try:
            # Skip elements with zero size
            size = element.size
            if size['width'] == 0 or size['height'] == 0:
                continue
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(2)
            contact_name = element.text.strip()
            element.click()

            # Check if the account has right permission or not
            try:
                toast = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
                toast_message = toast.text
                # Check if the message is "You do not have permission rights to access this record."
                if toast_message == "You do not have permission rights to access this record.":
                    print(f"Permission error for account: {contact_name}. Trying next element...")
                    time.sleep(5)
                    continue  # Skip to the next element in the loop
            except (NoSuchElementException, TimeoutException) as e:
                print(f"Error: {type(e).__name__}")
                pass

            wait.until(
                EC.visibility_of_element_located((By.XPATH, f"//h2[normalize-space()='Contact: {contact_name}']")))
            print(f"Clicked Account Name: {contact_name}")
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
        btn.send_keys("x")
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
        time.sleep(1)

        toast_message = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Actual Toast : {toast_message.text}")

        assert toast_message.text.strip().lower() == "contact successfully linked", f"Contact not clicked: {toast_message.text}"
        break  # Stop after clicking the first enabled button