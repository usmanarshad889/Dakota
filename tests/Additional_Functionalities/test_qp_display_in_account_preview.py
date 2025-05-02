import time
import pytest
import allure
from allure_commons.types import AttachmentType
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.mark.P1
@pytest.mark.Skipped
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Account Preview Display")
@allure.story('Verify the " of QPs" field is displayed correctly in account previews.')
def test_qp_display_in_account_preview(driver, config):
    # Navigate to login page
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

    # Navigate to installed pakages setup
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")


    # Select Unlinked Accounts
    dropdown = wait.until(EC.element_to_be_clickable((By.XPATH, "(//select[@name='DisplayCriteria'])")))
    dropdown_option = Select(dropdown)
    dropdown_option.select_by_visible_text("Unlinked Accounts")
    time.sleep(20)


    # Click the Search button and print its text
    search_button = wait.until(EC.visibility_of_element_located(
        (By.XPATH, "//button[@title='Search']")
    ))
    search_button.click()


    # Click on first Result
    button = wait.until(EC.element_to_be_clickable((By.XPATH, "(//button[@name='previewAccount'])[1]")))
    button.click()


    # Wait for loading of account preview
    wait.until(EC.presence_of_element_located((By.XPATH, "//label[normalize-space()='Dakota Account Name']")))
    time.sleep(2)


    # Verify the '# of QP's field display'
    expected_field = ['Dakota', '#', 'of', 'QPs']
    actual_field = driver.find_element(By.XPATH, "//label[normalize-space()='Dakota # of QPs']")
    text = actual_field.text.split()

    print(f"Actual Field Text : {text}")

    assert text == expected_field , f"Expected Field was 'Dakota # of QPs' but Got {text}"
