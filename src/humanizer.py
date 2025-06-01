# Human-like Behavior
import random
import time
import numpy as np
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyautogui
import math

class Humanizer:
    def __init__(self, driver):
        self.driver = driver
        self.actions = ActionChains(driver)
        
    def random_delay(self, min_sec=1, max_sec=3):
        """More natural delay using normal distribution"""
        mean = (min_sec + max_sec) / 2
        std_dev = (max_sec - min_sec) / 6
        delay = abs(np.random.normal(mean, std_dev))
        time.sleep(max(min_sec, min(max_sec, delay)))
        
    def human_type(self, element, text):
        """More realistic typing with occasional mistakes"""
        self.random_delay(0.5, 1.5)
        self.move_mouse_to_element(element)
        element.click()
        self.random_delay(0.2, 0.5)
        
        for i, char in enumerate(text):
            # Occasionally make a typo and correct it
            if random.random() < 0.03 and i > 2:  # 3% chance of typo
                wrong_char = random.choice('abcdefghijklmnopqrstuvwxyz')
                element.send_keys(wrong_char)
                time.sleep(random.uniform(0.1, 0.3))
                element.send_keys(Keys.BACKSPACE)
                time.sleep(random.uniform(0.1, 0.2))
            
            element.send_keys(char)
            # Vary typing speed
            time.sleep(random.uniform(0.05, 0.3))
            
    def human_click(self, element):
        """More human-like click with curved mouse movement"""
        self.move_mouse_to_element(element)
        
        # Sometimes move away and come back
        if random.random() < 0.2:  # 20% chance
            self.random_delay(0.2, 0.5)
            self.move_mouse_away(element)
            self.random_delay(0.1, 0.3)
            self.move_mouse_to_element(element)
        
        # Random click duration
        self.random_delay(0.1, 0.3)
        element.click()
        
    def move_mouse_to_element(self, element):
        """Curved mouse movement using Bezier curve"""
        loc = element.location_once_scrolled_into_view
        elem_x = loc['x'] + random.randint(5, 15)
        elem_y = loc['y'] + random.randint(5, 15)
        
        # Get current mouse position
        start_x, start_y = pyautogui.position()
        
        # Control points for Bezier curve
        cp1_x = start_x + (elem_x - start_x) * 0.3 + random.randint(-50, 50)
        cp1_y = start_y + (elem_y - start_y) * 0.3 + random.randint(-50, 50)
        cp2_x = start_x + (elem_x - start_x) * 0.7 + random.randint(-50, 50)
        cp2_y = start_y + (elem_y - start_y) * 0.7 + random.randint(-50, 50)
        
        # Generate curve points
        points = []
        for t in np.linspace(0, 1, 30):
            x = (1-t)**3 * start_x + 3*(1-t)**2*t*cp1_x + 3*(1-t)*t**2*cp2_x + t**3*elem_x
            y = (1-t)**3 * start_y + 3*(1-t)**2*t*cp1_y + 3*(1-t)*t**2*cp2_y + t**3*elem_y
            points.append((x, y))
        
        # Move through the points
        for point in points:
            pyautogui.moveTo(point[0], point[1], duration=0.0001)
            time.sleep(random.uniform(0.001, 0.003))
        
    def move_mouse_away(self, element):
        """Move mouse randomly away from element"""
        loc = element.location_once_scrolled_into_view
        elem_x = loc['x']
        elem_y = loc['y']
        
        # Move to random position on screen
        screen_width, screen_height = pyautogui.size()
        target_x = random.randint(0, screen_width)
        target_y = random.randint(0, screen_height)
        
        # Avoid moving too close to the element
        while math.sqrt((target_x - elem_x)**2 + (target_y - elem_y)**2) < 200:
            target_x = random.randint(0, screen_width)
            target_y = random.randint(0, screen_height)
            
        self.move_mouse_to_point(target_x, target_y)