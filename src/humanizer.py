# Human-like Behavior
import random
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui

class Humanizer:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)
        
    def random_delay(self, min_sec=1, max_sec=5):
        time.sleep(random.uniform(min_sec, max_sec))
        
    def human_type(self, element, text):
        self.random_delay(0.5, 3)
        element.click()
        self.random_delay(0.2, 1.5)
        
        for char in text:
            element.send_keys(char)
            time.sleep(random.uniform(0.05, 0.2))
            
    def human_click(self, element):
        # Move mouse human-like
        self.move_mouse_to_element(element)
        self.random_delay(0.3, 3.5)
        element.click()
        
    def move_mouse_to_element(self, element):
        # Get element position
        loc = element.location_once_scrolled_into_view
        x = loc['x'] + random.randint(5, 15)
        y = loc['y'] + random.randint(5, 15)
        
        # Move mouse gradually
        pyautogui.moveTo(x, y, duration=random.uniform(0.3, 0.7))
        
    def random_scroll(self):
        scroll_amount = random.randint(200, 800)
        if random.random() > 0.5:
            self.driver.execute_script(f"window.scrollBy(0, {scroll_amount})")
        else:
            self.actions.send_keys(Keys.PAGE_DOWN).perform()
        self.random_delay(1, 2)