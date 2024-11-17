#!/usr/bin/env python3
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException, TimeoutException
from webdriver_manager.chrome import ChromeDriverManager
import os
import requests
import argparse
import time

# ANSI escape codes for color
GREEN = '\033[32m'
BOLD_GREEN = '\033[1;32m'  # Bold Green for screenshot saved message
RED = '\033[31m'
YELLOW = '\033[33m'  # Yellow for retrying messages
RESET = '\033[0m'

def check_url_reachability_and_capture(file_path, output_dir="screenshots", max_retries=3, timeout=10):
    # Set up Selenium WebDriver with WebDriver Manager
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run browser in headless mode
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    
    # Automatically manage ChromeDriver
    driver_service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=driver_service, options=chrome_options)
    
    # Set window size to capture full-page screenshots
    driver.set_window_size(1920, 1080)  # You can adjust this as needed

    try:
        # Create output directory for screenshots if it doesn't exist
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Log file for reachable URLs
        log_file = os.path.join(output_dir, "reachable_urls.txt")

        # Read URLs from the file
        with open(file_path, 'r') as file:
            urls = [line.strip() for line in file if line.strip()]

        unreachable_urls = []

        # Open the log file to write reachable URLs
        with open(log_file, 'w') as log:
            total_urls = len(urls)

            for index, url in enumerate(urls, start=1):  # Start numbering URLs from 1
                retries = 0
                # Calculate progress percentage
                progress_percentage = (index / total_urls) * 100
                print(f"Checking URL #{index} of {total_urls} ({progress_percentage:.2f}%) : {url}")

                while retries < max_retries:
                    try:
                        # Allow redirects and set timeout for the HTTP request
                        response = requests.get(url, timeout=timeout, allow_redirects=True)

                        if response.status_code == 200:
                            print(f"{GREEN}Reachable: #{index} {url} (Final URL: {response.url}){RESET}")
                            log.write(f"#{index} Reachable: {url} -> Final URL: {response.url}\n")
                            
                            try:
                                # Load the final URL in Selenium and capture a screenshot
                                driver.get(response.url)
                                driver.set_page_load_timeout(timeout)  # Set page load timeout for Selenium
                                 
                                # Capture screenshot after the page is loaded
                                sanitized_url = response.url.replace('https://', '').replace('http://', '').replace('/', '_')
                                screenshot_path = os.path.join(output_dir, f"{sanitized_url}.png")
                                driver.save_screenshot(screenshot_path)
                                print(f"{BOLD_GREEN}Screenshot saved: {screenshot_path}{RESET}")
                                break  # Successfully handled the URL, exit retry loop
                            except TimeoutException:
                                print(f"{RED}Timeout while loading page for {url}{RESET}")
                                unreachable_urls.append(url)
                                break  # Exit retry loop after timeout
                            except WebDriverException as e:
                                print(f"Error capturing screenshot for {url}: {e}")
                                break  # Exit retry loop after error
                        else:
                            print(f"{RED}Unreachable (Status Code: {response.status_code}): #{index} {url}{RESET}")
                            unreachable_urls.append(url)
                            break  # Exit retry loop after an unreachable status code
                    except requests.exceptions.RequestException as e:
                        print(f"{RED}Unreachable (Error: {e}): #{index} {url}{RESET}")
                        if retries < max_retries - 1:
                            retries += 1
                            print(f"{YELLOW}Retrying URL #{index}: {url}... ({retries + 1}/{max_retries}){RESET}")
                            time.sleep(5)  # Wait before retrying
                        else:
                            unreachable_urls.append(url)
                            break  # Exit retry loop after max retries reached

        # Print summary of unreachable URLs
        if unreachable_urls:
            print("\nThe following URLs are not reachable, try manually:")
            for url in unreachable_urls:
                print(f"{RED}{url}{RESET}")
        else:
            print("\nAll URLs are reachable!")

    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Check URL reachability and capture screenshots.")
    parser.add_argument("file", help="Path to the file containing URLs")
    parser.add_argument("-o", "--output", default="screenshots", help="Output directory for screenshots")
    args = parser.parse_args()

    # Call the main function
    check_url_reachability_and_capture(args.file, args.output)
