"""
Base page class with common functionality
"""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import os
from config.config import TestConfig

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, TestConfig.EXPLICIT_WAIT)
        self.config = TestConfig()
    
    def open_url(self, url):
        """Navigate to specified URL"""
        self.driver.get(url)
        time.sleep(2)
    
    def find_element(self, locator):
        """Find element with explicit wait"""
        try:
            return self.wait.until(EC.presence_of_element_located(locator))
        except TimeoutException:
            raise Exception(f"Element not found: {locator}")
    
    def find_elements(self, locator):
        """Find multiple elements"""
        try:
            return self.wait.until(EC.presence_of_all_elements_located(locator))
        except TimeoutException:
            return []
    
    def click_element(self, locator):
        """Click element with wait"""
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        time.sleep(1)
    
    def enter_text(self, locator, text):
        """Enter text in input field"""
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
    
    def get_text(self, locator):
        """Get text from element"""
        element = self.find_element(locator)
        return element.text
    
    def is_element_present(self, locator, timeout=5):
        """Check if element is present"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True
        except TimeoutException:
            return False
    
    def take_screenshot(self, name):
        """Take screenshot for test evidence"""
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(self.config.get_screenshot_dir(), filename)
        self.driver.save_screenshot(filepath)
        return filepath
    
    def scroll_to_element(self, locator):
        """Scroll to element"""
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].scrollIntoView();", element)
        time.sleep(1)