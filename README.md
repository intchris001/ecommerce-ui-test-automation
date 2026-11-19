# E-commerce Automation Testing Framework

This is a comprehensive automation testing framework for e-commerce websites built with Python, Selenium, and pytest.

## Project Structure

```
automation_tests/
├── config/
│   ├── __init__.py
│   ├── config.py          # Test configuration settings
│   └── test_data.py       # Test data for various scenarios
├── pages/
│   ├── __init__.py
│   ├── base_page.py       # Base page class with common functionality
│   ├── checkout_page.py   # Checkout page object model
│   ├── contact_page.py    # Contact form page object model
│   ├── login_page.py      # Login page object model
│   └── wishlist_page.py   # Wishlist page object model
├── tests/
│   ├── __init__.py
│   ├── test_checkout.py   # Checkout functionality tests
│   ├── test_contact.py    # Contact form tests
│   └── test_wishlist.py   # Wishlist functionality tests
├── utils/
│   ├── __init__.py
│   ├── driver_manager.py  # WebDriver management utilities
│   └── helpers.py         # Helper functions and utilities
├── reports/               # Test reports directory
├── screenshots/           # Screenshots directory
├── conftest.py           # Pytest configuration and fixtures
├── pytest.ini           # Pytest settings
├── requirements.txt      # Python dependencies
├── run_tests.py         # Test runner script
└── README.md            # This file
```

## Features

- **Page Object Model (POM)**: Clean separation of test logic and page elements
- **Cross-browser Support**: Safari, Chrome, and Firefox
- **Parallel Execution**: Run tests in parallel for faster execution
- **HTML Reports**: Detailed HTML test reports with screenshots
- **Screenshot on Failure**: Automatic screenshots when tests fail
- **Flexible Test Selection**: Run specific test suites or individual tests
- **Data-driven Testing**: External test data configuration
- **Headless Mode**: Run tests without browser UI

## Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Web browsers (Safari, Chrome, Firefox)

## Installation

1. Navigate to the automation_tests directory:
   ```bash
   cd automation_tests
   ```

2. Install required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

### Test Configuration
Edit `config/config.py` to modify:
- Base URL of the e-commerce website
- Default browser settings
- Timeout values
- Screenshot and report paths

### Test Data
Edit `config/test_data.py` to modify:
- User registration data
- Checkout information
- Contact form data

## Running Tests

### Using the Test Runner Script

The easiest way to run tests is using the provided test runner:

```bash
# Run all tests
python run_tests.py

# Run specific test types
python run_tests.py --type smoke
python run_tests.py --type checkout
python run_tests.py --type wishlist
python run_tests.py --type contact
python run_tests.py --type regression

# Run with different browsers
python run_tests.py --browser chrome
python run_tests.py --browser firefox
python run_tests.py --browser safari

# Run in headless mode
python run_tests.py --headless

# Run tests in parallel
python run_tests.py --parallel

# Combine options
python run_tests.py --type smoke --browser chrome --headless
```

### Using pytest Directly

```bash
# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/test_checkout.py -v

# Run tests with specific markers
pytest -m smoke -v
pytest -m checkout -v
pytest -m wishlist -v
pytest -m contact -v

# Run with HTML report
pytest tests/ --html=reports/report.html --self-contained-html

# Run in parallel
pytest tests/ -n auto
```

## Test Categories

### Smoke Tests
Quick tests to verify basic functionality:
```bash
python run_tests.py --type smoke
```

### Checkout Tests
- Guest checkout process
- Invalid billing data handling
- Empty cart scenarios
- Multiple products checkout
- Form validation

### Wishlist Tests
- Add/remove products from wishlist
- Wishlist persistence
- Login requirements
- Multiple products handling

### Contact Form Tests
- Valid form submission
- Invalid email handling
- Empty field validation
- Long message handling
- Special characters testing
- Field limit validation

### Regression Tests
Comprehensive tests for regression testing:
```bash
python run_tests.py --type regression
```

## Test Reports

Test reports are automatically generated in the `reports/` directory:
- HTML reports with detailed test results
- Screenshots for failed tests
- Execution timestamps and duration

## Screenshots

Screenshots are automatically captured:
- On test failures (in `screenshots/` directory)
- At key verification points
- With timestamps for easy identification

## Browser Support

### Safari (Default)
- No additional setup required on macOS
- Ensure "Allow Remote Automation" is enabled in Safari's Develop menu

### Chrome
- Chrome browser must be installed
- ChromeDriver is managed automatically

### Firefox
- Firefox browser must be installed
- GeckoDriver is managed automatically

## Environment Variables

You can set environment variables to override default settings:

```bash
export BROWSER=chrome
export HEADLESS=true
export BASE_URL=https://your-ecommerce-site.com
```

## Troubleshooting

### Common Issues

1. **WebDriver Issues**
   - Ensure browsers are installed and up to date
   - Check that WebDriver permissions are granted

2. **Test Failures**
   - Check screenshots in the `screenshots/` directory
   - Review HTML reports for detailed error information
   - Verify the target website is accessible

3. **Permission Issues**
   - On macOS, you may need to grant accessibility permissions
   - Ensure Safari's "Allow Remote Automation" is enabled

### Debug Mode

Run tests with additional debugging:
```bash
pytest tests/ -v -s --tb=long
```

## Contributing

1. Follow the Page Object Model pattern
2. Add appropriate test markers (@pytest.mark.*)
3. Include docstrings with Test IDs
4. Take screenshots at verification points
5. Use the helper functions for common operations

## Test Data Management

- Use `TestHelpers.generate_test_data()` for random test data
- Define static test data in `config/test_data.py`
- Avoid hardcoding test data in test files

## Best Practices

1. **Test Independence**: Each test should be independent and not rely on other tests
2. **Clear Assertions**: Use descriptive assertion messages
3. **Page Object Model**: Keep page interactions in page object classes
4. **Wait Strategies**: Use explicit waits instead of sleep()
5. **Error Handling**: Include proper error handling and cleanup
6. **Documentation**: Document test cases with clear descriptions and Test IDs