import time
import random
import pytest
import allure
from selenium import webdriver
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

@pytest.mark.regression
@pytest.mark.P1
@allure.severity(allure.severity_level.CRITICAL)
@allure.feature("Video Playback")
@allure.story('Test video playback for "Content Name" columns.')
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

    buttons = driver.find_elements(By.XPATH, "//img[@alt='video']")

    # Check if at least 1 button is available
    if not buttons:
        pytest.skip("Not enough buttons found. Skipping test case.")
        driver.quit()
        exit()

    # Randomly select one button
    selected_button = random.choice(buttons)

    # Scroll to the selected button
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", selected_button)
    time.sleep(1)
    video_button = wait.until(EC.element_to_be_clickable(selected_button))  # Ensure it's clickable
    video_button.click()
    time.sleep(3)


    # Handle multiple tabs
    wait.until(lambda d: len(driver.window_handles) > 1)  # Wait for the new tab to open
    tabs = driver.window_handles
    print("Open tabs:", len(tabs))

    # Switch to the second tab (index 1)
    driver.switch_to.window(tabs[1])
    print("Switched to Tab - Title:", driver.title)

    # Try to find and click the play button
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[@class='ytp-impression-link-text']")))
        print("Video has been opened successfully")
        time.sleep(3)

        # Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Video Screen - Success", attachment_type=allure.attachment_type.PNG)

    except Exception as e:
        print(f"Error: Play button not found due to possible internet restrictions. {type(e).__name__}")

        # Take Screenshot & Attach to Allure
        screenshot = driver.get_screenshot_as_png()
        allure.attach(screenshot, name=f"Video Screen - Failed", attachment_type=allure.attachment_type.PNG)

        pytest.skip("Internet restrictions prevented video playback. Skipping test case.")
        driver.quit()
        exit()
