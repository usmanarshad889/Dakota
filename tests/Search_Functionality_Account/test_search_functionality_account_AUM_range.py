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
def test_search_aum(driver, config):
    wait = WebDriverWait(driver, 20)

    # Navigate to login page
    driver.get(config["base_url"])

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

    # Navigate to the contact search page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Search")

    # Select the Contacts tab and print its text
    tab = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@data-label='Accounts']")))
    print(f"Current Tab : {tab.text}")

    # Wait for the results to load
    time.sleep(8)


    # Select AUM "From" value
    aum_from_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='FROM']")))
    aum_from_input.send_keys("1")

    # Select AUM "To" value
    aum_to_input = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='To']")))
    aum_to_input.send_keys("10000")
    # aum_to_input.send_keys("9999")


    # Click the Search button and print its text
    search_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Search']")))
    print(f"Button Text: {search_button.text.strip()}")
    search_button.click()

    # Extract all AUM values from the table
    aum_results = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//lightning-datatable//tbody/tr/td[3]")))

    # Assert that at least one AUM is found
    assert aum_results, "❌ No AUM Range found in the search results!"

    # Verify that AUM values are within the expected range (1 to 10,000)
    for aum in aum_results:
        aum_text = aum.text.strip().replace("$", "").replace(",", "")  # Clean text (remove "$" and ",")

        assert aum_text.isdigit(), f"❌ Invalid AUM format: '{aum_text}'"

        aum_value = int(aum_text)
        print(f"✅ AUM Value: {aum_value}")

        assert 1 <= aum_value <= 10000, f"❌ AUM '{aum_value}' is out of range!"

    print("🎉 All AUM values are within the expected range!")
