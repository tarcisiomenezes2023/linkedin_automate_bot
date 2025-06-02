# Essential for automation:
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
# This will make it wait expected conditions to start other functions
from selenium.webdriver.support import expected_conditions as EC
# Avoiding anti-bot system detection
import undetected_chromedriver as uc
# for delay and sleep
import time
# for human-like behavior
import random
# for file managing paths, web etc
import os
# To show what the BOT is doing
import logging
# To find key words on the web browser
import re
# to find real time jobs based on date release
import datetime
# (Optional) for reading data from CSV file
import pandas as pd

# Chromedriver undetection from anti-bot system
import undetected_chromedriver as uc
options = uc.ChromeOptions()
driver = uc.Chrome(options=options)

# Go to LinkedIn login page
driver.get("https://www.linkedin.com/feed/")

# Wait for email input to appear
wait = WebDriverWait(driver, 10)
email_input = wait.until(EC.presence_of_element_located((By.ID, "username")))
password_input = driver.find_element(By.ID, "password")

# Enter credentials
email_input.send_keys(EMAIL)
password_input.send_keys(PASSWORD)

# Click "Sign in"
sign_in_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
sign_in_button.click()

# Optionally wait for homepage to load
wait.until(EC.presence_of_element_located((By.ID, "global-nav-search")))

print("✅ Login successful")

# Close or continue  
# driver.quit()    