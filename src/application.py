import os
import time
import random
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    ElementClickInterceptedException,
    StaleElementReferenceException
)
from src.humanizer import Humanizer
from src.external_handlers import ExternalHandlers
from src.utils.logger import logger
from src.utils.metrics import PerformanceTracker
from src.utils.exceptions import JobApplicationError
from config.settings import Config
from pathlib import Path

class ApplicationSystem:
    def __init__(self, driver):
        self.driver = driver
        self.humanizer = Humanizer(driver)
        self.wait = WebDriverWait(driver, 15)
        self.external_handler = ExternalHandlers(driver)
        self.applied_jobs = self.load_applied_jobs()
        self.tracker = PerformanceTracker()
        
    def load_applied_jobs(self):
        """Load previously applied jobs from CSV"""
        path = Config.DATA_DIR / 'applications.csv'
        if path.exists():
            try:
                df = pd.read_csv(path)
                return df['job_link'].tolist()
            except Exception as e:
                logger.warning(f"Failed to load applications: {str(e)}")
        return []
        
    def save_application(self, job_info):
        """Save application record to CSV"""
        try:
            path = Config.DATA_DIR / 'applications.csv'
            new_entry = pd.DataFrame([{
                'timestamp': pd.Timestamp.now(),
                'job_title': job_info['title'],
                'company': job_info['company'],
                'location': job_info['location'],
                'job_link': job_info['link'],
                'status': 'applied'
            }])
            
            if path.exists():
                df = pd.read_csv(path)
                df = pd.concat([df, new_entry], ignore_index=True)
            else:
                df = new_entry
                
            df.to_csv(path, index=False)
            self.applied_jobs.append(job_info['link'])
            logger.info(f"Saved application to {job_info['title']}")
            
        except Exception as e:
            logger.error(f"Failed to save application: {str(e)}")
            
    def apply_to_job(self, job_info, max_attempts=2):
        """Apply to a job with retry logic"""
        if job_info['link'] in self.applied_jobs:
            logger.info(f"Already applied to {job_info['title']}")
            return False
            
        logger.info(f"Attempting to apply to {job_info['title']}")
        
        for attempt in range(1, max_attempts + 1):
            try:
                # Open job in new tab
                self.driver.execute_script(f"window.open('{job_info['link']}');")
                self.driver.switch_to.window(self.driver.window_handles[-1])
                self.humanizer.random_delay(3, 5)
                
                # Check application method
                if self.is_easy_apply_available():
                    result = self.process_easy_apply(job_info)
                else:
                    result = self.process_external_application(job_info)
                
                if result:
                    self.tracker.record_success()
                    return True
                    
            except Exception as e:
                logger.error(f"Attempt {attempt} failed: {str(e)}")
                if attempt == max_attempts:
                    self.tracker.record_error()
                continue
                
            finally:
                # Cleanup
                self.close_current_tab()
                self.humanizer.random_delay(2, 4)
                
        return False
        
    def is_easy_apply_available(self):
        """Check if Easy Apply button exists"""
        try:
            return bool(self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")
                )
            ))
        except TimeoutException:
            return False
            
    def process_easy_apply(self, job_info):
        """Handle LinkedIn Easy Apply application"""
        try:
            logger.info("Processing Easy Apply")
            easy_apply_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")
                )
            )
            self.humanizer.human_click(easy_apply_button)
            self.humanizer.random_delay(2, 3)
            
            while True:
                # Check for submit button
                submit_buttons = self.driver.find_elements(
                    By.XPATH, "//button[contains(@aria-label, 'Submit application')]"
                )
                if submit_buttons:
                    self.humanizer.random_delay(1, 2)
                    self.humanizer.human_click(submit_buttons[0])
                    self.humanizer.random_delay(2, 3)
                    break
                    
                # Fill form fields
                self.fill_form_fields()
                
                # Click next/continue
                next_button = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, "//button[contains(@aria-label, 'Continue to next step')]")
                    )
                )
                self.humanizer.human_click(next_button)
                self.humanizer.random_delay(2, 3)
                
            # Verify success
            if self.is_application_submitted():
                self.save_application(job_info)
                logger.info(f"Successfully applied to {job_info['title']}")
                return True
            else:
                raise JobApplicationError("Application submission not confirmed")
                
        except Exception as e:
            logger.error(f"Easy Apply failed: {str(e)}")
            self.discard_application()
            raise
            
    def fill_form_fields(self):
        """Fill in application form fields"""
        try:
            # Phone number
            phone_fields = self.driver.find_elements(
                By.XPATH, "//input[contains(@id, 'phoneNumber')]"
            )
            for field in phone_fields:
                if not field.get_attribute('value'):
                    self.humanizer.human_type(field, self.generate_phone_number())
                    self.humanizer.random_delay(1, 2)
                    
            # Resume upload
            resume_inputs = self.driver.find_elements(
                By.XPATH, "//input[@type='file' and contains(@id, 'resume')]"
            )
            if resume_inputs:
                resume_path = Config.PROFILES_DIR / 'resumes' / 'resume.pdf'
                resume_inputs[0].send_keys(str(resume_path))
                self.humanizer.random_delay(3, 5)
                
        except Exception as e:
            logger.warning(f"Could not fill some form fields: {str(e)}")
            
    def generate_phone_number(self):
        """Generate random US phone number"""
        return f"1{random.randint(200, 999)}{random.randint(200, 999)}{random.randint(1000, 9999)}"
        
    def is_application_submitted(self):
        """Verify application was successfully submitted"""
        try:
            return bool(self.wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@class, 'artdeco-toast-item') and contains(., 'submitted')]")
                )
            ))
        except TimeoutException:
            return False
            
    def discard_application(self):
        """Discard incomplete application"""
        try:
            discard_btn = self.driver.find_element(
                By.XPATH, "//button[contains(@data-test-modal-close-btn, 'true')]"
            )
            if discard_btn:
                self.humanizer.human_click(discard_btn)
                self.humanizer.random_delay(1, 2)
                confirm_btn = self.driver.find_element(
                    By.XPATH, "//button[contains(@data-test-dialog-primary-btn, 'true')]"
                )
                if confirm_btn:
                    self.humanizer.human_click(confirm_btn)
        except Exception as e:
            logger.warning(f"Could not properly discard application: {str(e)}")
            
    def process_external_application(self, job_info):
        """Handle external application redirects"""
        try:
            logger.info("Processing external application")
            platform = self.external_handler.detect_application_platform()
            result = self.external_handler.handle_platform(platform)
            
            if result:
                self.save_application(job_info)
                return True
            return False
            
        except Exception as e:
            logger.error(f"External application failed: {str(e)}")
            raise
            
    def close_current_tab(self):
        """Close current tab and switch to main window"""
        if len(self.driver.window_handles) > 1:
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])