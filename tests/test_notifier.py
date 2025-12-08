
import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.notifier import EmailNotifier, LineNotifier

class TestNotifier(unittest.TestCase):
    @patch('src.notifier.notifier.smtplib.SMTP')
    def test_email_notifier(self, mock_smtp):
        """Test Email Notifier"""
        with patch.dict('os.environ', {
            'EMAIL_USER': 'test@example.com',
            'EMAIL_PASS': 'password',
            'SMTP_HOST': 'smtp.test.com'
        }):
            notifier = EmailNotifier()
            self.assertTrue(notifier.enabled)

            # Mock matches
            match = MagicMock()
            match.title = "Test Job"
            match.score = 90

            notifier.send([match])

            # Verify SMTP was called
            mock_smtp.assert_called_with('smtp.test.com', 587)
            instance = mock_smtp.return_value.__enter__.return_value
            instance.login.assert_called_with('test@example.com', 'password')
            instance.send_message.assert_called()

    @patch('src.notifier.notifier.requests.post')
    def test_line_notifier(self, mock_post):
        """Test LINE Notifier"""
        with patch.dict('os.environ', {'LINE_TOKEN': 'test_token'}):
            notifier = LineNotifier()
            self.assertTrue(notifier.enabled)

            # Mock matches
            match = MagicMock()
            match.title = "Test Job"
            match.score = 90
            match.company = "Test Corp"
            match.url = "http://test.com"

            mock_response = MagicMock()
            mock_response.status_code = 200
            mock_post.return_value = mock_response

            notifier.send([match])

            # Verify requests.post was called
            self.assertTrue(mock_post.called)
            args, kwargs = mock_post.call_args
            self.assertEqual(kwargs['headers']['Authorization'], 'Bearer test_token')

if __name__ == '__main__':
    unittest.main()
