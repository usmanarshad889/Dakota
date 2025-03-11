import time
import random
import pytest
from faker import Faker
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Chrome()
driver.maximize_window()
driver.implicitly_wait(10)

wait = WebDriverWait(driver, 20)


driver.get("https://mail.google.com/mail/u/0/#inbox")

email_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@id='identifierId']")))
email_field.send_keys("usman.arshad@rolustech.com")

next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Next']")))
next_btn.click()

password_field = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='Passwd']")))
password_field.send_keys("test")

next_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[normalize-space()='Next']")))
next_btn.click()
time.sleep(20)


# Wait for Gmail Inbox to Load
wait.until(EC.presence_of_element_located((By.XPATH, "//table[@role='grid']")))

# Locate the Gmail Search Box
search_box = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@aria-label='Search mail']")))

# Type Email Search Query (Modify as Needed)
search_box.send_keys("from:SF Development")  # Modify email search criteria
search_box.send_keys(Keys.ENTER)

# Wait for Search Results to Load
time.sleep(5)  # Adjust sleep time as needed

# Capture Search Results
emails = driver.find_elements(By.XPATH, "(//td[@class='oZ-x3 xY'])")

print(f"Total Emails Found: {len(emails)}")

# Close Browser
driver.quit()