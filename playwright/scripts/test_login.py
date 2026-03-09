#!/usr/bin/env python3
"""
Template for testing login flows with Playwright.
Usage: python test_login.py --url <login_page> --user <username> --pass <password>
"""

import argparse
import sys
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeout


def test_login(url: str, username: str, password: str, 
               user_selector: str = "input[name='username'], input[name='email'], #username, #email",
               pass_selector: str = "input[name='password'], input[type='password'], #password",
               submit_selector: str = "button[type='submit'], input[type='submit'], button:has-text('Login'), button:has-text('Sign in')"):
    """Test a login flow."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            # Navigate to login page
            print(f"Navigating to {url}...")
            page.goto(url, wait_until="networkidle")
            
            # Fill credentials
            print("Filling login form...")
            page.wait_for_selector(user_selector, timeout=5000)
            page.fill(user_selector, username)
            page.fill(pass_selector, password)
            
            # Submit
            print("Submitting form...")
            page.click(submit_selector)
            
            # Wait for navigation or error
            try:
                page.wait_for_load_state("networkidle", timeout=5000)
                current_url = page.url
                print(f"Login completed. Current URL: {current_url}")
                
                # Check for error messages
                error_selectors = [
                    ".error", ".alert", ".alert-danger", ".error-message",
                    "[role='alert']", ".login-error", ".auth-error"
                ]
                for sel in error_selectors:
                    try:
                        error = page.query_selector(sel)
                        if error and error.is_visible():
                            print(f"Error message found: {error.text_content()}")
                            return False
                    except:
                        pass
                
                return True
                
            except PlaywrightTimeout:
                print("Timeout waiting for page load")
                return False
                
        except Exception as e:
            print(f"Login test failed: {e}")
            # Take screenshot on failure
            page.screenshot(path="login_failure.png")
            print("Screenshot saved to login_failure.png")
            return False
            
        finally:
            browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Test login flow")
    parser.add_argument("--url", required=True, help="Login page URL")
    parser.add_argument("--user", "-u", required=True, help="Username")
    parser.add_argument("--pass", "-p", dest="password", required=True, help="Password")
    parser.add_argument("--user-selector", default="input[name='username'], input[name='email'], #username, #email")
    parser.add_argument("--pass-selector", default="input[name='password'], input[type='password'], #password")
    parser.add_argument("--submit-selector", default="button[type='submit'], input[type='submit']")
    
    args = parser.parse_args()
    
    success = test_login(
        args.url, args.user, args.password,
        args.user_selector, args.pass_selector, args.submit_selector
    )
    
    sys.exit(0 if success else 1)
