"""
Test cases for contact form functionality
"""
import pytest
import time
from pages.contact_page import ContactPage
from utils.helpers import TestHelpers

class TestContact:
    """Test class for contact form functionality"""
    
    def setup_method(self):
        """Setup before each test method"""
        self.test_start_time = time.time()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        test_duration = time.time() - self.test_start_time
        print(f"\nTest completed in {test_duration:.2f} seconds")
    
    @pytest.mark.contact
    @pytest.mark.smoke
    def test_contact_form_submission_valid_data(self, driver, test_data):
        """
        Test ID: TC011
        Test contact form submission with valid data
        """
        TestHelpers.log_test_step(1, "Navigate to contact page")
        contact_page = ContactPage(driver)
        contact_page.navigate_to_contact()
        time.sleep(2)
        
        TestHelpers.log_test_step(2, "Verify contact form is displayed")
        form_displayed = contact_page.is_contact_form_displayed()
        assert form_displayed, "Contact form should be displayed"
        
        TestHelpers.log_test_step(3, "Fill contact form with valid data")
        contact_data = test_data["contact"]["valid_enquiry"]
        contact_page.fill_contact_form(
            contact_data["name"],
            contact_data["email"],
            contact_data["enquiry"]
        )
        time.sleep(1)
        
        TestHelpers.log_test_step(4, "Submit contact form")
        contact_page.submit_form()
        time.sleep(3)
        
        TestHelpers.log_test_step(5, "Verify success message")
        success_message = contact_page.get_success_message()
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "contact_form_success")
        
        assert success_message, "Success message should be displayed after form submission"
        TestHelpers.log_test_step(6, "Verify form submission success", "PASS")
    
    @pytest.mark.contact
    def test_contact_form_submission_invalid_email(self, driver, test_data):
        """
        Test ID: TC012
        Test contact form submission with invalid email
        """
        TestHelpers.log_test_step(1, "Navigate to contact page")
        contact_page = ContactPage(driver)
        contact_page.navigate_to_contact()
        time.sleep(2)
        
        TestHelpers.log_test_step(2, "Fill contact form with invalid email")
        invalid_data = test_data["contact"]["invalid_email"]
        contact_page.fill_contact_form(
            invalid_data["name"],
            invalid_data["email"],
            invalid_data["enquiry"]
        )
        time.sleep(1)
        
        TestHelpers.log_test_step(3, "Submit contact form")
        contact_page.submit_form()
        time.sleep(2)
        
        TestHelpers.log_test_step(4, "Verify error handling")
        error_message = contact_page.get_error_message()
        field_errors = contact_page.check_field_errors()
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "contact_form_invalid_email")
        
        assert error_message or field_errors, "Error should be displayed for invalid email"
        TestHelpers.log_test_step(5, "Verify invalid email handling", "PASS")
    
    @pytest.mark.contact
    def test_contact_form_submission_empty_fields(self, driver):
        """
        Test ID: TC013
        Test contact form submission with empty required fields
        """
        TestHelpers.log_test_step(1, "Navigate to contact page")
        contact_page = ContactPage(driver)
        contact_page.navigate_to_contact()
        time.sleep(2)
        
        TestHelpers.log_test_step(2, "Submit empty contact form")
        contact_page.submit_empty_form()
        time.sleep(2)
        
        TestHelpers.log_test_step(3, "Verify validation errors")
        field_errors = contact_page.check_field_errors()
        error_message = contact_page.get_error_message()
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "contact_form_empty_fields")
        
        assert field_errors or error_message, "Validation errors should be displayed for empty fields"
        TestHelpers.log_test_step(4, "Verify empty fields validation", "PASS")
    
    @pytest.mark.contact
    def test_contact_form_long_message(self, driver, test_data):
        """
        Test ID: TC014
        Test contact form with very long message
        """
        TestHelpers.log_test_step(1, "Navigate to contact page")
        contact_page = ContactPage(driver)
        contact_page.navigate_to_contact()
        time.sleep(2)
        
        TestHelpers.log_test_step(2, "Fill contact form with long message")
        long_message_data = test_data["contact"]["long_message"]
        contact_page.fill_contact_form(
            long_message_data["name"],
            long_message_data["email"],
            long_message_data["enquiry"]
        )
        time.sleep(1)
        
        TestHelpers.log_test_step(3, "Submit contact form")
        contact_page.submit_form()
        time.sleep(3)
        
        TestHelpers.log_test_step(4, "Verify long message handling")
        success_message = contact_page.get_success_message()
        error_message = contact_page.get_error_message()
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "contact_form_long_message")
        
        # Either should succeed or show appropriate error for message length
        assert success_message or error_message, "Form should handle long messages appropriately"
        TestHelpers.log_test_step(5, "Verify long message handling", "PASS")
    
    @pytest.mark.contact
    @pytest.mark.regression
    def test_contact_form_special_characters(self, driver):
        """
        Test ID: TC015
        Test contact form with special characters
        """
        TestHelpers.log_test_step(1, "Navigate to contact page")
        contact_page = ContactPage(driver)
        contact_page.navigate_to_contact()
        time.sleep(2)
        
        TestHelpers.log_test_step(2, "Fill contact form with special characters")
        special_data = {
            "name": "Test User <script>alert('test')</script>",
            "email": "test+special@example.com",
            "enquiry": "Testing special chars: !@#$%^&*()_+{}|:<>?[]\\;'\",./"
        }
        
        contact_page.fill_contact_form(
            special_data["name"],
            special_data["email"],
            special_data["enquiry"]
        )
        time.sleep(1)
        
        TestHelpers.log_test_step(3, "Submit contact form")
        contact_page.submit_form()
        time.sleep(3)
        
        TestHelpers.log_test_step(4, "Verify special characters handling")
        success_message = contact_page.get_success_message()
        error_message = contact_page.get_error_message()
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "contact_form_special_chars")
        
        # Should handle special characters appropriately (either accept or reject with proper error)
        result = success_message or error_message
        assert result, "Form should handle special characters appropriately"
        TestHelpers.log_test_step(5, "Verify special characters handling", "PASS")
    
    @pytest.mark.contact
    def test_contact_form_field_limits(self, driver):
        """
        Test ID: TC016
        Test contact form field character limits
        """
        TestHelpers.log_test_step(1, "Navigate to contact page")
        contact_page = ContactPage(driver)
        contact_page.navigate_to_contact()
        time.sleep(2)
        
        TestHelpers.log_test_step(2, "Test field character limits")
        # Generate data that might exceed typical field limits
        long_name = "A" * 100  # Very long name
        long_email = "a" * 50 + "@example.com"  # Long email
        long_enquiry = TestHelpers.generate_long_text(2000)  # Very long enquiry
        
        contact_page.fill_contact_form(long_name, long_email, long_enquiry)
        time.sleep(1)
        
        TestHelpers.log_test_step(3, "Submit contact form")
        contact_page.submit_form()
        time.sleep(3)
        
        TestHelpers.log_test_step(4, "Verify field limits handling")
        success_message = contact_page.get_success_message()
        error_message = contact_page.get_error_message()
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "contact_form_field_limits")
        
        # Should either succeed or show appropriate error for field limits
        result = success_message or error_message
        assert result, "Form should handle field limits appropriately"
        TestHelpers.log_test_step(5, "Verify field limits handling", "PASS")

    @pytest.mark.contact
    def test_contact_form_missing_name(self, driver):
        """
        Additional Test: Missing name should trigger validation
        """
        TestHelpers.log_test_step(1, "Navigate to contact page")
        contact_page = ContactPage(driver)
        contact_page.navigate_to_contact()
        time.sleep(2)

        TestHelpers.log_test_step(2, "Fill contact form with missing name")
        contact_page.fill_contact_form(
            name="",
            email="valid.email@example.com",
            enquiry="This is a test enquiry"
        )
        time.sleep(1)

        TestHelpers.log_test_step(3, "Submit contact form")
        contact_page.submit_form()
        time.sleep(2)

        TestHelpers.log_test_step(4, "Verify validation error for name")
        field_errors = contact_page.check_field_errors()
        error_message = contact_page.get_error_message()
        TestHelpers.take_screenshot_with_timestamp(driver, "contact_missing_name")
        assert field_errors or error_message, "Validation should catch missing name"
        TestHelpers.log_test_step(5, "Missing name validation handled", "PASS")

    @pytest.mark.contact
    def test_contact_form_missing_enquiry(self, driver):
        """
        Additional Test: Missing enquiry should trigger validation
        """
        TestHelpers.log_test_step(1, "Navigate to contact page")
        contact_page = ContactPage(driver)
        contact_page.navigate_to_contact()
        time.sleep(2)

        TestHelpers.log_test_step(2, "Fill contact form with missing enquiry")
        contact_page.fill_contact_form(
            name="Valid User",
            email="valid.email@example.com",
            enquiry=""
        )
        time.sleep(1)

        TestHelpers.log_test_step(3, "Submit contact form")
        contact_page.submit_form()
        time.sleep(2)

        TestHelpers.log_test_step(4, "Verify validation error for enquiry")
        field_errors = contact_page.check_field_errors()
        error_message = contact_page.get_error_message()
        TestHelpers.take_screenshot_with_timestamp(driver, "contact_missing_enquiry")
        assert field_errors or error_message, "Validation should catch missing enquiry"
        TestHelpers.log_test_step(5, "Missing enquiry validation handled", "PASS")

    @pytest.mark.contact
    def test_contact_form_multiple_submissions(self, driver):
        """
        Additional Test: Multiple submissions should be handled gracefully
        """
        TestHelpers.log_test_step(1, "Navigate to contact page")
        contact_page = ContactPage(driver)
        contact_page.navigate_to_contact()

        TestHelpers.log_test_step(2, "First submission with valid data")
        contact_page.fill_contact_form(
            "First User",
            "first.user@example.com",
            "First enquiry message"
        )
        contact_page.submit_form()
        time.sleep(2)
        first_success = contact_page.get_success_message()

        TestHelpers.log_test_step(3, "Second submission with different valid data")
        contact_page.navigate_to_contact()
        contact_page.fill_contact_form(
            "Second User",
            "second.user@example.com",
            "Second enquiry message"
        )
        contact_page.submit_form()
        time.sleep(2)
        second_success = contact_page.get_success_message()
        TestHelpers.take_screenshot_with_timestamp(driver, "contact_multiple_submissions")
        assert first_success or second_success, "At least one submission should succeed"
        TestHelpers.log_test_step(4, "Multiple submissions handled", "PASS")

    @pytest.mark.contact
    def test_contact_form_whitespace_trim(self, driver):
        """
        Additional Test: Leading/trailing whitespace is handled
        """
        TestHelpers.log_test_step(1, "Navigate to contact page")
        contact_page = ContactPage(driver)
        contact_page.navigate_to_contact()
        time.sleep(1)

        TestHelpers.log_test_step(2, "Fill form with whitespace around fields")
        contact_page.fill_contact_form(
            "  Trim User  ",
            "  trim.user@example.com  ",
            "   This enquiry should be trimmed.   "
        )
        time.sleep(1)

        TestHelpers.log_test_step(3, "Submit contact form")
        contact_page.submit_form()
        time.sleep(2)

        TestHelpers.log_test_step(4, "Verify submission handled")
        success_message = contact_page.get_success_message()
        error_message = contact_page.get_error_message()
        TestHelpers.take_screenshot_with_timestamp(driver, "contact_whitespace_trim")
        assert success_message or error_message, "Form should handle trimmed inputs"
        TestHelpers.log_test_step(5, "Whitespace trimming handled", "PASS")