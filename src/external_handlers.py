from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from humanizer import Humanizer
import time
import random
import pytesseract
from PIL import Image
import io
import os

class ExternalHandlers:
    def __init__(self, driver):
        self.driver = driver
        self.humanizer = Humanizer(driver)
        self.wait = WebDriverWait(driver, 15)
        
    def detect_application_platform(self):
        """Identify which application platform is being used"""
        current_url = self.driver.current_url
        
        # Check for Greenhouse
        if 'greenhouse.io' in current_url:
            return 'greenhouse'
        # Check for Lever
        elif 'lever.co' in current_url:
            return 'lever'
        # Check for Workday
        elif 'workday.com' in current_url:
            return 'workday'
        else:
            return 'unknown'
    
    def handle_platform(self, platform):
        """Route to specific platform handler"""
        if platform == 'greenhouse':
            return self.handle_greenhouse()
        elif platform == 'lever':
            return self.handle_lever()
        elif platform == 'workday':
            return self.handle_workday()
        else:
            return self.handle_unknown()
    
    def handle_greenhouse(self):
        """Greenhouse-specific application handler"""
        print("Handling Greenhouse application")
        try:
            # Fill basic information
            self.humanizer.random_delay(2, 4)
            
            # Handle file uploads
            resume_input = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//input[@type='file']")))
            resume_path = os.path.abspath("../data/profiles/resume.pdf")
            resume_input.send_keys(resume_path)
            self.humanizer.random_delay(3, 5)
            
            # Fill other fields
            self.fill_fields_by_label('First Name', 'John')
            self.fill_fields_by_label('Last Name', 'Doe')
            self.fill_fields_by_label('Email', 'john.doe@example.com')
            self.fill_fields_by_label('Phone', '1234567890')
            
            # Handle CAPTCHA if present
            if self.is_captcha_present():
                self.solve_captcha()
                
            # Submit application
            submit_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(text(), 'Submit Application')]")))
            self.humanizer.human_click(submit_button)
            self.humanizer.random_delay(5, 8)
            
            return True
        except Exception as e:
            print(f"Error handling Greenhouse: {str(e)}")
            return False
    
    def solve_captcha(self):
        """Basic CAPTCHA solving using Tesseract OCR"""
        try:
            # Find CAPTCHA image
            captcha_img = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, "//img[contains(@src, 'captcha')]")))
            
            # Take screenshot of CAPTCHA
            img_binary = captcha_img.screenshot_as_png
            img = Image.open(io.BytesIO(img_binary))
            
            # Preprocess image for better OCR
            img = img.convert('L')  # Grayscale
            img = img.point(lambda x: 0 if x < 128 else 255)  # Threshold
            
            # Use Tesseract to read CAPTCHA
            captcha_text = pytesseract.image_to_string(img).strip()
            
            # Find input field and enter CAPTCHA
            captcha_input = self.driver.find_element(By.XPATH,
                "//input[contains(@id, 'captcha')]")
            self.humanizer.human_type(captcha_input, captcha_text)
            
            return True
        except Exception as e:
            print(f"Failed to solve CAPTCHA: {str(e)}")
            return False
    
    def is_captcha_present(self):
        """Check if CAPTCHA is present on page"""
        return len(self.driver.find_elements(By.XPATH,
            "//img[contains(@src, 'captcha')]")) > 0
    
    def fill_fields_by_label(self, label_text, value):
        """Find field by label text and fill it"""
        try:
            label = self.wait.until(EC.presence_of_element_located(
                (By.XPATH, f"//label[contains(., '{label_text}')]")))
            field_id = label.get_attribute('for')
            if field_id:
                field = self.driver.find_element(By.ID, field_id)
                self.humanizer.human_type(field, value)
            else:
                # Try to find adjacent input
                field = label.find_element(By.XPATH, 
                    "./following-sibling::input[1]")
                self.humanizer.human_type(field, value)
        except:
            print(f"Could not find field for label: {label_text}")