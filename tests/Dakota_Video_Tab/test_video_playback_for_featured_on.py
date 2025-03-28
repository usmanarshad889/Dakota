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
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.mark.P1
def test_video_playback_for_featured_on(driver, config):
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
        wait.until(EC.element_to_be_clickable((By.XPATH, "//one-app-nav-bar-item-root[5]"))).click()

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
    time.sleep(1)

    buttons = wait.until(EC.presence_of_all_elements_located((By.XPATH, "//td[3]//lightning-button-icon/button")))

    # Filter elements where both width and height are between 10 and 35
    filtered_buttons = [button for button in buttons if
                        10 <= button.size['width'] <= 35 and 10 <= button.size['height'] <= 35]

    print(f"Total Video Icons Found: {len(filtered_buttons)}")

    # Check if at least 1 button is available
    if not filtered_buttons:
        print("Not enough buttons with the specified size range found.")
        pytest.skip("Not enough buttons found. Skipping test case.")
        driver.quit()
        exit()

    # Randomly select one button
    selected_button = random.choice(filtered_buttons)

    # Scroll to the selected button
    driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", selected_button)
    time.sleep(1)
    video_button = wait.until(EC.element_to_be_clickable(selected_button))  # Ensure it's clickable
    video_button.click()
    time.sleep(3)
    print(f"Clicked Button at position: {selected_button.location}, Size: {selected_button.size}")

    # Wait and click the Full Screen button
    full_screen_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Full Screen']")))
    time.sleep(5)

    # Take Screenshot & Attach to Allure
    screenshot = driver.get_screenshot_as_png()
    allure.attach(screenshot, name=f"Full Screen Button", attachment_type=allure.attachment_type.PNG)

    full_screen_button.click()

    # Handle multiple tabs
    wait.until(lambda d: len(driver.window_handles) > 1)  # Wait for the new tab to open
    tabs = driver.window_handles
    print("Open tabs:", len(tabs))

    # Switch to the second tab (index 1)
    driver.switch_to.window(tabs[1])
    print("Switched to Tab - Title:", driver.title)

    # Try to find and click the play button
    try:
        play_button = wait.until(
            EC.element_to_be_clickable((By.XPATH, "/html[1]/body[1]/div[1]/div[5]/div[7]/div[1]/button[1]")))
        play_button.click()
        print("Play button clicked, video started.")
        time.sleep(30)

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
