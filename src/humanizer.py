import random
import time
import numpy as np
import pyautogui
import math
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from src.utils.logger import logger
from config.settings import Config

class Humanizer:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)
        
    def random_delay(self, min_sec=None, max_sec=None):
        """Human-like delay using normal distribution"""
        min_sec = Config.MIN_DELAY if min_sec is None else min_sec
        max_sec = Config.MAX_DELAY if max_sec is None else max_sec
        
        mean = (min_sec + max_sec) / 2
        std_dev = (max_sec - min_sec) / 6
        delay = abs(np.random.normal(mean, std_dev))
        sleep_time = max(min_sec, min(max_sec, delay))
        time.sleep(sleep_time)
        
    def human_type(self, element, text):
        """Type like a human with occasional mistakes"""
        self.random_delay(0.5, 1.5)
        self.move_mouse_to_element(element)
        element.click()
        self.random_delay(0.2, 0.5)
        
        for i, char in enumerate(text):
            if random.random() < Config.TYPO_CHANCE and i > 2:
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                element.send_keys(wrong_char)
                self.random_delay(0.1, 0.3)
                element.send_keys(Keys.BACKSPACE)
                self.random_delay(0.1, 0.2)
            
            element.send_keys(char)
            self.random_delay(0.05, 0.3)
            
    def human_click(self, element, highlight=True):
        """Human-like click with visual feedback"""
        try:
            self.move_mouse_to_element(element)
            
            if highlight and random.random() < 0.3:
                self.highlight_element(element)
                
            if random.random() < 0.2:
                self.random_delay(0.2, 0.5)
                self.move_mouse_away(element)
                self.random_delay(0.1, 0.3)
                self.move_mouse_to_element(element)
                
            self.random_delay(0.1, 0.3)
            element.click()
            
        except Exception as e:
            logger.error(f"Click failed: {str(e)}")
            raise
            
    def highlight_element(self, element, duration=0.3):
        """Visual feedback by highlighting element"""
        original_style = element.get_attribute("style")
        self.driver.execute_script(
            "arguments[0].style.border='2px solid red';"
            "arguments[0].style.transition='all 0.3s ease';",
            element
        )
        time.sleep(duration)
        self.driver.execute_script(
            f"arguments[0].setAttribute('style', '{original_style}');",
            element
        )
        
    def move_mouse_to_element(self, element, retries=3):
        """Smooth curved mouse movement to element"""
        for attempt in range(retries):
            try:
                loc = element.location_once_scrolled_into_view
                elem_x = loc['x'] + random.randint(5, 15)
                elem_y = loc['y'] + random.randint(5, 15)
                
                start_x, start_y = pyautogui.position()
                
                # Bezier curve control points
                cp1_x = start_x + (elem_x - start_x)*0.3 + random.randint(-50, 50)
                cp1_y = start_y + (elem_y - start_y)*0.3 + random.randint(-50, 50)
                cp2_x = start_x + (elem_x - start_x)*0.7 + random.randint(-50, 50)
                cp2_y = start_y + (elem_y - start_y)*0.7 + random.randint(-50, 50)
                
                # Generate curve points
                points = []
                for t in np.linspace(0, 1, Config.MOUSE_MOVE_POINTS):
                    x = (1-t)**3*start_x + 3*(1-t)**2*t*cp1_x + 3*(1-t)*t**2*cp2_x + t**3*elem_x
                    y = (1-t)**3*start_y + 3*(1-t)**2*t*cp1_y + 3*(1-t)*t**2*cp2_y + t**3*elem_y
                    points.append((x, y))
                
                # Move through points
                for point in points:
                    pyautogui.moveTo(point[0], point[1], duration=0.0001)
                    time.sleep(random.uniform(0.001, 0.003))
                return
                
            except MoveTargetOutOfBoundsException:
                if attempt == retries - 1:
                    raise
                self.driver.execute_script("arguments[0].scrollIntoView()", element)
                continue
                
    def move_mouse_away(self, element):
        """Move mouse randomly away from element"""
        loc = element.location_once_scrolled_into_view
        elem_x, elem_y = loc['x'], loc['y']
        screen_w, screen_h = pyautogui.size()
        
        target_x = random.randint(0, screen_w)
        target_y = random.randint(0, screen_h)
        
        while math.sqrt((target_x-elem_x)**2 + (target_y-elem_y)**2) < 200:
            target_x = random.randint(0, screen_w)
            target_y = random.randint(0, screen_h)
            
        self.move_mouse_to_point(target_x, target_y)
        
    def move_mouse_to_point(self, x, y):
        """Move mouse to specific coordinates"""
        start_x, start_y = pyautogui.position()
        distance = math.sqrt((x-start_x)**2 + (y-start_y)**2)
        duration = max(0.1, min(1.0, distance / 1000))
        pyautogui.moveTo(x, y, duration=duration)