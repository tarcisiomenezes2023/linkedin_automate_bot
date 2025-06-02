import os
import time
import random
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.common.by import By

# Load credentials
load_dotenv()
username = os.getenv("LINKEDIN_EMAIL")
password = os.getenv("LINKEDIN_PASSWORD")

# Initialize web browser with real profile to get cookies 
# and avoid receving automate msg from linkedin to remember password
driver = webdriver.Chrome()
driver.maximize_window()
driver.get("https://www.linkedin.com/login/")

# Wait some seconds like a human
time.sleep(random.uniform(2.0, 8.0))

# Find elements to touch
username_field = driver.find_element(By.ID, "username")
password_field = driver.find_element(By.ID, "password")

# Simulate human-typing
for char in username:
    username_field.send_keys(char)
    time.sleep(random.uniform(0.05, 0.15))

time.sleep(random.uniform(1.0, 2.0))

# password typing
for char in password:
    password_field.send_keys(char)
    time.sleep(random.uniform(0.05, 0.15))

time.sleep(random.uniform(1.0, 2.0))

# Find button and click
sign_in_button = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Sign in"]')
sign_in_button.click()

# Wait and scroll the page like a human
time.sleep(random.uniform(5.0, 7.0))
driver.execute_script("window.scrollTo(0, 500);")
time.sleep(random.uniform(1.5, 3.0))

print("✅ SUCCESS!")
