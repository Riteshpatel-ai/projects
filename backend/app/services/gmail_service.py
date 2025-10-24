"""
Gmail API Integration Service
"""
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
from app.core.config import settings

logger = logging.getLogger(__name__)


class GmailService:
    """Gmail API service for fetching and managing emails"""
    
    SCOPES = [
        'https://www.googleapis.com/auth/gmail.readonly',
        'https://www.googleapis.com/auth/gmail.modify'
    ]
    
    def __init__(self, credentials: Optional[Credentials] = None):
        """
        Initialize Gmail service
        
        Args:
            credentials: Google OAuth2 credentials
        """
        self.credentials = credentials
        self.service = None
        if credentials:
            # Ensure credentials are valid and refresh if expired (requires client_id/secret present)
            try:
                if getattr(self.credentials, 'expired', False) and getattr(self.credentials, 'refresh_token', None):
                    logger.info("Gmail credentials expired — attempting refresh")
                    try:
                        self.credentials.refresh(Request())
                        logger.info("Gmail credentials refreshed successfully")
                    except Exception as refresh_exc:
                        logger.exception("Failed to refresh Gmail credentials: %s", str(refresh_exc))
                        # Let the build fail below and surface the error when making API calls
                self.service = build('gmail', 'v1', credentials=self.credentials)
            except Exception as e:
                logger.exception("Failed to initialize Gmail API client: %s", str(e))
                self.service = None
    
    @staticmethod
    def get_authorization_url() -> str:
        """
        Get Gmail OAuth2 authorization URL
        
        Returns:
            str: Authorization URL for user to visit
        """
        # Validate client config
        if not settings.GMAIL_CLIENT_ID or not settings.GMAIL_CLIENT_SECRET:
            raise RuntimeError("GMAIL_CLIENT_ID and GMAIL_CLIENT_SECRET must be set in environment")

        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GMAIL_CLIENT_ID,
                    "client_secret": settings.GMAIL_CLIENT_SECRET,
                    "redirect_uris": [settings.GMAIL_REDIRECT_URI],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=GmailService.SCOPES,
            redirect_uri=settings.GMAIL_REDIRECT_URI
        )
        
        # Request only the explicitly declared scopes. Set include_granted_scopes=False
        # to avoid Google combining previously-granted scopes which can cause
        # "scope changed" errors when re-authorizing.
        auth_url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='false',
            prompt='consent'
        )
        
        return auth_url
    
    @staticmethod
    def exchange_code_for_token(code: str) -> Dict[str, Any]:
        """
        Exchange authorization code for access token
        
        Args:
            code: Authorization code from OAuth callback
            
        Returns:
            Dict containing token information
        """
        flow = Flow.from_client_config(
            {
                "web": {
                    "client_id": settings.GMAIL_CLIENT_ID,
                    "client_secret": settings.GMAIL_CLIENT_SECRET,
                    "redirect_uris": [settings.GMAIL_REDIRECT_URI],
                    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                    "token_uri": "https://oauth2.googleapis.com/token",
                }
            },
            scopes=GmailService.SCOPES,
            redirect_uri=settings.GMAIL_REDIRECT_URI
        )
        
        try:
            flow.fetch_token(code=code)
            credentials = flow.credentials

            return {
                "access_token": credentials.token,
                "refresh_token": credentials.refresh_token,
                "expiry": credentials.expiry.isoformat() if credentials.expiry else None
            }
        except Exception as e:
            logger.exception("Error exchanging code for token: %s", str(e))
            # Raise a clear error that will be logged by the route handler
            raise RuntimeError(f"Failed to fetch token from Google: {str(e)}")
    
    async def fetch_recent_emails(
        self, 
        max_results: int = 100,
        days: int = 7,
        query: str = ""
    ) -> List[Dict[str, Any]]:
        """
        Fetch recent emails from Gmail
        
        Args:
            max_results: Maximum number of emails to fetch
            days: Number of days to look back
            query: Gmail search query
            
        Returns:
            List of email dictionaries
        """
        if not self.service:
            logger.error("Gmail service not initialized — cannot fetch emails")
            return []
        
        try:
            # Calculate date filter
            after_date = (datetime.now() - timedelta(days=days)).strftime('%Y/%m/%d')
            search_query = f"after:{after_date}"
            if query:
                search_query += f" {query}"
            
            # Fetch message IDs
            results = self.service.users().messages().list(
                userId='me',
                maxResults=max_results,
                q=search_query
            ).execute()
            
            messages = results.get('messages', [])
            emails = []
            
            # Fetch full message details
            for msg in messages:
                try:
                    email_data = await self._get_email_details(msg['id'])
                    if email_data:
                        emails.append(email_data)
                except Exception as e:
                    logger.exception("Failed to fetch details for message %s: %s", msg.get('id'), str(e))
            
            logger.info(f"Fetched {len(emails)} emails from Gmail")
            return emails
            
        except Exception as e:
            logger.error(f"Error fetching emails: {str(e)}")
            return []
    
    async def _get_email_details(self, message_id: str) -> Optional[Dict[str, Any]]:
        """
        Get detailed information for a specific email
        
        Args:
            message_id: Gmail message ID
            
        Returns:
            Dictionary with email details
        """
        try:
            message = self.service.users().messages().get(
                userId='me',
                id=message_id,
                format='full'
            ).execute()
            
            headers = message['payload']['headers']
            header_dict = {h['name'].lower(): h['value'] for h in headers}
            
            # Extract email body
            body = self._extract_body(message['payload'])
            
            # Extract attachments info
            attachments = self._extract_attachments_info(message['payload'])
            
            email_data = {
                'gmail_id': message['id'],
                'thread_id': message.get('threadId'),
                'sender': header_dict.get('from', 'Unknown'),
                'recipient': header_dict.get('to', ''),
                'subject': header_dict.get('subject', 'No Subject'),
                'timestamp': datetime.fromtimestamp(int(message['internalDate']) / 1000),
                'content': body,
                'attachments': attachments,
                'labels': message.get('labelIds', [])
            }
            
            return email_data
            
        except Exception as e:
            logger.error(f"Error getting email details for {message_id}: {str(e)}")
            return None
    
    def _extract_body(self, payload: Dict) -> str:
        """Extract email body from payload"""
        if 'parts' in payload:
            for part in payload['parts']:
                if part['mimeType'] == 'text/plain':
                    data = part['body'].get('data', '')
                    if data:
                        return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        # Single part message
        if 'body' in payload and 'data' in payload['body']:
            data = payload['body']['data']
            return base64.urlsafe_b64decode(data).decode('utf-8', errors='ignore')
        
        return ""
    
    def _extract_attachments_info(self, payload: Dict) -> List[Dict[str, Any]]:
        """Extract attachment information"""
        attachments = []
        
        if 'parts' in payload:
            for part in payload['parts']:
                if part.get('filename'):
                    attachments.append({
                        'filename': part['filename'],
                        'mime_type': part['mimeType'],
                        'size': part['body'].get('size', 0)
                    })
        
        return attachments
    
    async def mark_as_read(self, message_id: str) -> bool:
        """Mark email as read"""
        try:
            self.service.users().messages().modify(
                userId='me',
                id=message_id,
                body={'removeLabelIds': ['UNREAD']}
            ).execute()
            return True
        except Exception as e:
            logger.error(f"Error marking email as read: {str(e)}")
            return False
