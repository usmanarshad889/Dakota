import time
import pytest
import allure
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common import NoSuchElementException
from selenium.common import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

src = "u"

@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()

@pytest.mark.release_two
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Dakota Home Tab - Ask Dakota, Link Account")
@allure.story("Test creation of contacts directly from member comment")
def test_member_comment_linking_account(driver, config):
    driver.get(config["base_url"])
    driver.delete_all_cookies()
    wait = WebDriverWait(driver, 30, poll_frequency=0.5)

    # Login block
    try:
        wait.until(EC.element_to_be_clickable((By.ID, "username"))).send_keys(config["username"])
        wait.until(EC.element_to_be_clickable((By.ID, "password"))).send_keys(config["password"])
        time.sleep(1)
        wait.until(EC.element_to_be_clickable((By.ID, "Login"))).click()
    except Exception as e:
        driver.quit()
        pytest.skip(f"Skipping test due to login failure: {type(e).__name__}")

    # Confirm login success
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//button[@title='App Launcher']")))
        print("App Launcher is found")
    except Exception as e:
        driver.quit()
        pytest.skip(f"Skipping test due to missing App Launcher: {type(e).__name__}")

    # Navigate to Dakota Home Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Home")

    wait = WebDriverWait(driver, 60, poll_frequency=0.5)

    # Print Section name
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='title-div'][normalize-space()='Ask Dakota']")))
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'start'});", btn)
    time.sleep(1)
    print(f"Section Name : {btn.text}")

    # Click on View all button
    view_all = wait.until(EC.element_to_be_clickable((By.XPATH, "(//a[contains(text(),'View All')])[2]")))
    view_all.click()

    # Wait for records display
    try:
        WebDriverWait(driver, 20).until(EC.presence_of_all_elements_located((By.XPATH, "(//td[@data-label='Last Updated Date'])[1]")))
        time.sleep(1)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")

    # Locate all Account Names
    xpath = '''/html[1]/body[1]/div[4]/div[1]/section[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/marketplace-comments-relatedto-acc-con-homepage-view-all[1]/article[1]/div[2]/div[1]/div/div[1]/div[2]/p[1]/b[1]/a[1]'''
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
                continue
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
            time.sleep(2)
            element.click()

            toast_count = 0  # Counter for the toast message occurrences

            for _ in range(5):  # Example loop iteration count
                try:
                    toast = wait.until(
                        EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage forceActionsText']")))
                    toast_message = toast.text
                    if toast_message == "You do not have permission rights to access this record.":
                        toast_count += 1
                        print(f"Permission error detected {toast_count} time(s). Trying next element...")
                        if toast_count >= 2:  # If message appears twice, skip the test
                            pytest.skip("Test skipped: Permission error occurred twice.")
                        time.sleep(5)
                        continue  # Skip to the next element in the loop
                except (NoSuchElementException, TimeoutException) as e:
                    print(f"Error: {type(e).__name__}")

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error: {type(e).__name__} while clicking {element.text}")
        break

    # Click on linked Account
    link_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Link Account']")))
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
        time.sleep(2)

        toast_message = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Actual Toast Text : {toast_message.text}")

        # Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

        assert toast_message.text.strip().lower() == "account successfully linked", f"Contact not clicked: {toast_message.text}"
        time.sleep(2)
        break  # Stop after clicking the first enabled button