"""
Login page object model
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class LoginPage(BasePage):
    # URLs
    LOGIN_URL = "/index.php?route=account/login"
    ACCOUNT_URL = "/index.php?route=account/account"
    
    # Login elements
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    
    # Account elements
    MY_ACCOUNT_DROPDOWN = (By.CSS_SELECTOR, "a[title='My Account']")
    LOGIN_LINK = (By.CSS_SELECTOR, "a[href*='account/login']")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href*='account/logout']")
    
    # Error messages
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    
    def navigate_to_login(self):
        """Navigate to login page"""
        url = self.config.BASE_URL + self.LOGIN_URL
        self.open_url(url)
        return self.take_screenshot("login_page_loaded")
    
    def login(self, email, password):
        """Login with credentials"""
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        time.sleep(2)
        return self.take_screenshot("login_attempted")
    
    def is_logged_in(self):
        """Check if user is logged in"""
        return self.is_element_present(self.LOGOUT_LINK)
    
    def logout(self):
        """Logout user"""
        if self.is_element_present(self.MY_ACCOUNT_DROPDOWN):
            self.click_element(self.MY_ACCOUNT_DROPDOWN)
            time.sleep(1)
        
        if self.is_element_present(self.LOGOUT_LINK):
            self.click_element(self.LOGOUT_LINK)
            time.sleep(2)
            return self.take_screenshot("user_logged_out")
        return None
    
    def get_error_message(self):
        """Get login error message"""
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None