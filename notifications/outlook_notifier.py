"""
Send email notifications via Microsoft Outlook using Graph API and MSAL.
"""
import msal
import requests
import logging
import os
from dotenv import load_dotenv

load_dotenv()
logger = logging.getLogger("ComplianceAssistant.Notifier")

class OutlookNotifier:
    """Handles Outlook email notifications via Microsoft Graph API."""
    
    def __init__(self):
        """Initialize MSAL client and acquire token."""
        self.client_id = os.getenv("AZURE_CLIENT_ID")
        self.client_secret = os.getenv("AZURE_CLIENT_SECRET")
        self.tenant_id = os.getenv("AZURE_TENANT_ID")
        self.sender_email = os.getenv("SENDER_EMAIL")
        
        if not all([self.client_id, self.client_secret, self.tenant_id]):
            raise ValueError("Missing Azure AD credentials in environment variables")
        
        self.authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        self.scope = ["https://graph.microsoft.com/.default"]
        
        self.app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=self.authority,
            client_credential=self.client_secret
        )
        
        self.token = None
        self._acquire_token()
    
    def _acquire_token(self):
        """Acquire access token using client credentials flow."""
        try:
            result = self.app.acquire_token_for_client(scopes=self.scope)
            
            if "access_token" in result:
                self.token = result["access_token"]
                logger.info("Successfully acquired access token")
            else:
                error = result.get("error_description", result.get("error"))
                raise Exception(f"Failed to acquire token: {error}")
        
        except Exception as e:
            logger.error(f"Error acquiring token: {str(e)}")
            raise
    
    def send_email(self, to_email, subject, body_html):
        """
        Send email via Microsoft Graph API.
        
        Args:
            to_email: Recipient email address
            subject: Email subject line
            body_html: Email body in HTML format
        
        Returns:
            True if successful, False otherwise
        """
        try:
            endpoint = f"https://graph.microsoft.com/v1.0/users/{self.sender_email}/sendMail"
            
            headers = {
                "Authorization": f"Bearer {self.token}",
                "Content-Type": "application/json"
            }
            
            email_msg = {
                "message": {
                    "subject": subject,
                    "body": {
                        "contentType": "HTML",
                        "content": body_html
                    },
                    "toRecipients": [
                        {
                            "emailAddress": {
                                "address": to_email
                            }
                        }
                    ]
                },
                "saveToSentItems": "true"
            }
            
            response = requests.post(endpoint, headers=headers, json=email_msg)
            
            if response.status_code == 202:
                logger.info(f"Email sent successfully to {to_email}")
                return True
            else:
                logger.error(f"Failed to send email: {response.status_code} - {response.text}")
                return False
        
        except Exception as e:
            logger.error(f"Error sending email: {str(e)}")
            return False

def send_notification(to_email, subject, prerequisites, due_date):
    """
    Send compliance notification with prerequisites.
    
    Args:
        to_email: Recipient email
        subject: Email subject
        prerequisites: Prerequisites text
        due_date: Due date for compliance item
    """
    try:
        notifier = OutlookNotifier()
        
        # Create HTML email body
        body_html = f"""
        <html>
        <head>
            <style>
                body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
                .header {{ background-color: #0078d4; color: white; padding: 20px; }}
                .content {{ padding: 20px; }}
                .prerequisites {{ background-color: #f3f2f1; padding: 15px; border-left: 4px solid #0078d4; }}
                .footer {{ padding: 20px; font-size: 12px; color: #605e5c; }}
                .due-date {{ color: #d13438; font-weight: bold; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>New Compliance Item Assigned</h1>
            </div>
            <div class="content">
                <p>Hello,</p>
                <p>You have been assigned a new compliance item that requires your attention.</p>
                <p><strong>Due Date:</strong> <span class="due-date">{due_date}</span></p>
                
                <div class="prerequisites">
                    <h2>Prerequisites and Requirements:</h2>
                    <pre style="white-space: pre-wrap; font-family: 'Segoe UI', sans-serif;">{prerequisites}</pre>
                </div>
                
                <p>Please review the prerequisites above and take necessary actions to ensure compliance by the due date.</p>
                <p>If you have any questions or need clarification, please contact the compliance team.</p>
            </div>
            <div class="footer">
                <p>This is an automated message from the Compliance Assistant system.</p>
                <p>Please do not reply to this email.</p>
            </div>
        </body>
        </html>
        """
        
        # Send email
        success = notifier.send_email(to_email, subject, body_html)
        
        if not success:
            raise Exception("Failed to send notification email")
        
        logger.info(f"Notification sent to {to_email}")
    
    except Exception as e:
        logger.error(f"Error sending notification: {str(e)}")
        raise
