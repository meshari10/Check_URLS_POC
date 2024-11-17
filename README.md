# URL Reachability Checker with Screenshot Capture

This Python script checks the reachability of URLs from a file and captures a screenshot of each reachable website's homepage. It handles HTTP redirects and uses a headless Chrome browser for the screenshots.

---

## Features

- Checks if a list of URLs is reachable.
- Follows HTTP redirects and logs the final resolved URL.
- Captures a screenshot of each reachable website's homepage.
- Logs unreachable URLs for review.
- Automatically manages ChromeDriver compatibility with the installed Chrome version.
- Retry Logic: Automatically retries up to 3 times if a URL times out or encounters a network error.
- Timeout Support: Set timeout for URL requests and page load to ensure the script does not hang indefinitely.


---

## Prerequisites

1. **Python 3.7 or later** installed on your system.
2. **Google Chrome** installed.
   ```bash
   google-chrome --version
   ```
4. **Install Required Python Libraries**:
   Use pip to install dependencies:
   ```bash
   pip install selenium webdriver-manager requests
   ```
