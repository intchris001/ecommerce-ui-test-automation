"""
Helper utilities for test automation
"""
import time
import os
import random
import string
from datetime import datetime
from config.config import TestConfig

class TestHelpers:
    """Collection of helper methods for test automation"""
    
    @staticmethod
    def generate_random_email():
        """Generate random email for testing"""
        random_string = ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
        return f"test_{random_string}@example.com"
    
    @staticmethod
    def generate_random_string(length=10):
        """Generate random string of specified length"""
        return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
    
    @staticmethod
    def get_timestamp():
        """Get current timestamp string"""
        return datetime.now().strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def wait_for_page_load(driver, timeout=10):
        """Wait for page to load completely"""
        start_time = time.time()
        while time.time() - start_time < timeout:
            if driver.execute_script("return document.readyState") == "complete":
                return True
            time.sleep(0.5)
        return False
    
    @staticmethod
    def scroll_to_bottom(driver):
        """Scroll to bottom of page"""
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
    
    @staticmethod
    def scroll_to_top(driver):
        """Scroll to top of page"""
        driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
    
    @staticmethod
    def create_directory_if_not_exists(directory_path):
        """Create directory if it doesn't exist"""
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)
            return True
        return False
    
    @staticmethod
    def clean_screenshot_directory():
        """Clean old screenshots from directory"""
        config = TestConfig()
        screenshot_dir = config.get_screenshot_dir()
        
        if os.path.exists(screenshot_dir):
            for filename in os.listdir(screenshot_dir):
                if filename.endswith('.png'):
                    file_path = os.path.join(screenshot_dir, filename)
                    # Remove files older than 24 hours
                    if os.path.getctime(file_path) < time.time() - 86400:
                        os.remove(file_path)
    
    @staticmethod
    def generate_test_data():
        """Generate test data for forms"""
        return {
            "first_name": f"Test{TestHelpers.generate_random_string(5)}",
            "last_name": f"User{TestHelpers.generate_random_string(5)}",
            "email": TestHelpers.generate_random_email(),
            "telephone": f"555{random.randint(1000000, 9999999)}",
            "address": f"{random.randint(100, 999)} Test Street",
            "city": "Test City",
            "postcode": f"{random.randint(10000, 99999)}",
            "password": "Test123!"
        }
    
    @staticmethod
    def generate_long_text(length=1000):
        """Generate long text for testing character limits"""
        words = ["test", "automation", "selenium", "python", "ecommerce", "website", "functionality"]
        text = ""
        while len(text) < length:
            text += random.choice(words) + " "
        return text[:length].strip()
    
    @staticmethod
    def validate_email_format(email):
        """Basic email format validation"""
        import re
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    @staticmethod
    def take_screenshot_with_timestamp(driver, name):
        """Take screenshot with timestamp"""
        config = TestConfig()
        timestamp = TestHelpers.get_timestamp()
        filename = f"{name}_{timestamp}.png"
        filepath = os.path.join(config.get_screenshot_dir(), filename)
        driver.save_screenshot(filepath)
        return filepath
    
    @staticmethod
    def log_test_step(step_number, description, status="PASS"):
        """Log test step with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] Step {step_number}: {description} - {status}")
    
    @staticmethod
    def wait_and_retry(func, max_attempts=3, delay=2):
        """Retry function execution with delay"""
        for attempt in range(max_attempts):
            try:
                return func()
            except Exception as e:
                if attempt == max_attempts - 1:
                    raise e
                time.sleep(delay)
        return None