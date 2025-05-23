# Job Search and Filter
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from humanizer import Humanizer
import time
import random

class JobFilters:
    def __init__(self, driver):
        self.driver = driver
        self.humanizer = Humanizer(driver)
        self.wait = WebDriverWait(driver, 15)
        
    def search_jobs(self, keywords, location="Budapest", experience_level=["Internship", "Entry level"]):
        # Navigate to jobs page
        self.driver.get("https://www.linkedin.com/jobs")
        self.humanizer.random_delay(3, 5)
        
        # Search keywords
        search_keywords = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@id, 'jobs-search-box-keyword')]"))
        )
        self.humanizer.human_type(search_keywords, keywords)
        self.humanizer.random_delay(1, 2)
        
        # Search location
        search_location = self.wait.until(EC.presence_of_element_located(
            (By.XPATH, "//input[contains(@id, 'jobs-search-box-location')]"))
        )
        search_location.clear()
        self.humanizer.random_delay(1, 2)
        self.humanizer.human_type(search_location, location)
        self.humanizer.random_delay(1, 2)
        search_location.send_keys(Keys.RETURN)
        
        # Apply experience filters
        self.apply_experience_filter(experience_level)
        
        # Get all job listings
        return self.get_job_listings()
    
    def apply_experience_filter(self, experience_levels):
        try:
            # Click on experience filter button
            exp_filter = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@aria-label, 'Experience level filter')]"))
            self.humanizer.human_click(exp_filter)
            self.humanizer.random_delay(1, 2)
            
            # Select desired experience levels
            for level in experience_levels:
                checkbox = self.wait.until(EC.element_to_be_clickable(
                    (By.XPATH, f"//label[contains(@for, 'experience-{level.lower().replace(' ', '-')}')]")))
                self.humanizer.human_click(checkbox)
                self.humanizer.random_delay(0.5, 1)
            
            # Apply filters
            apply_button = self.wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@aria-label, 'Apply current filters')]")))
            self.humanizer.human_click(apply_button)
            self.humanizer.random_delay(2, 4)
            
        except Exception as e:
            print(f"Could not apply experience filter: {str(e)}")
    
    def get_job_listings(self):
        self.humanizer.random_delay(3, 5)
        
        # Scroll to load more jobs
        for _ in range(3):
            self.humanizer.random_scroll()
        
        # Get all job cards
        job_cards = self.wait.until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[contains(@class, 'jobs-search-results-list')]//li")))
        
        jobs = []
        for card in job_cards:
            try:
                # Extract job details
                title_elem = card.find_element(By.XPATH, ".//a[contains(@class, 'job-card-list__title')]")
                company_elem = card.find_element(By.XPATH, ".//span[contains(@class, 'job-card-container__primary-description')]")
                location_elem = card.find_element(By.XPATH, ".//li[contains(@class, 'job-card-container__metadata-item')]")
                link = title_elem.get_attribute('href')
                
                jobs.append({
                    'title': title_elem.text.strip(),
                    'company': company_elem.text.strip(),
                    'location': location_elem.text.strip(),
                    'link': link,
                    'element': card
                })
            except:
                continue
                
        return jobs
            
            