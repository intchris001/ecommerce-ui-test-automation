"""
Pytest configuration and fixtures
"""
import pytest
import os
import sys
from datetime import datetime

# Add the automation_tests directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utils.driver_manager import DriverManager
from utils.helpers import TestHelpers
from config.config import TestConfig

@pytest.fixture(scope="session")
def config():
    """Provide test configuration"""
    return TestConfig()

@pytest.fixture(scope="function")
def driver(config):
    """Provide WebDriver instance for each test"""
    driver_manager = DriverManager(config)
    driver = driver_manager.get_driver()
    
    yield driver
    
    # Cleanup
    driver_manager.quit_driver(driver)

@pytest.fixture(scope="function")
def driver_with_screenshot(driver, request):
    """Provide WebDriver with automatic screenshot on failure"""
    yield driver
    
    # Take screenshot on test failure
    if request.node.rep_call.failed:
        test_name = request.node.name
        timestamp = TestHelpers.get_timestamp()
        screenshot_name = f"FAILED_{test_name}_{timestamp}"
        TestHelpers.take_screenshot_with_timestamp(driver, screenshot_name)

@pytest.fixture(autouse=True)
def setup_test_environment(config):
    """Setup test environment before each test"""
    # Ensure directories exist
    config.ensure_directories_exist()
    
    # Clean old screenshots
    TestHelpers.clean_screenshot_directory()

@pytest.fixture(scope="session")
def test_data():
    """Provide test data"""
    from config.test_data import CHECKOUT_DATA, CONTACT_DATA, USER_DATA
    return {
        "checkout": CHECKOUT_DATA,
        "contact": CONTACT_DATA,
        "user": USER_DATA
    }

@pytest.fixture
def random_test_data():
    """Generate random test data for each test"""
    return TestHelpers.generate_test_data()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot on failure"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)

def pytest_configure(config):
    """Configure pytest"""
    # Create reports directory
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
    
    # Set HTML report path with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    html_report_path = os.path.join(reports_dir, f"test_report_{timestamp}.html")
    config.option.htmlpath = html_report_path

def pytest_collection_modifyitems(config, items):
    """Modify test collection"""
    # Add markers based on test names
    for item in items:
        if "checkout" in item.name.lower():
            item.add_marker(pytest.mark.checkout)
        elif "wishlist" in item.name.lower():
            item.add_marker(pytest.mark.wishlist)
        elif "contact" in item.name.lower():
            item.add_marker(pytest.mark.contact)
        elif "login" in item.name.lower():
            item.add_marker(pytest.mark.login)

def pytest_html_report_title(report):
    """Customize HTML report title"""
    report.title = "E-commerce Automation Test Report"

@pytest.fixture(scope="session", autouse=True)
def test_session_setup():
    """Setup for entire test session"""
    print("\n" + "="*50)
    print("Starting E-commerce Automation Test Suite")
    print(f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)
    
    yield
    
    print("\n" + "="*50)
    print("E-commerce Automation Test Suite Completed")
    print(f"Test completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*50)