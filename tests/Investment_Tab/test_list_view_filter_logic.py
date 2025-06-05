import time
from datetime import datetime
import pytest
import allure
from test_utils import skip_broken , pass_broken

from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    """Fixture for setting up WebDriver"""
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.release_four
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Custom List View Filters")
@allure.story("Validate filters and filter logic in custom list views.")
@pytest.mark.all
@pass_broken
def test_list_view_filter_logic(driver, config):
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


    # Click on Marketplace Search button
    try:
        btn = WebDriverWait(driver, 30).until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]")))
        btn.click()
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
    time.sleep(1)


    # Navigate to Marketplace Investment Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Investments")


    # Verify Investment Page Loaded
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, "(//td[@data-label='Created Date'])[1]")))
        assert element.is_displayed(), "Investment list is not displayed"
    except TimeoutException:
        pytest.fail("Investment list not loaded in time")


    # Create a List View
    gear_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Open Settings']")))
    gear_icon.click()

    # First Create a View
    new_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='New']")))
    if new_button.is_enabled():
        new_button.click()
    else:
        pytest.skip("Create List button is not enabled")


    # Enter Name of View
    name_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']")))
    name_field.clear()
    name_field.send_keys("Test Filter")


    # Save the View
    save_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    driver.execute_script("arguments[0].click();", save_btn)
    time.sleep(1)


    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Create List", attachment_type=allure.attachment_type.PNG)


    verify_element = wait.until(
        EC.presence_of_element_located((By.XPATH, "//span[@class='slds-truncate'][normalize-space()='Test Filter']")))
    assert verify_element.is_displayed(), "List View not created"
    element = wait.until(EC.presence_of_element_located((By.XPATH, "(//td[@data-label='Created Date'])[1]")))
    assert element.is_displayed(), "Investment list is not displayed"


    # Edit Filter Logic
    gear_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Open Settings']")))
    gear_icon.click()


    # Filter Logic
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Edit List Filters']")))
    if button.is_enabled():
        button.click()
        time.sleep(7)
    else:
        pytest.skip("Filter Logic button is not enabled")


    # Click on Add Filter
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Add Filter']")))
    time.sleep(1)
    btn.click()


    # Select Field Option
    field_name = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@type='button' and @part='input-button'])[2]")))
    field_name.click()

    options = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//lightning-base-combobox-item[@role='option']")))

    for option in options:
        option_text = option.text.strip()

        if option_text == "Investment Name":
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", option)
            time.sleep(1)
            option.click()
    time.sleep(1)


    # Select Operator Logic
    field_name = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@type='button' and @part='input-button'])[3]")))
    field_name.click()

    options = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//lightning-base-combobox-item[@role='option']")))

    for option in options:
        option_text = option.text.strip()

        if option_text == "contains":
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", option)
            time.sleep(1)
            option.click()
    time.sleep(1)


    # Select Value
    value_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@type='text']")))
    value_field.send_keys("Test")

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Filter - Logic", attachment_type=allure.attachment_type.PNG)


    # Click on DONE button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Done']")))
    btn.click()

    # Click on SAVE button
    btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Save']")))
    btn.click()
    time.sleep(5)


    # Extract all Investment names text using a simpler XPath
    inv_names = wait.until(EC.presence_of_all_elements_located(
        (By.XPATH, "//tbody/tr/th")
    ))


    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Filter Result", attachment_type=allure.attachment_type.PNG)


    # Assert that at least one name is found
    assert len(inv_names) > 0, "No investment names found in the search results"


    # Check that all returned contact names contain the text "test"
    for inv in inv_names:
        inv_text = inv.text.strip().lower()
        assert "test" in inv_text, f"Contact name '{inv.text}' does not contain 'test'"

    time.sleep(2)


    try:
        # Delete the List View
        gear_icon = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Open Settings']")))
        gear_icon.click()


        # Delete the list view
        delete_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[@title='Delete']")))
        if delete_button.is_enabled():
            delete_button.click()
        else:
            pytest.skip("Delete button is not enabled")


        # Confirm Delete
        delete_confirm_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Delete']")))
        driver.execute_script("arguments[0].click();", delete_confirm_btn)
        time.sleep(1)


        # Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Delete List", attachment_type=allure.attachment_type.PNG)
        time.sleep(2)
    except (NoSuchElementException, TimeoutException) as e:
        print(f"Message: {type(e).__name__}")
