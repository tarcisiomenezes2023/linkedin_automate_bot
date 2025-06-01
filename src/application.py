# Application System
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from humanizer import Humanizer
from selenium.common.exceptions import (NoSuchElementException, 
                                      TimeoutException,
                                      ElementClickInterceptedException,
                                      StaleElementReferenceException)
import logging
import time
import random
import pandas as pd
import os

class ApplicationSystem:
    def __init__(self, driver):
        self.driver = driver
        self.humanizer = Humanizer(driver)
        self.wait = WebDriverWait(driver, 15)
        self.applied_jobs = self.load_applied_jobs()
        
    def load_applied_jobs(self):
        if os.path.exists('../data/applications.csv'):
            return pd.read_csv('../data/applications.csv')['job_link'].tolist()
        return []
    
    def save_application(self, job_info):
        new_entry = pd.DataFrame([{
            'timestamp': pd.Timestamp.now(),
            'job_title': job_info['title'],
            'company': job_info['company'],
            'location': job_info['location'],
            'job_link': job_info['link'],
            'status': 'applied'
        }])
        
        if os.path.exists('../data/applications.csv'):
            df = pd.read_csv('../data/applications.csv')
            df = pd.concat([df, new_entry], ignore_index=True)
        else:
            df = new_entry
            
        df.to_csv('../data/applications.csv', index=False)
        self.applied_jobs.append(job_info['link'])
    
    def apply_to_job(self, job_info):
        if job_info['link'] in self.applied_jobs:
            print(f"Already applied to {job_info['title']} at {job_info['company']}")
            return False
        
        print(f"Attempting to apply to {job_info['title']} at {job_info['company']}")
        
        # Open job in new tab
        self.driver.execute_script(f"window.open('{job_info['link']}');")
        self.driver.switch_to.window(self.driver.window_handles[-1])
        self.humanizer.random_delay(3, 5)
        
        try:
            # Check if Easy Apply is available
            easy_apply_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")))
            
            if easy_apply_button:
                self.process_easy_apply(job_info)
            else:
                self.process_external_application(job_info)
                
        except Exception as e:
            print(f"Failed to apply to {job_info['title']}: {str(e)}")
            return False
        finally:
            # Close the tab and switch back
            self.driver.close()
            self.driver.switch_to.window(self.driver.window_handles[0])
            self.humanizer.random_delay(2, 4)
            
        return True
    
    def process_easy_apply(self, job_info):
        # Click Easy Apply button
        easy_apply_button = self.wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'jobs-apply-button')]")))
        self.humanizer.human_click(easy_apply_button)
        self.humanizer.random_delay(2, 3)
        
        # Process multi-page application form
        while True:
            try:
                # Check if submit application button is present
                submit_button = self.driver.find_elements(By.XPATH, 
                    "//button[contains(@aria-label, 'Submit application')]")
                
                if submit_button:
                    self.humanizer.random_delay(1, 2)
                    self.humanizer.human_click(submit_button[0])
                    self.humanizer.random_delay(2, 3)
                    break
                
                # Fill form fields (simplified - you'll need to expand this)
                self.fill_form_fields()
                
                # Click next button
                next_button = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(@aria-label, 'Continue to next step')]")))
                self.humanizer.human_click(next_button)
                self.humanizer.random_delay(2, 3)
                
            except Exception as e:
                print(f"Error in Easy Apply process: {str(e)}")
                # Close application
                discard_button = self.driver.find_element(By.XPATH, 
                    "//button[contains(@data-test-modal-close-btn, 'true')]")
                if discard_button:
                    self.humanizer.human_click(discard_button)
                    self.humanizer.random_delay(1, 2)
                    confirm_discard = self.driver.find_element(By.XPATH,
                        "//button[contains(@data-test-dialog-primary-btn, 'true')]")
                    if confirm_discard:
                        self.humanizer.human_click(confirm_discard)
                raise e
        
        # Verify application was successful
        self.humanizer.random_delay(3, 5)
        success_element = self.driver.find_elements(By.XPATH,
            "//div[contains(@class, 'artdeco-toast-item') and contains(., 'submitted')]")
        
        if success_element:
            self.save_application(job_info)
            print(f"Successfully applied to {job_info['title']} at {job_info['company']}")
        else:
            raise Exception("Application submission not confirmed")
    
    def fill_form_fields(self):
        # This is a simplified version - you'll need to expand it based on your profile data
        try:
            # Handle phone number field if present
            phone_field = self.driver.find_elements(By.XPATH,
                "//input[contains(@id, 'phoneNumber')]")
            if phone_field and not phone_field[0].get_attribute('value'):
                self.humanizer.human_type(phone_field[0], "1234567890")
                self.humanizer.random_delay(1, 2)
                
            # Handle resume selection if needed
            resume_select = self.driver.find_elements(By.XPATH,
                "//div[contains(@class, 'jobs-document-upload')]//input")
            if resume_select:
                # Upload your resume file
                resume_path = os.path.abspath("../data/profiles/resume.pdf")
                resume_select[0].send_keys(resume_path)
                self.humanizer.random_delay(3, 5)
                
        except Exception as e:
            print(f"Error filling form: {str(e)}")
            raise
    
    def process_external_application(self, job_info):
        print(f"Processing external application for {job_info['title']}")
        # This would involve:
        # 1. Clicking the "Apply" button that redirects to company site
        # 2. Switching to the new window/tab
        # 3. Automating the external application form
        # 4. Handling various website designs
        
        # Implementation would be similar to Easy Apply but more complex
        # You might need to create website-specific handlers for common platforms
        
        # For now, just mark as applied
        self.save_application(job_info)