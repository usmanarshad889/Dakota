import time
import random
import pytest
import allure
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
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
@allure.feature("Search Functionality")
@allure.story("Test search functionality with multiple keywords.")
def test_video_playback_for_content_on(driver, config):
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



    # Navigate to Dakota Home Page
    driver.get(f"{config['base_url']}lightning/n/Marketplace__Dakota_Video")

    wait.until(EC.visibility_of_element_located((By.XPATH, "(//th[@data-label='Date'])[1]")))
    time.sleep(2)






    # Collect all "Featured On" names
    all_names_elements = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//td[@data-label='Featured On'])")))

    all_names = [elem.text.strip() for elem in all_names_elements if elem.text.strip()]
    assert len(all_names) >= 5, "Not enough 'Featured On' names to perform test!"

    # Select 5 unique names for testing
    random_names = random.sample(all_names, 5)

    print(f"Testing search for these names one by one: {', '.join(random_names)}")

    searched_names = []  # Store all searched names

    for i, name in enumerate(random_names):
        print(f"Step {i+1}: Searching for {name}")

        search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='searchValue']")))

        # Clear search box before each search
        search_box.clear()
        search_box.send_keys(name)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        # Collect current search results
        conf_names = wait.until(EC.presence_of_all_elements_located((By.XPATH, "(//td[@data-label='Featured On'])")))
        current_results = {conf.text.strip().lower() for conf in conf_names}

        # Store searched names
        searched_names.append(name.lower())

        # Screenshot & Allure attachment
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Step {i+1}: {name} - Search Result", attachment_type=allure.attachment_type.PNG)

        # Validate that all previously searched names are in the results
        for searched_name in searched_names:  # Check all names searched so far
            assert any(searched_name in result for result in current_results), f"'{searched_name}' not found in search results!"

        print(f"Validation passed for: {', '.join(searched_names)}")

        # Wait before the next search
        time.sleep(2)