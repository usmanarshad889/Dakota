from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import subprocess

# Get Chrome version (Windows)
try:
    chrome_version = subprocess.check_output(
        ['C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe', '--version'],
        stderr=subprocess.STDOUT
    ).decode('utf-8').strip()
except FileNotFoundError:
    chrome_version = subprocess.check_output(
        ['C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe', '--version'],
        stderr=subprocess.STDOUT
    ).decode('utf-8').strip()

# Get ChromeDriver version
chromedriver_path = ChromeDriverManager().install()
chromedriver_version = subprocess.check_output([chromedriver_path, '--version']).decode('utf-8').strip()

# Setup driver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Print Chrome and ChromeDriver versions
print(f"Chrome Version: {chrome_version}")
print(f"ChromeDriver Version: {chromedriver_version}")

driver.get("https://www.google.co.uk/")

# Quit the driver
driver.quit()
