
import unittest
from unittest.mock import MagicMock, patch
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.scrapers.scraper_cakeresume import CakeResumeScraper

class TestCakeResumeScraper(unittest.TestCase):
    @patch('src.scrapers.scraper_cakeresume.requests.get')
    def test_search_keyword(self, mock_get):
        """Test search_keyword"""
        scraper = CakeResumeScraper()

        # Mock HTML response
        mock_html = """
        <html>
            <div class="JobSearchItem_wrapper">
                <h3><a class="JobSearchItem_jobTitle" href="/companies/test/jobs/1">Test Job</a></h3>
                <a class="JobSearchItem_companyName">Test Company</a>
            </div>
        </html>
        """

        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.text = mock_html
        mock_get.return_value = mock_resp

        jobs = scraper.search_keyword("test")

        self.assertEqual(len(jobs), 1)
        self.assertEqual(jobs[0]['title'], "Test Job")
        self.assertEqual(jobs[0]['company'], "Test Company")
        self.assertTrue(jobs[0]['url'].endswith('/companies/test/jobs/1'))

if __name__ == '__main__':
    unittest.main()
