#!/usr/bin/env python3
"""
Scrape structured data from web pages using Playwright.
Usage: python scrape.py <url> --selector <css_selector> [--output <json_file>]
"""

import argparse
import json
import sys
from playwright.sync_api import sync_playwright


def scrape_page(url: str, selector: str, extract_attrs: list = None):
    """Extract data from page elements matching the selector."""
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url, wait_until="networkidle")
        
        # Wait for selector to be present
        page.wait_for_selector(selector)
        
        # Extract data
        if extract_attrs:
            data = page.eval_on_selector_all(
                selector,
                """(elements, attrs) => elements.map(e => {
                    const result = { text: e.textContent.trim() };
                    attrs.forEach(attr => {
                        if (e.hasAttribute(attr)) {
                            result[attr] = e.getAttribute(attr);
                        }
                    });
                    return result;
                })""",
                extract_attrs
            )
        else:
            data = page.eval_on_selector_all(
                selector,
                "elements => elements.map(e => e.textContent.trim())"
            )
        
        browser.close()
        return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape web page data")
    parser.add_argument("url", help="URL to scrape")
    parser.add_argument("-s", "--selector", required=True, help="CSS selector for target elements")
    parser.add_argument("-a", "--attrs", nargs="+", help="Attributes to extract")
    parser.add_argument("-o", "--output", help="Output JSON file (default: print to stdout)")
    
    args = parser.parse_args()
    
    data = scrape_page(args.url, args.selector, args.attrs)
    
    if args.output:
        with open(args.output, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"Data saved to: {args.output}")
    else:
        print(json.dumps(data, indent=2, ensure_ascii=False))
