"""
Test runner script for e-commerce automation tests
"""
import os
import sys
import subprocess
import argparse
from datetime import datetime

def run_tests(test_type="all", browser="safari", headless=False, parallel=False):
    """
    Run automation tests with specified parameters
    
    Args:
        test_type: Type of tests to run (all, smoke, checkout, wishlist, contact, regression)
        browser: Browser to use (safari, chrome, firefox)
        headless: Run in headless mode
        parallel: Run tests in parallel
    """
    
    # Set environment variables
    os.environ["BROWSER"] = browser
    if headless:
        os.environ["HEADLESS"] = "true"
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add test selection based on type
    if test_type == "smoke":
        cmd.extend(["-m", "smoke"])
    elif test_type == "checkout":
        cmd.extend(["-m", "checkout"])
    elif test_type == "wishlist":
        cmd.extend(["-m", "wishlist"])
    elif test_type == "contact":
        cmd.extend(["-m", "contact"])
    elif test_type == "regression":
        cmd.extend(["-m", "regression"])
    elif test_type == "all":
        cmd.append("tests/")
    
    # Add parallel execution if requested
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # Add verbose output
    cmd.extend(["-v", "-s"])
    
    # Add HTML report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"reports/test_report_{timestamp}.html"
    cmd.extend(["--html", report_path, "--self-contained-html"])
    
    # Add test directory
    cmd.append("tests/")
    
    print(f"Running command: {' '.join(cmd)}")
    print(f"Test type: {test_type}")
    print(f"Browser: {browser}")
    print(f"Headless: {headless}")
    print(f"Parallel: {parallel}")
    print(f"Report will be saved to: {report_path}")
    print("-" * 50)
    
    # Run the tests
    try:
        result = subprocess.run(cmd, cwd=os.path.dirname(__file__))
        return result.returncode
    except KeyboardInterrupt:
        print("\nTests interrupted by user")
        return 1
    except Exception as e:
        print(f"Error running tests: {str(e)}")
        return 1

def main():
    """Main function to parse arguments and run tests"""
    parser = argparse.ArgumentParser(description="Run e-commerce automation tests")
    
    parser.add_argument(
        "--type", 
        choices=["all", "smoke", "checkout", "wishlist", "contact", "regression"],
        default="all",
        help="Type of tests to run (default: all)"
    )
    
    parser.add_argument(
        "--browser",
        choices=["safari", "chrome", "firefox"],
        default="safari",
        help="Browser to use for testing (default: safari)"
    )
    
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run tests in headless mode"
    )
    
    parser.add_argument(
        "--parallel",
        action="store_true",
        help="Run tests in parallel"
    )
    
    args = parser.parse_args()
    
    print("E-commerce Automation Test Runner")
    print("=" * 40)
    
    # Run the tests
    exit_code = run_tests(
        test_type=args.type,
        browser=args.browser,
        headless=args.headless,
        parallel=args.parallel
    )
    
    sys.exit(exit_code)

if __name__ == "__main__":
    main()