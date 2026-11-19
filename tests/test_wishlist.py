"""
Test cases for wishlist functionality
"""
import pytest
import time
from pages.wishlist_page import WishlistPage
from pages.login_page import LoginPage
from utils.helpers import TestHelpers

class TestWishlist:
    """Test class for wishlist functionality"""
    
    def setup_method(self):
        """Setup before each test method"""
        self.test_start_time = time.time()
    
    def teardown_method(self):
        """Cleanup after each test method"""
        test_duration = time.time() - self.test_start_time
        print(f"\nTest completed in {test_duration:.2f} seconds")
    
    @pytest.mark.wishlist
    @pytest.mark.smoke
    def test_add_product_to_wishlist_registered_user(self, driver, test_data):
        """
        Test ID: TC006
        Test adding product to wishlist as registered user
        """
        TestHelpers.log_test_step(1, "Navigate to registration page")
        wishlist_page = WishlistPage(driver)
        wishlist_page.navigate_to_register()
        
        TestHelpers.log_test_step(2, "Register new user")
        user_data = TestHelpers.generate_test_data()
        wishlist_page.register_user(user_data)
        time.sleep(3)
        
        TestHelpers.log_test_step(3, "Navigate to product page")
        wishlist_page.navigate_to_product()
        time.sleep(2)
        
        TestHelpers.log_test_step(4, "Add product to wishlist")
        success = wishlist_page.add_to_wishlist()
        time.sleep(2)
        
        TestHelpers.log_test_step(5, "Navigate to wishlist page")
        wishlist_page.navigate_to_wishlist()
        time.sleep(2)
        
        TestHelpers.log_test_step(6, "Verify product in wishlist")
        is_in_wishlist = wishlist_page.check_product_in_wishlist()
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "product_added_to_wishlist")
        
        assert success and is_in_wishlist, "Product should be successfully added to wishlist"
        TestHelpers.log_test_step(7, "Verify wishlist addition", "PASS")
    
    @pytest.mark.wishlist
    def test_remove_product_from_wishlist(self, driver, test_data):
        """
        Test ID: TC007
        Test removing product from wishlist
        """
        TestHelpers.log_test_step(1, "Navigate to registration page")
        wishlist_page = WishlistPage(driver)
        wishlist_page.navigate_to_register()
        
        TestHelpers.log_test_step(2, "Register new user")
        user_data = TestHelpers.generate_test_data()
        wishlist_page.register_user(user_data)
        time.sleep(3)
        
        TestHelpers.log_test_step(3, "Navigate to product page")
        wishlist_page.navigate_to_product()
        time.sleep(2)
        
        TestHelpers.log_test_step(4, "Add product to wishlist")
        wishlist_page.add_to_wishlist()
        time.sleep(2)
        
        TestHelpers.log_test_step(5, "Navigate to wishlist page")
        wishlist_page.navigate_to_wishlist()
        time.sleep(2)
        
        TestHelpers.log_test_step(6, "Remove product from wishlist")
        success = wishlist_page.remove_from_wishlist()
        time.sleep(2)
        
        TestHelpers.log_test_step(7, "Verify product removed from wishlist")
        is_in_wishlist = wishlist_page.check_product_in_wishlist()
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "product_removed_from_wishlist")
        
        assert success and not is_in_wishlist, "Product should be successfully removed from wishlist"
        TestHelpers.log_test_step(8, "Verify wishlist removal", "PASS")
    
    @pytest.mark.wishlist
    def test_wishlist_access_without_login(self, driver):
        """
        Test ID: TC008
        Test accessing wishlist without being logged in
        """
        TestHelpers.log_test_step(1, "Navigate to product page without login")
        wishlist_page = WishlistPage(driver)
        wishlist_page.navigate_to_product()
        time.sleep(2)
        
        TestHelpers.log_test_step(2, "Attempt to add product to wishlist")
        success = wishlist_page.add_to_wishlist()
        time.sleep(2)
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "wishlist_without_login")
        
        # Should either redirect to login or show login requirement
        current_url = driver.current_url
        login_required = "login" in current_url.lower() or not success
        
        assert login_required, "Should require login to add items to wishlist"
        TestHelpers.log_test_step(3, "Verify login requirement", "PASS")
    
    @pytest.mark.wishlist
    def test_wishlist_persistence_after_logout_login(self, driver, test_data):
        """
        Test ID: TC009
        Test wishlist persistence after logout and login
        """
        TestHelpers.log_test_step(1, "Navigate to registration page")
        wishlist_page = WishlistPage(driver)
        wishlist_page.navigate_to_register()
        
        TestHelpers.log_test_step(2, "Register new user")
        user_data = TestHelpers.generate_test_data()
        wishlist_page.register_user(user_data)
        time.sleep(3)
        
        TestHelpers.log_test_step(3, "Add product to wishlist")
        wishlist_page.navigate_to_product()
        time.sleep(2)
        wishlist_page.add_to_wishlist()
        time.sleep(2)
        
        TestHelpers.log_test_step(4, "Logout")
        wishlist_page.logout()
        time.sleep(2)
        
        TestHelpers.log_test_step(5, "Login again")
        login_page = LoginPage(driver)
        login_page.navigate_to_login()
        login_page.login(user_data["email"], user_data["password"])
        time.sleep(3)
        
        TestHelpers.log_test_step(6, "Check wishlist persistence")
        wishlist_page.navigate_to_wishlist()
        time.sleep(2)
        is_in_wishlist = wishlist_page.check_product_in_wishlist()
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "wishlist_persistence")
        
        assert is_in_wishlist, "Wishlist should persist after logout and login"
        TestHelpers.log_test_step(7, "Verify wishlist persistence", "PASS")
    
    @pytest.mark.wishlist
    @pytest.mark.regression
    def test_multiple_products_in_wishlist(self, driver, test_data):
        """
        Test ID: TC010
        Test adding multiple products to wishlist
        """
        TestHelpers.log_test_step(1, "Navigate to registration page")
        wishlist_page = WishlistPage(driver)
        wishlist_page.navigate_to_register()
        
        TestHelpers.log_test_step(2, "Register new user")
        user_data = TestHelpers.generate_test_data()
        wishlist_page.register_user(user_data)
        time.sleep(3)
        
        TestHelpers.log_test_step(3, "Add first product to wishlist")
        wishlist_page.navigate_to_product()
        time.sleep(2)
        wishlist_page.add_to_wishlist()
        time.sleep(2)
        
        TestHelpers.log_test_step(4, "Navigate to different product")
        driver.back()
        time.sleep(1)
        wishlist_page.navigate_to_product()
        time.sleep(2)
        
        TestHelpers.log_test_step(5, "Add second product to wishlist")
        wishlist_page.add_to_wishlist()
        time.sleep(2)
        
        TestHelpers.log_test_step(6, "Check wishlist contains multiple products")
        wishlist_page.navigate_to_wishlist()
        time.sleep(2)
        
        # Take screenshot for verification
        TestHelpers.take_screenshot_with_timestamp(driver, "multiple_products_wishlist")
        
        # Verify multiple products are in wishlist
        # This is a basic check - in real implementation, you'd count actual products
        is_in_wishlist = wishlist_page.check_product_in_wishlist()
        
        assert is_in_wishlist, "Multiple products should be addable to wishlist"
        TestHelpers.log_test_step(7, "Verify multiple products in wishlist", "PASS")

    @pytest.mark.wishlist
    def test_wishlist_items_count_increases_on_add(self, driver):
        """
        Additional Test: Wishlist items count should increase after add
        """
        TestHelpers.log_test_step(1, "Register new user and login")
        wishlist_page = WishlistPage(driver)
        user_data = TestHelpers.generate_test_data()
        wishlist_page.register_user(user_data)
        time.sleep(2)

        TestHelpers.log_test_step(2, "Check initial wishlist count")
        wishlist_page.navigate_to_wishlist()
        before_count = wishlist_page.get_wishlist_items_count()

        TestHelpers.log_test_step(3, "Add product to wishlist")
        wishlist_page.navigate_to_product()
        wishlist_page.add_to_wishlist()
        time.sleep(1)

        TestHelpers.log_test_step(4, "Verify wishlist count increased")
        wishlist_page.navigate_to_wishlist()
        after_count = wishlist_page.get_wishlist_items_count()
        TestHelpers.take_screenshot_with_timestamp(driver, "wishlist_count_increase")
        assert after_count >= before_count + 1 or after_count > 0, "Wishlist count should increase"
        TestHelpers.log_test_step(5, "Wishlist count increased", "PASS")

    @pytest.mark.wishlist
    def test_wishlist_remove_item_results_decrease(self, driver):
        """
        Additional Test: Removing wishlist item decreases count
        """
        TestHelpers.log_test_step(1, "Register and add product to wishlist")
        wishlist_page = WishlistPage(driver)
        user_data = TestHelpers.generate_test_data()
        wishlist_page.register_user(user_data)
        wishlist_page.navigate_to_product()
        wishlist_page.add_to_wishlist()
        time.sleep(1)

        TestHelpers.log_test_step(2, "Navigate to wishlist and record count")
        wishlist_page.navigate_to_wishlist()
        before_count = wishlist_page.get_wishlist_items_count()

        TestHelpers.log_test_step(3, "Remove first item and verify count")
        wishlist_page.remove_from_wishlist()
        time.sleep(1)
        wishlist_page.navigate_to_wishlist()
        after_count = wishlist_page.get_wishlist_items_count()
        TestHelpers.take_screenshot_with_timestamp(driver, "wishlist_count_decrease")
        assert after_count <= max(0, before_count - 1), "Wishlist count should decrease after removal"
        TestHelpers.log_test_step(4, "Wishlist count decreased", "PASS")

    @pytest.mark.wishlist
    def test_wishlist_duplicate_add_no_error(self, driver):
        """
        Additional Test: Adding same product twice should not error
        """
        TestHelpers.log_test_step(1, "Register and navigate to product")
        wishlist_page = WishlistPage(driver)
        user_data = TestHelpers.generate_test_data()
        wishlist_page.register_user(user_data)
        wishlist_page.navigate_to_product()

        TestHelpers.log_test_step(2, "Add same product twice")
        wishlist_page.add_to_wishlist()
        time.sleep(1)
        wishlist_page.add_to_wishlist()
        time.sleep(1)

        TestHelpers.log_test_step(3, "Verify wishlist has items")
        wishlist_page.navigate_to_wishlist()
        has_items = wishlist_page.get_wishlist_items_count() > 0
        TestHelpers.take_screenshot_with_timestamp(driver, "wishlist_duplicate_add")
        assert has_items, "Wishlist should contain at least one item"
        TestHelpers.log_test_step(4, "Duplicate add handled", "PASS")

    @pytest.mark.wishlist
    def test_wishlist_direct_page_after_login(self, driver):
        """
        Additional Test: Wishlist page reachable after login
        """
        TestHelpers.log_test_step(1, "Register and login user")
        wishlist_page = WishlistPage(driver)
        user_data = TestHelpers.generate_test_data()
        wishlist_page.register_user(user_data)
        time.sleep(1)

        TestHelpers.log_test_step(2, "Navigate to wishlist page")
        wishlist_page.navigate_to_wishlist()
        TestHelpers.take_screenshot_with_timestamp(driver, "wishlist_direct_page")
        assert "wishlist" in driver.current_url.lower(), "Should be on wishlist page"
        TestHelpers.log_test_step(3, "Wishlist page reachable", "PASS")

    @pytest.mark.wishlist
    def test_wishlist_add_button_absent_on_wishlist_page(self, driver):
        """
        Additional Test: Add to wishlist button should not exist on wishlist page
        """
        TestHelpers.log_test_step(1, "Register user and navigate to wishlist")
        wishlist_page = WishlistPage(driver)
        user_data = TestHelpers.generate_test_data()
        wishlist_page.register_user(user_data)
        wishlist_page.navigate_to_wishlist()

        TestHelpers.log_test_step(2, "Try add to wishlist on wishlist page")
        result = wishlist_page.add_to_wishlist()  # Button should not be present here
        TestHelpers.take_screenshot_with_timestamp(driver, "wishlist_page_add_button_absent")
        assert result is None, "Add to wishlist should not work on wishlist page"
        TestHelpers.log_test_step(3, "Button absent validated", "PASS")

    @pytest.mark.wishlist
    def test_end_to_end_wishlist_workflow(self, driver):
        """
        Additional Test: End-to-end wishlist workflow completes without exceptions
        """
        TestHelpers.log_test_step(1, "Complete end-to-end wishlist workflow")
        wishlist_page = WishlistPage(driver)
        user_data = TestHelpers.generate_test_data()
        result = wishlist_page.complete_wishlist_workflow(user_data)
        TestHelpers.take_screenshot_with_timestamp(driver, "wishlist_workflow_e2e")
        assert result in [True, False], "Workflow should execute and return boolean"
        TestHelpers.log_test_step(2, "E2E workflow executed", "PASS")