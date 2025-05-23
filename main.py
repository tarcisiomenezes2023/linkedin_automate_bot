# Main Application
from src.browser import create_browser_instance
from src.linkedin import LinkedIn
from src.filters import JobFilters
from src.application import ApplicationSystem
import time
import random

def main():
    # Initialize browser with human-like settings
    driver = create_browser_instance(headless=False)  # Set to True for production
    
    try:
        # Login to LinkedIn
        linkedin = LinkedIn(driver)
        linkedin.login()
        
        # Initialize job search and application system
        job_filters = JobFilters(driver)
        app_system = ApplicationSystem(driver)
        
        # Define your search criteria
        keywords = "python OR excel OR frontend"
        location = "Budapest"
        experience_levels = ["Internship", "Entry level"]
        
        # Search for jobs
        jobs = job_filters.search_jobs(keywords, location, experience_levels)
        print(f"Found {len(jobs)} matching jobs")
        
        # Apply to jobs
        for job in jobs:
            try:
                app_system.apply_to_job(job)
                # Random delay between applications
                time.sleep(random.randint(10, 30))
            except Exception as e:
                print(f"Error applying to job: {str(e)}")
                continue
                
    except Exception as e:
        print(f"Fatal error: {str(e)}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()