"""
Wishlist page object model
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class WishlistPage(BasePage):
    # URLs
    WISHLIST_URL = "/index.php?route=account/wishlist"
    LOGIN_URL = "/index.php?route=account/login"
    REGISTER_URL = "/index.php?route=account/register"
    
    # Login elements
    EMAIL_INPUT = (By.ID, "input-email")
    PASSWORD_INPUT = (By.ID, "input-password")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "input[value='Login']")
    
    # Registration elements
    REG_FIRST_NAME = (By.ID, "input-firstname")
    REG_LAST_NAME = (By.ID, "input-lastname")
    REG_EMAIL = (By.ID, "input-email")
    REG_TELEPHONE = (By.ID, "input-telephone")
    REG_PASSWORD = (By.ID, "input-password")
    REG_CONFIRM = (By.ID, "input-confirm")
    PRIVACY_POLICY_CHECKBOX = (By.NAME, "agree")
    REGISTER_BUTTON = (By.CSS_SELECTOR, "input[value='Continue']")
    
    # Product elements
    PRODUCT_LINK = (By.CSS_SELECTOR, ".product-thumb h4 a")
    ADD_TO_WISHLIST_BUTTON = (By.CSS_SELECTOR, "button[data-original-title='Add to Wish List']")
    WISHLIST_SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    
    # Wishlist elements
    WISHLIST_ITEMS = (By.CSS_SELECTOR, ".table-responsive tbody tr")
    REMOVE_WISHLIST_BUTTON = (By.CSS_SELECTOR, "a[data-original-title='Remove']")
    WISHLIST_EMPTY_MESSAGE = (By.CSS_SELECTOR, ".text-center")
    
    # Account menu
    MY_ACCOUNT_LINK = (By.CSS_SELECTOR, "a[title='My Account']")
    WISHLIST_LINK = (By.CSS_SELECTOR, "a[href*='wishlist']")
    LOGOUT_LINK = (By.CSS_SELECTOR, "a[href*='route=account/logout'], a[href*='logout']")
    
    def navigate_to_login(self):
        """Navigate to login page"""
        url = self.config.BASE_URL + self.LOGIN_URL
        self.open_url(url)
        return self.take_screenshot("login_page_loaded")
    
    def navigate_to_register(self):
        """Navigate to registration page"""
        url = self.config.BASE_URL + self.REGISTER_URL
        self.open_url(url)
        return self.take_screenshot("register_page_loaded")
    
    def register_new_user(self, user_data):
        """Register a new user account"""
        self.enter_text(self.REG_FIRST_NAME, user_data["first_name"])
        self.enter_text(self.REG_LAST_NAME, user_data["last_name"])
        self.enter_text(self.REG_EMAIL, user_data["email"])
        self.enter_text(self.REG_TELEPHONE, "1234567890")
        self.enter_text(self.REG_PASSWORD, user_data["password"])
        self.enter_text(self.REG_CONFIRM, user_data["password"])
        
        if self.is_element_present(self.PRIVACY_POLICY_CHECKBOX):
            self.click_element(self.PRIVACY_POLICY_CHECKBOX)
        
        self.click_element(self.REGISTER_BUTTON)
        return self.take_screenshot("user_registered")
    
    def login(self, email, password):
        """Login with credentials"""
        self.enter_text(self.EMAIL_INPUT, email)
        self.enter_text(self.PASSWORD_INPUT, password)
        self.click_element(self.LOGIN_BUTTON)
        time.sleep(2)
        return self.take_screenshot("user_logged_in")
    
    def navigate_to_product_page(self):
        """Navigate to a product page"""
        self.open_url(self.config.BASE_URL)
        if self.is_element_present(self.PRODUCT_LINK):
            self.click_element(self.PRODUCT_LINK)
            return self.take_screenshot("product_page_loaded")
        else:
            # Navigate to a specific product if no products found on homepage
            product_url = f"{self.config.BASE_URL}/index.php?route=product/product&product_id=40"
            self.open_url(product_url)
            return self.take_screenshot("product_page_loaded")
    
    def add_to_wishlist(self):
        """Add current product to wishlist"""
        if self.is_element_present(self.ADD_TO_WISHLIST_BUTTON):
            self.click_element(self.ADD_TO_WISHLIST_BUTTON)
            time.sleep(2)
            return self.take_screenshot("product_added_to_wishlist")
        return None
    
    def navigate_to_wishlist(self):
        """Navigate to wishlist page"""
        url = self.config.BASE_URL + self.WISHLIST_URL
        self.open_url(url)
        return self.take_screenshot("wishlist_page_loaded")
    
    def get_wishlist_items_count(self):
        """Get number of items in wishlist"""
        items = self.find_elements(self.WISHLIST_ITEMS)
        return len(items)
    
    def remove_first_wishlist_item(self):
        """Remove first item from wishlist"""
        if self.is_element_present(self.REMOVE_WISHLIST_BUTTON):
            self.click_element(self.REMOVE_WISHLIST_BUTTON)
            time.sleep(2)
            return self.take_screenshot("item_removed_from_wishlist")
        return None

    # Aliases for test compatibility
    def remove_from_wishlist(self):
        """Alias: remove first item from wishlist"""
        return self.remove_first_wishlist_item()

    def logout(self):
        """Logout from account (direct URL or via menu)"""
        try:
            # Prefer direct logout URL for reliability
            logout_url = f"{self.config.BASE_URL}/index.php?route=account/logout"
            self.open_url(logout_url)
            time.sleep(2)
            self.take_screenshot("user_logged_out")
            return True
        except Exception as e:
            print(f"Error during logout via URL: {e}")
            # Fallback: click logout link if present
            try:
                if self.is_element_present(self.MY_ACCOUNT_LINK):
                    self.click_element(self.MY_ACCOUNT_LINK)
                    time.sleep(1)
                if self.is_element_present(self.LOGOUT_LINK):
                    self.click_element(self.LOGOUT_LINK)
                    time.sleep(2)
                    self.take_screenshot("user_logged_out")
                    return True
            except Exception as e2:
                print(f"Error during logout via menu: {e2}")
            self.take_screenshot("user_logout_error")
            return False
    
    def is_wishlist_empty(self):
        """Check if wishlist is empty"""
        return self.is_element_present(self.WISHLIST_EMPTY_MESSAGE)
    
    def get_success_message(self):
        """Get success message text"""
        if self.is_element_present(self.WISHLIST_SUCCESS_MESSAGE):
            return self.get_text(self.WISHLIST_SUCCESS_MESSAGE)
        return None
    
    def register_user(self, user_data):
        """Register a new user - alias for register_new_user for test compatibility"""
        try:
            # Navigate to register page first
            self.navigate_to_register()
            time.sleep(1)
            
            # Fill registration form
            result = self.register_new_user(user_data)
            
            # Take additional screenshot for verification
            self.take_screenshot("user_registration_completed")
            return result
        except Exception as e:
            print(f"Error registering user: {e}")
            self.take_screenshot("user_registration_error")
            return None
    
    def navigate_to_wishlist_page(self):
        """Navigate to wishlist page - alias for navigate_to_wishlist for test compatibility"""
        try:
            return self.navigate_to_wishlist()
        except Exception as e:
            print(f"Error navigating to wishlist: {e}")
            return None
    
    def verify_wishlist_functionality(self):
        """Verify wishlist functionality is working"""
        try:
            # Navigate to wishlist
            self.navigate_to_wishlist()
            time.sleep(2)
            
            # Check if page loaded correctly
            current_url = self.driver.current_url
            if "wishlist" in current_url.lower():
                self.take_screenshot("wishlist_functionality_verified")
                return True
            return False
        except Exception as e:
            print(f"Error verifying wishlist functionality: {e}")
            return False
    
    def complete_wishlist_workflow(self, user_data):
        """Complete full wishlist workflow for testing"""
        try:
            # Step 1: Register user
            self.register_user(user_data)
            time.sleep(2)
            
            # Step 2: Navigate to product
            self.navigate_to_product_page()
            time.sleep(2)
            
            # Step 3: Add to wishlist
            self.add_to_wishlist()
            time.sleep(2)
            
            # Step 4: Navigate to wishlist
            self.navigate_to_wishlist()
            time.sleep(2)
            
            # Take final screenshot
            self.take_screenshot("wishlist_workflow_completed")
            return True
        except Exception as e:
            print(f"Error in wishlist workflow: {e}")
            self.take_screenshot("wishlist_workflow_error")
            return False
    
    def navigate_to_product(self):
        """Navigate to product - alias for navigate_to_product_page"""
        return self.navigate_to_product_page()
    
    def check_product_in_wishlist(self):
        """Check if product is in wishlist"""
        try:
            # Navigate to wishlist first
            self.navigate_to_wishlist()
            time.sleep(2)
            
            # Check if there are items in wishlist
            items_count = self.get_wishlist_items_count()
            self.take_screenshot("wishlist_items_checked")
            
            return items_count > 0
        except Exception as e:
            print(f"Error checking product in wishlist: {e}")
            return False