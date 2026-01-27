#!/usr/bin/env python3
"""
Gmail Puller - Automatically clicks "Fetch emails now" button every minute
This script logs into Gmail and clicks the button to fetch emails from external accounts.
"""

import os
import time
import logging
from datetime import datetime
from dotenv import load_dotenv

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

# Load environment variables
load_dotenv()

# Configuration
GMAIL_EMAIL = os.getenv('GMAIL_EMAIL', '')
GMAIL_PASSWORD = os.getenv('GMAIL_PASSWORD', '')
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 60))
GMAIL_ACCOUNT_INDEX = int(os.getenv('GMAIL_ACCOUNT_INDEX', 0))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
HEADLESS = os.getenv('HEADLESS', 'true').lower() == 'true'

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def setup_driver():
    """
    Setup and return Chrome WebDriver with appropriate options.
    """
    chrome_options = Options()
    
    if HEADLESS:
        chrome_options.add_argument('--headless=new')
        chrome_options.add_argument('--disable-gpu')
    
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')
    
    # Add preferences to keep user logged in
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    
    # Use user data directory to persist session
    chrome_options.add_argument('--user-data-dir=/tmp/chrome-profile')
    
    logger.info("Setting up Chrome WebDriver...")
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.set_page_load_timeout(30)
    
    return driver


def login_to_gmail(driver):
    """
    Log into Gmail using provided credentials.
    """
    logger.info("Attempting to log into Gmail...")
    
    try:
        # Navigate to Gmail
        driver.get('https://mail.google.com')
        time.sleep(3)
        
        # Check if already logged in
        try:
            driver.find_element(By.XPATH, "//a[@aria-label='Google-Konto']")
            logger.info("Already logged in to Gmail")
            return True
        except NoSuchElementException:
            logger.info("Not logged in, proceeding with login...")
        
        # Enter email
        try:
            email_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, "identifierId"))
            )
            email_field.clear()
            email_field.send_keys(GMAIL_EMAIL)
            
            next_button = driver.find_element(By.ID, "identifierNext")
            next_button.click()
            logger.info("Email entered, waiting for password page...")
            time.sleep(3)
        except TimeoutException:
            logger.warning("Email field not found, might already be logged in")
            return True
        
        # Enter password
        try:
            password_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.NAME, "Passwd"))
            )
            password_field.clear()
            password_field.send_keys(GMAIL_PASSWORD)
            
            next_button = driver.find_element(By.ID, "passwordNext")
            next_button.click()
            logger.info("Password entered, waiting for login to complete...")
            time.sleep(5)
        except TimeoutException:
            logger.error("Password field not found")
            return False
        
        # Wait for Gmail to load
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//a[@aria-label='Google-Konto']"))
        )
        logger.info("Successfully logged into Gmail")
        return True
        
    except Exception as e:
        logger.error(f"Error during login: {e}")
        return False


def click_fetch_emails_button(driver):
    """
    Navigate to Gmail settings and click the "Fetch emails now" button.
    """
    try:
        # Navigate to accounts settings page
        settings_url = f'https://mail.google.com/mail/u/{GMAIL_ACCOUNT_INDEX}/#settings/accounts'
        logger.info(f"Navigating to settings page: {settings_url}")
        driver.get(settings_url)
        time.sleep(5)
        
        # Try multiple possible button texts and selectors
        button_texts = [
            "Jetzt E-Mails abrufen",  # German
            "Fetch mail now",          # English
            "Nachricht jetzt abrufen", # Alternative German
            "Get mail now"             # Alternative English
        ]
        
        button_found = False
        
        # Try to find button by text
        for button_text in button_texts:
            try:
                logger.info(f"Looking for button with text: {button_text}")
                
                # Try different XPath strategies
                xpaths = [
                    f"//button[contains(text(), '{button_text}')]",
                    f"//input[@type='button' and contains(@value, '{button_text}')]",
                    f"//div[contains(text(), '{button_text}')]/ancestor::button",
                    f"//*[contains(text(), '{button_text}')]",
                ]
                
                for xpath in xpaths:
                    try:
                        button = WebDriverWait(driver, 5).until(
                            EC.element_to_be_clickable((By.XPATH, xpath))
                        )
                        button.click()
                        logger.info(f"✓ Successfully clicked '{button_text}' button!")
                        button_found = True
                        break
                    except TimeoutException:
                        continue
                
                if button_found:
                    break
                    
            except Exception as e:
                logger.debug(f"Button '{button_text}' not found: {e}")
                continue
        
        if not button_found:
            logger.warning("Could not find 'Fetch emails now' button. It may not be available on this account.")
            logger.info("This feature requires having external email accounts configured in Gmail settings.")
            return False
        
        time.sleep(2)
        return True
        
    except Exception as e:
        logger.error(f"Error while trying to click fetch button: {e}")
        return False


def main():
    """
    Main function to run the Gmail puller continuously.
    """
    logger.info("=" * 60)
    logger.info("Gmail Puller Started")
    logger.info(f"Email: {GMAIL_EMAIL}")
    logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
    logger.info(f"Gmail account index: {GMAIL_ACCOUNT_INDEX}")
    logger.info(f"Headless mode: {HEADLESS}")
    logger.info("=" * 60)
    
    # Validate credentials
    if not GMAIL_EMAIL or not GMAIL_PASSWORD:
        logger.error("GMAIL_EMAIL and GMAIL_PASSWORD must be set in .env file")
        logger.error("Please copy .env.example to .env and configure your credentials")
        return
    
    driver = None
    
    try:
        # Setup driver
        driver = setup_driver()
        
        # Login to Gmail (only needed once, session persists)
        if not login_to_gmail(driver):
            logger.error("Failed to login to Gmail")
            return
        
        # Main loop
        check_count = 0
        while True:
            check_count += 1
            logger.info(f"\n--- Check #{check_count} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
            
            try:
                success = click_fetch_emails_button(driver)
                if success:
                    logger.info("✓ Email fetch triggered successfully")
                else:
                    logger.warning("✗ Failed to trigger email fetch")
            except Exception as e:
                logger.error(f"Error during check: {e}")
                # Try to recover by logging in again
                try:
                    logger.info("Attempting to recover session...")
                    login_to_gmail(driver)
                except Exception as recovery_error:
                    logger.error(f"Recovery failed: {recovery_error}")
            
            logger.info(f"Waiting {CHECK_INTERVAL} seconds until next check...")
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("\nGmail Puller stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise
    finally:
        if driver:
            logger.info("Closing browser...")
            driver.quit()


if __name__ == '__main__':
    main()
