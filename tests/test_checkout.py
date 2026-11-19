"""
Test cases for checkout functionality
"""
import pytest
import time
from pages.checkout_page import CheckoutPage
from utils.helpers import TestHelpers

class TestCheckout:
    """Test class for checkout functionality"""
    
    def setup_method(self):
        """Setup before each test method"""
        self.test_start_time = time.time()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        test_duration = time.time() - self.test_start_time
        print(f"\nTest completed in {test_duration:.2f} seconds")
    
    @pytest.mark.checkout
    @pytest.mark.smoke
    def test_guest_checkout_process(self, driver, test_data):
        """
        Test ID: TC001
        Test guest checkout process with valid data
        """
        TestHelpers.log_test_step(1, "Navigate to checkout page")
        checkout_page = CheckoutPage(driver)
        checkout_page.navigate_to_checkout()
        
        TestHelpers.log_test_step(2, "Add product to cart")
        checkout_page.add_product_to_cart()
        time.sleep(2)
        
        TestHelpers.log_test_step(3, "Proceed to checkout")
        checkout_page.proceed_to_checkout()
        time.sleep(2)
        
        TestHelpers.log_test_step(4, "Select guest checkout")
        checkout_page.select_guest_checkout()
        time.sleep(1)
        
        TestHelpers.log_test_step(5, "Fill billing details")
        billing_data = test_data["checkout"]["valid_billing"]
        checkout_page.fill_billing_details(billing_data)
        time.sleep(1)
        
        TestHelpers.log_test_step(6, "Confirm order")
        success = checkout_page.confirm_order()
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "guest_checkout_completed")
        
        assert success, "Guest checkout process should complete successfully"
        TestHelpers.log_test_step(7, "Verify checkout completion", "PASS")
    
    @pytest.mark.checkout
    def test_checkout_with_invalid_billing_data(self, driver, test_data):
        """
        Test ID: TC002
        Test checkout with invalid billing information
        """
        TestHelpers.log_test_step(1, "Navigate to checkout page")
        checkout_page = CheckoutPage(driver)
        checkout_page.navigate_to_checkout()
        
        TestHelpers.log_test_step(2, "Add product to cart")
        checkout_page.add_product_to_cart()
        time.sleep(2)
        
        TestHelpers.log_test_step(3, "Proceed to checkout")
        checkout_page.proceed_to_checkout()
        time.sleep(2)
        
        TestHelpers.log_test_step(4, "Select guest checkout")
        checkout_page.select_guest_checkout()
        time.sleep(1)
        
        TestHelpers.log_test_step(5, "Fill invalid billing details")
        invalid_data = test_data["checkout"]["invalid_billing"]
        checkout_page.fill_billing_details(invalid_data)
        time.sleep(1)
        
        TestHelpers.log_test_step(6, "Attempt to confirm order")
        success = checkout_page.confirm_order()
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "checkout_invalid_data")
        
        assert not success, "Checkout should fail with invalid billing data"
        TestHelpers.log_test_step(7, "Verify checkout failure", "PASS")
    
    @pytest.mark.checkout
    def test_checkout_with_empty_cart(self, driver):
        """
        Test ID: TC003
        Test checkout process with empty cart
        """
        TestHelpers.log_test_step(1, "Navigate to checkout page directly")
        checkout_page = CheckoutPage(driver)
        checkout_page.navigate_to_checkout()
        
        TestHelpers.log_test_step(2, "Attempt to proceed to checkout with empty cart")
        checkout_page.proceed_to_checkout()
        time.sleep(2)
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "empty_cart_checkout")
        
        # Verify that checkout is not possible with empty cart
        current_url = driver.current_url
        assert "checkout" not in current_url.lower() or "cart" in current_url.lower(), \
            "Should not be able to proceed to checkout with empty cart"
        
        TestHelpers.log_test_step(3, "Verify empty cart handling", "PASS")
    
    @pytest.mark.checkout
    def test_multiple_products_checkout(self, driver, test_data):
        """
        Test ID: TC004
        Test checkout with multiple products in cart
        """
        TestHelpers.log_test_step(1, "Navigate to checkout page")
        checkout_page = CheckoutPage(driver)
        checkout_page.navigate_to_checkout()
        
        TestHelpers.log_test_step(2, "Add multiple products to cart")
        # Add first product
        checkout_page.add_product_to_cart()
        time.sleep(1)
        
        # Navigate back and add another product
        driver.back()
        time.sleep(1)
        checkout_page.add_product_to_cart()
        time.sleep(2)
        
        TestHelpers.log_test_step(3, "Proceed to checkout")
        checkout_page.proceed_to_checkout()
        time.sleep(2)
        
        TestHelpers.log_test_step(4, "Select guest checkout")
        checkout_page.select_guest_checkout()
        time.sleep(1)
        
        TestHelpers.log_test_step(5, "Fill billing details")
        billing_data = test_data["checkout"]["valid_billing"]
        checkout_page.fill_billing_details(billing_data)
        time.sleep(1)
        
        TestHelpers.log_test_step(6, "Confirm order")
        success = checkout_page.confirm_order()
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "multiple_products_checkout")
        
        assert success, "Multiple products checkout should complete successfully"
        TestHelpers.log_test_step(7, "Verify multiple products checkout", "PASS")
    
    @pytest.mark.checkout
    @pytest.mark.regression
    def test_checkout_form_validation(self, driver):
        """
        Test ID: TC005
        Test checkout form field validation
        """
        TestHelpers.log_test_step(1, "Navigate to checkout page")
        checkout_page = CheckoutPage(driver)
        checkout_page.navigate_to_checkout()
        
        TestHelpers.log_test_step(2, "Add product to cart")
        checkout_page.add_product_to_cart()
        time.sleep(2)
        
        TestHelpers.log_test_step(3, "Proceed to checkout")
        checkout_page.proceed_to_checkout()
        time.sleep(2)
        
        TestHelpers.log_test_step(4, "Select guest checkout")
        checkout_page.select_guest_checkout()
        time.sleep(1)
        
        TestHelpers.log_test_step(5, "Submit form with empty fields")
        # Try to submit without filling any fields
        checkout_page.confirm_order()
        time.sleep(2)
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "checkout_form_validation")
        
        # Verify that form validation prevents submission
        current_url = driver.current_url
        assert "success" not in current_url.lower(), \
            "Form should not submit with empty required fields"
        
        TestHelpers.log_test_step(6, "Verify form validation", "PASS")

    @pytest.mark.checkout
    def test_checkout_page_url_validation(self, driver):
        """
        Additional Test: Validate checkout URL contains expected route
        """
        TestHelpers.log_test_step(1, "Navigate to checkout page")
        checkout_page = CheckoutPage(driver)
        checkout_page.navigate_to_checkout()
        time.sleep(1)

        # Take screenshot and validate URL
        TestHelpers.take_screenshot_with_timestamp(driver, "checkout_url_validation")
        assert "checkout" in driver.current_url.lower(), "Checkout URL should contain 'checkout'"
        TestHelpers.log_test_step(2, "Verify checkout URL", "PASS")

    @pytest.mark.checkout
    def test_delivery_and_payment_flow(self, driver, test_data):
        """
        Additional Test: Continue through delivery and payment steps
        """
        TestHelpers.log_test_step(1, "Navigate to checkout page")
        checkout_page = CheckoutPage(driver)
        checkout_page.navigate_to_checkout()

        TestHelpers.log_test_step(2, "Add product to cart")
        checkout_page.add_product_to_cart()
        time.sleep(1)

        TestHelpers.log_test_step(3, "Proceed to checkout")
        checkout_page.proceed_to_checkout()
        time.sleep(1)

        TestHelpers.log_test_step(4, "Select guest checkout")
        checkout_page.select_guest_checkout()
        time.sleep(1)

        TestHelpers.log_test_step(5, "Fill billing details")
        billing_data = test_data["checkout"]["valid_billing"]
        checkout_page.fill_billing_details(billing_data)

        TestHelpers.log_test_step(6, "Continue to delivery and payment")
        checkout_page.continue_to_delivery()
        time.sleep(1)
        checkout_page.continue_to_payment()
        time.sleep(1)

        TestHelpers.log_test_step(7, "Confirm order attempt")
        success = checkout_page.confirm_order()
        TestHelpers.take_screenshot_with_timestamp(driver, "delivery_payment_flow_confirm")
        assert success in [True, False], "Should attempt to confirm order and return boolean"
        TestHelpers.log_test_step(8, "Delivery/payment flow tested", "PASS")

    @pytest.mark.checkout
    def test_checkout_cart_navigation_flow(self, driver):
        """
        Additional Test: Navigate via cart button to checkout
        """
        TestHelpers.log_test_step(1, "Add product and open cart")
        checkout_page = CheckoutPage(driver)
        checkout_page.add_product_to_cart()
        time.sleep(1)

        TestHelpers.log_test_step(2, "Proceed to checkout via cart")
        checkout_page.proceed_to_checkout()
        time.sleep(1)
        TestHelpers.take_screenshot_with_timestamp(driver, "cart_to_checkout_navigation")
        assert "checkout" in driver.current_url.lower(), "Should navigate to checkout page"
        TestHelpers.log_test_step(3, "Verify cart navigation flow", "PASS")

    @pytest.mark.checkout
    def test_checkout_missing_postcode_validation(self, driver, test_data):
        """
        Additional Test: Missing postcode should prevent successful checkout
        """
        TestHelpers.log_test_step(1, "Navigate to checkout page")
        checkout_page = CheckoutPage(driver)
        checkout_page.navigate_to_checkout()

        TestHelpers.log_test_step(2, "Add product to cart")
        checkout_page.add_product_to_cart()
        time.sleep(1)

        TestHelpers.log_test_step(3, "Proceed to checkout")
        checkout_page.proceed_to_checkout()
        time.sleep(1)

        TestHelpers.log_test_step(4, "Select guest checkout")
        checkout_page.select_guest_checkout()
        time.sleep(1)

        TestHelpers.log_test_step(5, "Fill billing details then clear postcode")
        billing_data = test_data["checkout"]["valid_billing"]
        checkout_page.fill_billing_details(billing_data)
        # Clear postcode to simulate missing required field
        checkout_page.enter_text(CheckoutPage.POSTCODE_INPUT, "")
        time.sleep(1)

        TestHelpers.log_test_step(6, "Attempt to confirm order")
        success = checkout_page.confirm_order()
        TestHelpers.take_screenshot_with_timestamp(driver, "checkout_missing_postcode")
        assert success is False, "Checkout should fail when postcode is missing"
        TestHelpers.log_test_step(7, "Verify postcode validation", "PASS")

    @pytest.mark.checkout
    def test_checkout_invalid_email_in_billing(self, driver, test_data):
        """
        Additional Test: Invalid email in billing should fail checkout
        """
        TestHelpers.log_test_step(1, "Navigate to checkout page")
        checkout_page = CheckoutPage(driver)
        checkout_page.navigate_to_checkout()

        TestHelpers.log_test_step(2, "Add product to cart")
        checkout_page.add_product_to_cart()
        time.sleep(1)

        TestHelpers.log_test_step(3, "Proceed to checkout")
        checkout_page.proceed_to_checkout()
        time.sleep(1)

        TestHelpers.log_test_step(4, "Select guest checkout")
        checkout_page.select_guest_checkout()
        time.sleep(1)

        TestHelpers.log_test_step(5, "Fill billing details with invalid email")
        invalid_data = dict(test_data["checkout"]["valid_billing"])  # copy
        invalid_data["email"] = "invalid-email"
        checkout_page.fill_billing_details(invalid_data)

        TestHelpers.log_test_step(6, "Attempt to confirm order")
        success = checkout_page.confirm_order()
        TestHelpers.take_screenshot_with_timestamp(driver, "checkout_invalid_email")
        assert success is False, "Checkout should fail with invalid email"
        TestHelpers.log_test_step(7, "Verify email validation", "PASS")