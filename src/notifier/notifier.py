"""
Notification module for Yusei Job Hunter.
Handles sending notifications via Email and LINE.
"""
import os
import smtplib
import logging
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List, Dict, Any, Optional

logger = logging.getLogger(__name__)

class Notifier:
    """Base class for notifiers"""
    def send(self, matches: List[Any]):
        raise NotImplementedError

class EmailNotifier(Notifier):
    """Email Notifier"""
    def __init__(self):
        self.user = os.environ.get('EMAIL_USER')
        self.password = os.environ.get('EMAIL_PASS')
        self.host = os.environ.get('SMTP_HOST', 'smtp.gmail.com')
        self.port = int(os.environ.get('SMTP_PORT', 587))

        if not self.user or not self.password:
            logger.warning("Email credentials not found. Email notifications will be disabled.")
            self.enabled = False
        else:
            self.enabled = True

    def send(self, matches: List[Any]):
        """Send email with matched jobs"""
        if not self.enabled or not matches:
            return

        try:
            msg = MIMEMultipart()
            msg['From'] = self.user
            msg['To'] = self.user  # Send to self by default
            msg['Subject'] = f"Job Hunter Report: {len(matches)} High Matches Found"

            body = self._format_body(matches)
            msg.attach(MIMEText(body, 'html'))

            with smtplib.SMTP(self.host, self.port) as server:
                server.starttls()
                server.login(self.user, self.password)
                server.send_message(msg)

            logger.info(f"Email sent successfully to {self.user}")

        except Exception as e:
            logger.error(f"Failed to send email: {e}")

    def _format_body(self, matches: List[Any]) -> str:
        """Format the email body as HTML"""
        html = "<h2>🔥 High Match Jobs Found</h2>"
        html += "<ul>"
        for m in matches:
            html += f"""
            <li>
                <strong>[{m.score}%] {m.title}</strong><br>
                Company: {m.company}<br>
                Location: {m.location}<br>
                Salary: {m.salary or 'Negotiable'}<br>
                <a href="{m.url}">View Job</a>
            </li>
            <br>
            """
        html += "</ul>"
        return html

class LineNotifier(Notifier):
    """LINE Notify Notifier"""
    def __init__(self):
        self.token = os.environ.get('LINE_TOKEN')
        self.api_url = 'https://notify-api.line.me/api/notify'

        if not self.token:
            logger.warning("LINE token not found. LINE notifications will be disabled.")
            self.enabled = False
        else:
            self.enabled = True

    def send(self, matches: List[Any]):
        """Send LINE notification"""
        if not self.enabled or not matches:
            return

        try:
            # LINE Notify has a character limit (1000), so we might need to truncate or send summary
            # Sending a summary first
            summary = f"\n🔥 Found {len(matches)} high match jobs!"
            self._send_message(summary)

            # Send top 3 matches individually to avoid hitting limits
            for i, m in enumerate(matches[:3]):
                msg = (
                    f"\nTop {i+1}: {m.title}\n"
                    f"Company: {m.company}\n"
                    f"Score: {m.score}%\n"
                    f"Link: {m.url}"
                )
                self._send_message(msg)

            if len(matches) > 3:
                self._send_message(f"\n...and {len(matches) - 3} more. Check your email/report.")

            logger.info("LINE notifications sent successfully")

        except Exception as e:
            logger.error(f"Failed to send LINE notification: {e}")

    def _send_message(self, message: str):
        headers = {'Authorization': f'Bearer {self.token}'}
        payload = {'message': message}
        response = requests.post(self.api_url, headers=headers, data=payload)
        response.raise_for_status()
