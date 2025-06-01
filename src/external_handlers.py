import pytesseract
from PIL import Image
import io
import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.humanizer import Humanizer
from src.utils.logger import logger
from config.settings import Config
from pathlib import Path

class ExternalHandlers:
    def __init__(self, driver):
        self.driver = driver
        self.humanizer = Humanizer(driver)
        self.wait = WebDriverWait(driver, 15)
        
    def detect_application_platform(self):
        """Detect which application platform is being used"""
        current_url = self.driver.current_url.lower()
        
        if 'greenhouse' in current_url:
            return 'greenhouse'
        elif 'lever' in current_url:
            return 'lever'
        elif 'workday' in current_url:
            return 'workday'
        elif 'applytojob' in current_url:
            return 'applytojob'
        elif 'smartrecruiters' in current_url:
            return 'smartrecruiters'
        else:
            return 'unknown'
            
    def handle_platform(self, platform):
        """Route to appropriate platform handler"""
        handler_name = f"handle_{platform.lower()}"
        handler = getattr(self, handler_name, self.handle_unknown)
        return handler()
        
    def handle_greenhouse(self):
        """Handle Greenhouse application forms"""
        try:
            logger.info("Handling Greenhouse application")
            self.humanizer.random_delay(2, 4)
            
            # Resume upload
            resume_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@type='file']"))
            )
            resume_path = Config.PROFILES_DIR / 'resumes' / 'resume.pdf'
            resume_input.send_keys(str(resume_path))
            self.humanizer.random_delay(3, 5)
            
            # Fill basic info
            self.fill_field_by_label('First Name', 'John')
            self.fill_field_by_label('Last Name', 'Doe')
            self.fill_field_by_label('Email', 'john.doe@example.com')
            self.fill_field_by_label('Phone', self.generate_phone_number())
            
            # Handle CAPTCHA if present
            if self.is_captcha_present():
                self.solve_captcha()
                
            # Submit application
            submit_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Submit Application')]")
                )
            )
            self.humanizer.human_click(submit_btn)
            self.humanizer.random_delay(5, 8)
            
            return True
            
        except Exception as e:
            logger.error(f"Greenhouse handler failed: {str(e)}")
            return False
            
    def handle_lever(self):
        """Handle Lever.co application forms"""
        try:
            logger.info("Handling Lever application")
            self.humanizer.random_delay(2, 4)
            
            # Fill basic info
            self.fill_field_by_name('name', 'John Doe')
            self.fill_field_by_name('email', 'john.doe@example.com')
            self.fill_field_by_name('phone', self.generate_phone_number())
            
            # Resume upload
            resume_input = self.driver.find_element(
                By.XPATH, "//input[@type='file' and contains(@name, 'resume')]"
            )
            if resume_input:
                resume_path = Config.PROFILES_DIR / 'resumes' / 'resume.pdf'
                resume_input.send_keys(str(resume_path))
                self.humanizer.random_delay(3, 5)
                
            # Submit application
            submit_btn = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'Submit Application')]")
                )
            )
            self.humanizer.human_click(submit_btn)
            self.humanizer.random_delay(5, 8)
            
            return True
            
        except Exception as e:
            logger.error(f"Lever handler failed: {str(e)}")
            return False
            
    def handle_workday(self):
        """Handle Workday application forms (simplified)"""
        try:
            logger.info("Handling Workday application")
            self