"""
CakeResume Scraper
"""
import requests
import time
import random
import logging
from typing import List, Dict, Any
import yaml
from urllib.parse import quote
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class CakeResumeScraper:
    """CakeResume Job Scraper"""

    def __init__(self, config_path: str = "config/platforms.yaml"):
        # Load config to get keywords, but if fails, use defaults
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = yaml.safe_load(f)
        except:
            self.config = {}

        # Try to get keywords from config -> cakeresume -> keywords
        # If not found, use a default set relevant to the user
        self.keywords = self.config.get('cakeresume', {}).get('keywords', ["報關", "Import Export"])
        if not self.keywords:
             # Fallback to some defaults based on README
             self.keywords = ["報關", "Customs", "Import Export"]

        self.base_url = "https://www.cakeresume.com/jobs"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Accept-Language": "zh-TW,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        }

    def search_all(self) -> List[Dict[str, Any]]:
        """Search jobs for all keywords"""
        all_jobs = []
        for keyword in self.keywords:
            try:
                jobs = self.search_keyword(keyword)
                all_jobs.extend(jobs)
                # Random delay
                time.sleep(random.uniform(2, 5))
            except Exception as e:
                logger.error(f"Error searching CakeResume for {keyword}: {e}")

        # Deduplicate by ID
        seen_ids = set()
        unique_jobs = []
        for job in all_jobs:
            if job['id'] not in seen_ids:
                seen_ids.add(job['id'])
                unique_jobs.append(job)

        return unique_jobs

    def search_keyword(self, keyword: str) -> List[Dict[str, Any]]:
        """Search jobs for a specific keyword"""
        logger.info(f"Searching CakeResume for: {keyword}")

        results = []
        url = f"{self.base_url}?q={quote(keyword)}&refinementList%5Blang_name%5D%5B0%5D=Chinese&refinementList%5Blang_name%5D%5B1%5D=English"

        try:
            resp = requests.get(url, headers=self.headers, timeout=10)
            if resp.status_code != 200:
                logger.warning(f"Failed to fetch CakeResume: {resp.status_code}")
                return []

            soup = BeautifulSoup(resp.text, 'html.parser')

            # Select job items
            # The class names might change, but usually they are inside a container
            # We look for 'div' with class containing 'JobItem' or similar structure

            # Strategy: Look for links that contain '/companies/' and have title text
            # This is a bit heuristic but often more stable than specific class names

            job_cards = soup.find_all('div', class_=lambda x: x and 'JobSearchItem_wrapper' in x)

            if not job_cards:
                 # Fallback for other class names observed in CakeResume
                 job_cards = soup.find_all('div', class_=lambda x: x and 'JobItem_container' in x)

            logger.debug(f"Found {len(job_cards)} potential job cards")

            for card in job_cards:
                try:
                    # Title and URL
                    title_tag = card.find('a', class_=lambda x: x and 'JobSearchItem_jobTitle' in x)
                    if not title_tag:
                         title_tag = card.find('h3') # Sometimes it's in h3

                    if not title_tag:
                        continue

                    title = title_tag.get_text(strip=True)
                    link = title_tag.get('href')
                    if link and not link.startswith('http'):
                        link = f"https://www.cakeresume.com{link}"

                    # Company
                    company_tag = card.find('a', class_=lambda x: x and 'JobSearchItem_companyName' in x)
                    company = company_tag.get_text(strip=True) if company_tag else "Unknown"

                    # Location
                    # Usually in a specific div
                    location = "Taiwan" # Default
                    # Try to find location text

                    # Salary
                    # Try to find salary text
                    salary = None

                    # ID
                    # Extract from link
                    job_id = link.split('/')[-1] if link else f"cr_{hash(title)}"

                    job = {
                        'id': f"cr_{job_id}",
                        'title': title,
                        'company': company,
                        'location': location,
                        'salary': salary,
                        'url': link,
                        'source': 'CakeResume',
                        'description': '', # Details require visiting the page
                        'requirements': '',
                        'tags': []
                    }
                    results.append(job)

                except Exception as e:
                    logger.debug(f"Error parsing job card: {e}")
                    continue

        except Exception as e:
            logger.error(f"Exception during CakeResume search: {e}")

        logger.info(f"Found {len(results)} jobs on CakeResume for {keyword}")
        return results
