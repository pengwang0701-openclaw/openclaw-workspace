#!/usr/bin/env python3
"""
Take screenshots of web pages using Playwright.
Usage: python screenshot.py <url> [--output <path>] [--full-page]
"""

import argparse
import sys
from playwright.sync_api import sync_playwright


def take_screenshot(url: str, output: str = "screenshot.png", full_page: bool = True):
    """Take a screenshot of the given URL."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        page.screenshot(path=output, full_page=full_page)
        browser.close()
        print(f"Screenshot saved to: {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Take webpage screenshots")
    parser.add_argument("url", help="URL to screenshot")
    parser.add_argument("-o", "--output", default="screenshot.png", help="Output file path")
    parser.add_argument("--no-full-page", action="store_true", help="Capture viewport only")
    
    args = parser.parse_args()
    take_screenshot(args.url, args.output, full_page=not args.no_full_page)
