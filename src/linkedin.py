# LinkedIn Login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from humanizer import Humanizer
import time
import random
from dotenv import load_dotenv
import os

load_dotenv('../config/credentials.env')

class LinkedIn:
    def __init__(self, driver):
        self.driver = driver
        self.humanizer = Humanizer(driver)
        self.wait = WebDriverWait(driver, 10)
        
    def login(self):
        self.driver.get("https://www.linkedin.com/login")
        self.humanizer.random_delay(2, 4)
        
        # Fill email
        email = self.wait.until(EC.presence_of_element_located((By.ID, "username")))
        self.humanizer.human_type(email, os.getenv('LINKEDIN_EMAIL'))
        
        # Fill password
        password = self.wait.until(EC.presence_of_element_located((By.ID, "password")))
        self.humanizer.human_type(password, os.getenv('LINKEDIN_PASSWORD'))
        
        # Click login with human-like delay
        self.humanizer.random_delay(1, 2)
        login_button = self.wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']")))
        self.humanizer.human_click(login_button)
        
        # Verify login success
        self.humanizer.random_delay(3, 5)
        if "feed" not in self.driver.current_url:
            raise Exception("Login failed")