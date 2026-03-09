---
name: playwright
description: Browser automation using Playwright for testing, scraping, screenshots, and web interaction. Use when: (1) automating browser actions like clicking, typing, navigation, (2) taking screenshots or recording videos of web pages, (3) extracting data from websites, (4) end-to-end testing of web applications, (5) filling and submitting forms automatically.
---

# Playwright Browser Automation

This skill provides browser automation capabilities using Microsoft Playwright.

## Quick Start

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
    browser.close()
```

## Common Patterns

### Screenshot
```python
page.screenshot(path="screenshot.png", full_page=True)
```

### Wait and Click
```python
page.wait_for_selector("button.submit")
page.click("button.submit")
```

### Extract Data
```python
data = page.eval_on_selector_all(".item", "elements => elements.map(e => e.textContent)")
```

### Fill Form
```python
page.fill("input[name='username']", "myuser")
page.fill("input[name='password']", "mypass")
page.click("button[type='submit']")
```

## Scripts

Use scripts in this skill for reusable automation tasks:

- `scripts/screenshot.py` - Take full-page or element screenshots
- `scripts/scrape.py` - Extract structured data from pages
- `scripts/test_login.py` - Login flow testing template

## Best Practices

1. Always use `wait_for_selector` before interacting with elements
2. Use `headless=False` for debugging, `headless=True` for production
3. Handle timeouts and retries for flaky operations
4. Close browsers properly to avoid resource leaks

## Installation

```bash
pip install playwright
playwright install chromium  # or firefox, webkit
```
