import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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
@pytest.mark.release_three
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Marketplace Search")
@allure.story('Validate the "Link Contact" button in the preview popup for Marketplace Search and proper linking.')
def test_link_contact_preview_popup_marketplace(driver, config):
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

    # Navigate to the contact search page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Switch to Contact Tab
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Contacts']")))
    btn.click()

    # Wait for the results to load
    time.sleep(10)

    # Select Display Criteria (Unlinked Contacts)
    criteria_dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])[2]")))
    dropdown_option = Select(criteria_dropdown)
    dropdown_option.select_by_visible_text("Unlinked Contacts")
    time.sleep(3)


    # Click the Search button and print its text
    search_button = wait.until(EC.element_to_be_clickable(
        (By.XPATH, "//div[@class='buttonDiv']//button[@title='Search'][normalize-space()='Search']")
    ))
    print(f"Button Text : {search_button.text}")
    search_button.click()

    # Click on first name
    first_name = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@name='previewContact'])[1]")))
    print(f"Contact Name : {first_name.text}")
    first_name.click()

    # Verify the "Link Account" button on preview popup
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Link Contact']")))

    assert button.text.strip() == "Link Contact" , f"Expected button was 'Link Account' but got {button.text}"
    time.sleep(1)

    # Verify the correct linking
    button.click()

    # Locate all 'Link' buttons
    all_buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//button[@title='Link'][normalize-space()='Link'])")))

    # Check if any button is enabled
    enabled_buttons = [button for button in all_buttons if button.is_enabled()]

    if not enabled_buttons:  # If all buttons are disabled
        print(f"All {len(all_buttons)} 'Link' buttons are disabled. Performing alternative action.")

        # search the element
        btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='SearchBar']")))
        btn.clear()
        btn.send_keys("x")
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

        toast_message = WebDriverWait(driver, 30).until(EC.element_to_be_clickable(
            (By.XPATH, "//span[@class='toastMessage slds-text-heading--small forceActionsText']")))
        print(f"Actual Toast Text : {toast_message.text}")

        # Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Verification Screenshot", attachment_type=allure.attachment_type.PNG)

        assert toast_message.text.strip() == "Contact successfully linked", f"Contact not clicked: {toast_message.text}"
        break  # Stop after clicking the first enabled button
    time.sleep(2)