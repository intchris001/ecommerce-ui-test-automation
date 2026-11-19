"""
Checkout page object model
"""
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pages.base_page import BasePage
import time

class CheckoutPage(BasePage):
    # Locators
    CHECKOUT_URL = "/index.php?route=checkout/checkout"
    
    # Product and cart
    ADD_TO_CART_BUTTON = (By.CSS_SELECTOR, "button[title='Add to Cart']")
    CART_BUTTON = (By.CSS_SELECTOR, ".btn-inverse")
    CHECKOUT_BUTTON = (By.CSS_SELECTOR, "a[title='Checkout']")
    
    # Guest checkout
    GUEST_CHECKOUT_RADIO = (By.CSS_SELECTOR, "input[value='guest']")
    CONTINUE_BUTTON = (By.ID, "button-account")
    
    # Billing details
    FIRST_NAME_INPUT = (By.ID, "input-payment-firstname")
    LAST_NAME_INPUT = (By.ID, "input-payment-lastname")
    EMAIL_INPUT = (By.ID, "input-payment-email")
    TELEPHONE_INPUT = (By.ID, "input-payment-telephone")
    ADDRESS_INPUT = (By.ID, "input-payment-address-1")
    CITY_INPUT = (By.ID, "input-payment-city")
    POSTCODE_INPUT = (By.ID, "input-payment-postcode")
    COUNTRY_SELECT = (By.ID, "input-payment-country")
    REGION_SELECT = (By.ID, "input-payment-zone")
    
    # Delivery method
    DELIVERY_CONTINUE = (By.ID, "button-shipping-method")
    
    # Payment method
    PAYMENT_CONTINUE = (By.ID, "button-payment-method")
    TERMS_CHECKBOX = (By.NAME, "agree")
    
    # Confirm order
    CONFIRM_ORDER_BUTTON = (By.ID, "button-confirm")
    ORDER_SUCCESS_MESSAGE = (By.CSS_SELECTOR, ".alert-success")
    
    def navigate_to_homepage(self):
        """Navigate to homepage"""
        self.open_url(self.config.BASE_URL)
        return self.take_screenshot("homepage_loaded")
    
    def add_product_to_cart(self):
        """Add first available product to cart"""
        try:
            # Find and click first add to cart button
            if self.is_element_present(self.ADD_TO_CART_BUTTON):
                self.click_element(self.ADD_TO_CART_BUTTON)
                time.sleep(2)
                return self.take_screenshot("product_added_to_cart")
        except:
            # Alternative approach - navigate to a specific product
            product_url = f"{self.config.BASE_URL}/index.php?route=product/product&product_id=40"
            self.open_url(product_url)
            if self.is_element_present(self.ADD_TO_CART_BUTTON):
                self.click_element(self.ADD_TO_CART_BUTTON)
                time.sleep(2)
                return self.take_screenshot("product_added_to_cart")
        return None
    
    def navigate_to_checkout(self):
        """Navigate to checkout page"""
        url = self.config.BASE_URL + self.CHECKOUT_URL
        self.open_url(url)
        return self.take_screenshot("checkout_page_loaded")
    
    def select_guest_checkout(self):
        """Select guest checkout option"""
        if self.is_element_present(self.GUEST_CHECKOUT_RADIO):
            self.click_element(self.GUEST_CHECKOUT_RADIO)
            self.click_element(self.CONTINUE_BUTTON)
            return self.take_screenshot("guest_checkout_selected")
        return None
    
    def fill_billing_details(self, billing_data):
        """Fill billing information form"""
        self.enter_text(self.FIRST_NAME_INPUT, billing_data["first_name"])
        self.enter_text(self.LAST_NAME_INPUT, billing_data["last_name"])
        self.enter_text(self.EMAIL_INPUT, billing_data["email"])
        self.enter_text(self.TELEPHONE_INPUT, billing_data["telephone"])
        self.enter_text(self.ADDRESS_INPUT, billing_data["address_1"])
        self.enter_text(self.CITY_INPUT, billing_data["city"])
        self.enter_text(self.POSTCODE_INPUT, billing_data["postcode"])
        
        # Handle country and region selection
        try:
            country_select = Select(self.find_element(self.COUNTRY_SELECT))
            country_select.select_by_visible_text(billing_data["country"])
            time.sleep(2)
            
            region_select = Select(self.find_element(self.REGION_SELECT))
            region_select.select_by_visible_text(billing_data["region"])
        except:
            pass  # Continue if dropdowns are not available
        
        return self.take_screenshot("billing_details_filled")
    
    def continue_to_delivery(self):
        """Continue to delivery method"""
        if self.is_element_present(self.DELIVERY_CONTINUE):
            self.click_element(self.DELIVERY_CONTINUE)
            return self.take_screenshot("delivery_method_selected")
        return None
    
    def continue_to_payment(self):
        """Continue to payment method"""
        if self.is_element_present(self.PAYMENT_CONTINUE):
            self.click_element(self.PAYMENT_CONTINUE)
            return self.take_screenshot("payment_method_selected")
        return None
    
    def accept_terms_and_confirm(self):
        """Accept terms and confirm order"""
        if self.is_element_present(self.TERMS_CHECKBOX):
            self.click_element(self.TERMS_CHECKBOX)
        
        self.click_element(self.CONFIRM_ORDER_BUTTON)
        return self.take_screenshot("order_confirmed")
    
    def get_success_message(self):
        """Get order success message"""
        if self.is_element_present(self.ORDER_SUCCESS_MESSAGE):
            return self.get_text(self.ORDER_SUCCESS_MESSAGE)
        return None
    
    def proceed_to_checkout(self):
        """Proceed to checkout from cart"""
        try:
            # Click cart button first
            if self.is_element_present(self.CART_BUTTON):
                self.click_element(self.CART_BUTTON)
                time.sleep(1)
            
            # Click checkout button
            if self.is_element_present(self.CHECKOUT_BUTTON):
                self.click_element(self.CHECKOUT_BUTTON)
                time.sleep(2)
                return self.take_screenshot("proceeded_to_checkout")
            else:
                # Alternative: navigate directly to checkout URL
                self.navigate_to_checkout()
                return self.take_screenshot("navigated_to_checkout")
        except Exception as e:
            print(f"Error proceeding to checkout: {e}")
            return None
    
    def confirm_order(self):
        """Complete the entire checkout process and confirm order"""
        try:
            # Continue through delivery method
            if self.is_element_present(self.DELIVERY_CONTINUE):
                self.click_element(self.DELIVERY_CONTINUE)
                time.sleep(1)
            
            # Continue through payment method
            if self.is_element_present(self.PAYMENT_CONTINUE):
                self.click_element(self.PAYMENT_CONTINUE)
                time.sleep(1)
            
            # Accept terms if checkbox exists
            if self.is_element_present(self.TERMS_CHECKBOX):
                self.click_element(self.TERMS_CHECKBOX)
                time.sleep(1)
            
            # Confirm order
            if self.is_element_present(self.CONFIRM_ORDER_BUTTON):
                self.click_element(self.CONFIRM_ORDER_BUTTON)
                time.sleep(3)
                
                # Check for success message
                success_msg = self.get_success_message()
                screenshot = self.take_screenshot("order_confirmation_attempt")
                
                return success_msg is not None
            
            return False
        except Exception as e:
            print(f"Error confirming order: {e}")
            self.take_screenshot("order_confirmation_error")
            return False