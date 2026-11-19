"""
Test configuration settings for e-commerce automation testing
"""
import os
from dataclasses import dataclass

@dataclass
class TestConfig:
    # Base URL for the e-commerce website
    BASE_URL: str = "https://ecommerce-playground.lambdatest.io"
    
    # Browser settings
    BROWSER: str = os.getenv("BROWSER", "safari")  # Back to safari as default
    IMPLICIT_WAIT: int = 10
    EXPLICIT_WAIT: int = 20
    
    # Test environment
    HEADLESS: bool = os.getenv("HEADLESS", "false").lower() == "true"
    WINDOW_SIZE: tuple = (1920, 1080)
    
    # Paths
    SCREENSHOT_PATH: str = "screenshots"
    REPORT_PATH: str = "reports"
    
    # Test data
    TEST_EMAIL: str = "testuser@example.com"
    TEST_PASSWORD: str = "Test123!"
    
    @classmethod
    def get_screenshot_dir(cls):
        if not os.path.exists(cls.SCREENSHOT_PATH):
            os.makedirs(cls.SCREENSHOT_PATH)
        return cls.SCREENSHOT_PATH
    
    @classmethod
    def get_report_dir(cls):
        if not os.path.exists(cls.REPORT_PATH):
            os.makedirs(cls.REPORT_PATH)
        return cls.REPORT_PATH
    
    @classmethod
    def ensure_directories_exist(cls):
        """Ensure all required directories exist"""
        cls.get_screenshot_dir()
        cls.get_report_dir()