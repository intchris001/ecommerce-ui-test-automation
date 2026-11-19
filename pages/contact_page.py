"""
Contact page object model
"""
from selenium.webdriver.common.by import By
from pages.base_page import BasePage
import time

class ContactPage(BasePage):
    # URL
    CONTACT_URL = "/index.php?route=information/contact"
    
    # Form elements
    NAME_INPUT = (By.ID, "input-name")
    EMAIL_INPUT = (By.ID, "input-email")
    ENQUIRY_TEXTAREA = (By.ID, "input-enquiry")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "input[value='Submit']")
    
    # Success/Error messages
    SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    ERROR_MESSAGE = (By.CSS_SELECTOR, ".alert-danger")
    FIELD_ERROR = (By.CSS_SELECTOR, ".text-danger")
    
    # Form validation elements
    REQUIRED_FIELD_INDICATORS = (By.CSS_SELECTOR, ".required")
    
    def navigate_to_contact(self):
        """Navigate to contact page"""
        url = self.config.BASE_URL + self.CONTACT_URL
        self.open_url(url)
        return self.take_screenshot("contact_page_loaded")
    
    def verify_form_displayed(self):
        """Verify contact form is displayed with required fields"""
        form_displayed = (
            self.is_element_present(self.NAME_INPUT) and
            self.is_element_present(self.EMAIL_INPUT) and
            self.is_element_present(self.ENQUIRY_TEXTAREA) and
            self.is_element_present(self.SUBMIT_BUTTON)
        )
        if form_displayed:
            return self.take_screenshot("contact_form_displayed")
        return None
    
    def fill_name_field(self, name):
        """Fill name field"""
        self.enter_text(self.NAME_INPUT, name)
        return self.take_screenshot("name_field_filled")
    
    def fill_email_field(self, email):
        """Fill email field"""
        self.enter_text(self.EMAIL_INPUT, email)
        return self.take_screenshot("email_field_filled")
    
    def fill_enquiry_field(self, message):
        """Fill enquiry/message field"""
        self.enter_text(self.ENQUIRY_TEXTAREA, message)
        return self.take_screenshot("enquiry_field_filled")
    
    def fill_contact_form(self, *args, **kwargs):
        """Fill contact form with provided data - supports multiple formats"""
        try:
            if len(args) == 1 and isinstance(args[0], dict):
                # Dictionary format: fill_contact_form({"name": "...", "email": "...", "message": "..."})
                contact_data = args[0]
                name = contact_data.get("name", "")
                email = contact_data.get("email", "")
                message = contact_data.get("message", contact_data.get("enquiry", ""))
            elif len(args) == 3:
                # Individual parameters format: fill_contact_form(name, email, message)
                name, email, message = args
            else:
                raise ValueError("Invalid arguments for fill_contact_form")
            
            self.enter_text(self.NAME_INPUT, name)
            self.enter_text(self.EMAIL_INPUT, email)
            self.enter_text(self.ENQUIRY_TEXTAREA, message)
            return self.take_screenshot("contact_form_filled")
        except Exception as e:
            print(f"Error filling contact form: {e}")
            return None
    
    def submit_form(self):
        """Submit contact form"""
        self.click_element(self.SUBMIT_BUTTON)
        time.sleep(2)
        return self.take_screenshot("contact_form_submitted")
    
    def get_success_message(self):
        """Get success message text"""
        if self.is_element_present(self.SUCCESS_MESSAGE):
            return self.get_text(self.SUCCESS_MESSAGE)
        return None
    
    def get_error_message(self):
        """Get error message text"""
        if self.is_element_present(self.ERROR_MESSAGE):
            return self.get_text(self.ERROR_MESSAGE)
        return None
    
    def has_field_errors(self):
        """Check if form has field validation errors"""
        return self.is_element_present(self.FIELD_ERROR)
    
    def submit_empty_form(self):
        """Submit form with empty fields for validation testing"""
        # Clear all fields first
        self.enter_text(self.NAME_INPUT, "")
        self.enter_text(self.EMAIL_INPUT, "")
        self.enter_text(self.ENQUIRY_TEXTAREA, "")
        
        screenshot = self.take_screenshot("empty_form_before_submit")
        self.click_element(self.SUBMIT_BUTTON)
        time.sleep(2)
        return self.take_screenshot("empty_form_submitted")
    
    def test_invalid_email(self, invalid_email):
        """Test form with invalid email format"""
        self.enter_text(self.NAME_INPUT, "Test User")
        self.enter_text(self.EMAIL_INPUT, invalid_email)
        self.enter_text(self.ENQUIRY_TEXTAREA, "Test message")
        
        screenshot = self.take_screenshot("invalid_email_entered")
        self.click_element(self.SUBMIT_BUTTON)
        time.sleep(2)
        return self.take_screenshot("invalid_email_submitted")
    
    def test_long_message(self, long_message):
        """Test form with extremely long message"""
        self.enter_text(self.NAME_INPUT, "Test User")
        self.enter_text(self.EMAIL_INPUT, "test@example.com")
        self.enter_text(self.ENQUIRY_TEXTAREA, long_message)
        
        screenshot = self.take_screenshot("long_message_entered")
        self.click_element(self.SUBMIT_BUTTON)
        time.sleep(2)
        return self.take_screenshot("long_message_submitted")
    
    def is_contact_form_visible(self):
        """Check if contact form is visible and accessible"""
        try:
            form_visible = (
                self.is_element_present(self.NAME_INPUT) and
                self.is_element_present(self.EMAIL_INPUT) and
                self.is_element_present(self.ENQUIRY_TEXTAREA) and
                self.is_element_present(self.SUBMIT_BUTTON)
            )
            
            if form_visible:
                self.take_screenshot("contact_form_visible")
                return True
            return False
        except Exception as e:
            print(f"Error checking form visibility: {e}")
            return False
    
    def validate_form_fields(self):
        """Validate that all required form fields are present"""
        try:
            required_fields = [
                self.NAME_INPUT,
                self.EMAIL_INPUT,
                self.ENQUIRY_TEXTAREA
            ]
            
            for field in required_fields:
                if not self.is_element_present(field):
                    return False
            
            self.take_screenshot("form_fields_validated")
            return True
        except Exception as e:
            print(f"Error validating form fields: {e}")
            return False
    
    def clear_form(self):
        """Clear all form fields"""
        try:
            self.enter_text(self.NAME_INPUT, "")
            self.enter_text(self.EMAIL_INPUT, "")
            self.enter_text(self.ENQUIRY_TEXTAREA, "")
            return self.take_screenshot("form_cleared")
        except Exception as e:
            print(f"Error clearing form: {e}")
            return None
    
    def is_contact_form_displayed(self):
        """Check if contact form is displayed - alias for is_contact_form_visible"""
        return self.is_contact_form_visible()
    
    def check_field_errors(self):
        """Check for field validation errors"""
        try:
            has_errors = self.has_field_errors()
            self.take_screenshot("field_errors_checked")
            return has_errors
        except Exception as e:
            print(f"Error checking field errors: {e}")
            return False