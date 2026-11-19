"""
WebDriver management utilities
"""
from selenium import webdriver
from selenium.webdriver.safari.service import Service as SafariService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from config.config import TestConfig
import os

class DriverManager:
    """Manages WebDriver instances for different browsers"""
    
    def __init__(self, config=None):
        self.config = config or TestConfig()
        self.driver = None
    
    def get_driver(self, browser=None):
        """Get WebDriver instance for specified browser"""
        browser = browser or self.config.BROWSER.lower()
        
        if browser == "safari":
            return self._get_safari_driver()
        elif browser == "chrome":
            return self._get_chrome_driver()
        elif browser == "firefox":
            return self._get_firefox_driver()
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    def _get_safari_driver(self):
        """Get Safari WebDriver (macOS only)"""
        try:
            driver = webdriver.Safari()
            self._configure_driver(driver)
            return driver
        except Exception as e:
            raise Exception(f"Failed to initialize Safari driver: {str(e)}")
    
    def _get_chrome_driver(self):
        """Get Chrome WebDriver"""
        try:
            options = ChromeOptions()
            if self.config.HEADLESS:
                options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--disable-gpu")
            options.add_argument("--disable-web-security")
            options.add_argument("--allow-running-insecure-content")
            options.add_argument(f"--window-size={self.config.WINDOW_SIZE[0]},{self.config.WINDOW_SIZE[1]}")
            
            service = ChromeService(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=options)
            self._configure_driver(driver)
            return driver
        except Exception as e:
            raise Exception(f"Failed to initialize Chrome driver: {str(e)}")
    
    def _get_firefox_driver(self):
        """Get Firefox WebDriver"""
        try:
            options = FirefoxOptions()
            if self.config.HEADLESS:
                options.add_argument("--headless")
            
            driver = webdriver.Firefox(options=options)
            self._configure_driver(driver)
            return driver
        except Exception as e:
            raise Exception(f"Failed to initialize Firefox driver: {str(e)}")
    
    def _configure_driver(self, driver):
        """Configure WebDriver with common settings"""
        driver.implicitly_wait(self.config.IMPLICIT_WAIT)
        if not self.config.HEADLESS:
            driver.maximize_window()
        
        # Set window size if specified
        if self.config.WINDOW_SIZE:
            driver.set_window_size(*self.config.WINDOW_SIZE)
    
    def quit_driver(self, driver):
        """Safely quit WebDriver"""
        if driver:
            try:
                driver.quit()
            except Exception as e:
                print(f"Error quitting driver: {str(e)}")

# Singleton instance for global use
driver_manager = DriverManager()