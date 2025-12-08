"""
Email 通知模組
"""
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List
import logging
from dotenv import load_dotenv

from src.matcher.job_matcher import MatchResult

load_dotenv()
logger = logging.getLogger(__name__)


class EmailNotifier:
    """Email 通知器"""

    def __init__(self):
        """初始化"""
        self.email_user = os.getenv('EMAIL_USER')
        self.email_pass = os.getenv('EMAIL_PASS')
        self.email_to = os.getenv('EMAIL_TO', self.email_user)
        self.smtp_host = os.getenv('SMTP_HOST', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))

    def send(self, matches: List[MatchResult]):
        """
        發送通知

        Args:
            matches: 高度匹配的職缺列表
        """
        if not all([self.email_user, self.email_pass]):
            logger.warning("Email 通知未設定，跳過寄送")
            return

        if not matches:
            logger.info("沒有需要通知的職缺")
            return

        subject = f"🚀 Yusei Job Hunter - {len(matches)} 個新職缺通知"
        html_content = self._build_html(matches)

        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = self.email_user
        msg['To'] = self.email_to

        part = MIMEText(html_content, 'html')
        msg.attach(part)

        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_pass)
                server.sendmail(self.email_user, self.email_to, msg.as_string())
            logger.info(f"Email 通知已成功寄送至 {self.email_to}")
        except Exception as e:
            logger.error(f"Email 寄送失敗: {e}")

    def _build_html(self, matches: List[MatchResult]) -> str:
        """建立 HTML 郵件內容"""
        html = "<html><body>"
        html += f"<h1>🔥 Yusei Job Hunter 為您找到 {len(matches)} 個高度匹配新職缺！</h1>"

        for m in matches:
            html += f"""
            <div style="border-bottom: 1px solid #eee; padding: 10px;">
                <h3><a href="{m.url}">【{m.company}】{m.title}</a></h3>
                <p>
                    <b>匹配度:</b> {m.score}%<br>
                    <b>地點:</b> {m.location}<br>
                    <b>薪資:</b> {m.salary or '面議'}<br>
                    <b>匹配技能:</b> {', '.join(m.matched_skills[:5]) if m.matched_skills else 'N/A'}
                </p>
            </div>
            """
        html += "</body></html>"
        return html
