#!/usr/bin/env python3
"""
Gmail Puller - Automatically checks for new emails every minute
"""

import os
import time
import logging
from datetime import datetime
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gmail API scope
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# Configuration
CHECK_INTERVAL = int(os.getenv('CHECK_INTERVAL', 60))
GMAIL_LABELS = os.getenv('GMAIL_LABELS', 'INBOX').split(',')
MAX_MESSAGES = int(os.getenv('MAX_MESSAGES', 10))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def get_gmail_service():
    """
    Authenticate and return Gmail API service instance.
    """
    creds = None
    token_path = Path('token.json')
    credentials_path = Path('credentials.json')

    # Check if credentials.json exists
    if not credentials_path.exists():
        logger.error("credentials.json not found. Please download it from Google Cloud Console.")
        raise FileNotFoundError(
            "credentials.json is required. "
            "Download it from https://console.cloud.google.com/apis/credentials"
        )

    # Load saved credentials
    if token_path.exists():
        creds = Credentials.from_authorized_user_file(str(token_path), SCOPES)

    # If no valid credentials, let user log in
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            logger.info("Refreshing access token...")
            creds.refresh(Request())
        else:
            logger.info("Starting OAuth flow...")
            flow = InstalledAppFlow.from_client_secrets_file(
                str(credentials_path), SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        # Save credentials for next run
        with open(token_path, 'w') as token:
            token.write(creds.to_json())
        logger.info("Credentials saved to token.json")

    return build('gmail', 'v1', credentials=creds)


def check_new_emails(service):
    """
    Check for new emails in specified labels.
    """
    try:
        # Query for unread messages in specified labels
        query_parts = []
        for label in GMAIL_LABELS:
            query_parts.append(f'label:{label.strip()}')
        query_parts.append('is:unread')
        query = ' '.join(query_parts)

        logger.info(f"Checking for new emails with query: {query}")
        
        # Get list of messages
        results = service.users().messages().list(
            userId='me',
            q=query,
            maxResults=MAX_MESSAGES
        ).execute()
        
        messages = results.get('messages', [])
        
        if not messages:
            logger.info("No new unread messages found.")
            return 0
        
        logger.info(f"Found {len(messages)} unread message(s)")
        
        # Get details for each message
        for msg in messages:
            try:
                message = service.users().messages().get(
                    userId='me',
                    id=msg['id'],
                    format='metadata',
                    metadataHeaders=['From', 'Subject', 'Date']
                ).execute()
                
                headers = message.get('payload', {}).get('headers', [])
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), 'No Subject')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), 'Unknown')
                date = next((h['value'] for h in headers if h['name'] == 'Date'), 'Unknown')
                
                logger.info(f"  - From: {sender}")
                logger.info(f"    Subject: {subject}")
                logger.info(f"    Date: {date}")
                
            except HttpError as error:
                logger.error(f"Error fetching message {msg['id']}: {error}")
        
        return len(messages)
        
    except HttpError as error:
        logger.error(f"An error occurred while checking emails: {error}")
        return 0


def main():
    """
    Main function to run the Gmail puller continuously.
    """
    logger.info("=" * 60)
    logger.info("Gmail Puller Started")
    logger.info(f"Check interval: {CHECK_INTERVAL} seconds")
    logger.info(f"Monitoring labels: {', '.join(GMAIL_LABELS)}")
    logger.info(f"Max messages per check: {MAX_MESSAGES}")
    logger.info("=" * 60)
    
    try:
        # Initialize Gmail service
        service = get_gmail_service()
        logger.info("Successfully authenticated with Gmail API")
        
        # Main loop
        check_count = 0
        while True:
            check_count += 1
            logger.info(f"\n--- Check #{check_count} at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
            
            try:
                new_emails = check_new_emails(service)
                logger.info(f"Check completed. Found {new_emails} new email(s).")
            except Exception as e:
                logger.error(f"Error during email check: {e}")
            
            logger.info(f"Waiting {CHECK_INTERVAL} seconds until next check...")
            time.sleep(CHECK_INTERVAL)
            
    except KeyboardInterrupt:
        logger.info("\nGmail Puller stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise


if __name__ == '__main__':
    main()
