"""
104 人力銀行爬蟲
"""
import requests
from bs4 import BeautifulSoup
import time
import random
import logging
from typing import List, Dict, Any, Optional
import yaml
import re
import json

logger = logging.getLogger(__name__)


class Platform104Scraper:
    """104 人力銀行職缺爬蟲"""

    BASE_URL = "https://www.104.com.tw"
    SEARCH_API = "https://www.104.com.tw/jobs/search/list"

    def __init__(self, config_path: str = "config/platforms.yaml"):
        """
        初始化爬蟲

        Args:
            config_path: 平台配置檔路徑
        """
        with open(config_path, 'r', encoding='utf-8') as f:
            platforms = yaml.safe_load(f)

        self.config = platforms.get('platforms', {}).get('platform_104', {})
        self.scraper_settings = platforms.get('scraper_settings', {})

        self.session = requests.Session()
        self._setup_session()

        logger.info("104 爬蟲初始化完成")

    def _setup_session(self):
        """設定 Session"""
        user_agents = self.scraper_settings.get('user_agents', [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        ])

        self.session.headers.update({
            'User-Agent': random.choice(user_agents),
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'zh-TW,zh;q=0.9,en;q=0.8',
            'Referer': 'https://www.104.com.tw/jobs/search/',
        })

    def search(self, keyword: str, **kwargs) -> List[Dict[str, Any]]:
        """
        搜尋職缺

        Args:
            keyword: 搜尋關鍵字
            **kwargs: 其他搜尋參數

        Returns:
            職缺列表
        """
        jobs = []
        max_pages = self.config.get('scraper', {}).get('max_pages', 5)
        delay = self.config.get('scraper', {}).get('delay', 2)

        for page in range(1, max_pages + 1):
            logger.info(f"搜尋 '{keyword}' - 第 {page} 頁")

            try:
                page_jobs = self._search_page(keyword, page, **kwargs)
                if not page_jobs:
                    break

                jobs.extend(page_jobs)

                # 隨機延遲，避免被封鎖
                time.sleep(delay + random.uniform(0, 1))

            except Exception as e:
                logger.error(f"搜尋第 {page} 頁時發生錯誤: {e}")
                break

        logger.info(f"關鍵字 '{keyword}' 共找到 {len(jobs)} 個職缺")
        return jobs

    def _search_page(self, keyword: str, page: int = 1, **kwargs) -> List[Dict[str, Any]]:
        """搜尋單一頁面"""
        params = {
            'ro': 0,           # 全部工作
            'keyword': keyword,
            'order': 12,       # 依最新排序
            'asc': 0,          # 降序
            'page': page,
            'mode': 's',       # 搜尋模式
            'jobsource': '2018indexpoc',
        }

        # 加入自訂參數
        config_params = self.config.get('params', {})
        if 'area' in config_params:
            params['area'] = config_params['area']
        if 'jobexp' in config_params:
            params['jobexp'] = config_params['jobexp']

        params.update(kwargs)

        try:
            response = self.session.get(
                self.SEARCH_API,
                params=params,
                timeout=self.scraper_settings.get('timeout', 30)
            )
            response.raise_for_status()

            data = response.json()
            return self._parse_jobs(data)

        except requests.RequestException as e:
            logger.error(f"請求失敗: {e}")
            return []
        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失敗: {e}")
            return []

    def _parse_jobs(self, data: Dict) -> List[Dict[str, Any]]:
        """解析職缺資料"""
        jobs = []

        job_list = data.get('data', {}).get('list', [])

        for item in job_list:
            try:
                job = {
                    'id': f"104_{item.get('jobNo', '')}",
                    'title': item.get('jobName', ''),
                    'company': item.get('custName', ''),
                    'location': item.get('jobAddrNo498', ''),
                    'salary': item.get('salaryDesc', ''),
                    'url': f"https://www.104.com.tw/job/{item.get('link', {}).get('job', '')}",
                    'description': item.get('jobContent', ''),
                    'requirements': '',
                    'tags': item.get('tags', []),
                    'source': '104',
                    'posted_date': item.get('appearDate', ''),
                    'raw': item
                }

                # 提取更多資訊
                if item.get('s10'):
                    job['experience_required'] = item['s10']
                if item.get('s11'):
                    job['education_required'] = item['s11']

                jobs.append(job)

            except Exception as e:
                logger.warning(f"解析職缺時發生錯誤: {e}")
                continue

        return jobs

    def get_job_detail(self, job_url: str) -> Optional[Dict[str, Any]]:
        """
        取得職缺詳細資訊

        Args:
            job_url: 職缺 URL

        Returns:
            職缺詳細資料
        """
        try:
            # 從 URL 提取 job code
            match = re.search(r'/job/([a-zA-Z0-9]+)', job_url)
            if not match:
                return None

            job_code = match.group(1)
            detail_url = f"https://www.104.com.tw/job/ajax/content/{job_code}"

            response = self.session.get(
                detail_url,
                timeout=self.scraper_settings.get('timeout', 30)
            )
            response.raise_for_status()

            data = response.json()

            return {
                'description': data.get('data', {}).get('jobDetail', {}).get('jobDescription', ''),
                'requirements': data.get('data', {}).get('condition', {}).get('other', ''),
                'benefits': data.get('data', {}).get('welfare', {}).get('welfare', ''),
                'company_info': data.get('data', {}).get('custInfo', {}),
            }

        except Exception as e:
            logger.error(f"取得職缺詳細資訊失敗: {e}")
            return None

    def search_all(self) -> List[Dict[str, Any]]:
        """
        執行所有預設搜尋

        Returns:
            所有職缺（已去重）
        """
        all_jobs = []
        seen_ids = set()

        queries = self.config.get('search_queries', [])

        for query in queries:
            keyword = query.get('keywords', '')
            if not keyword:
                continue

            logger.info(f"搜尋關鍵字: {keyword}")
            jobs = self.search(keyword)

            # 去重
            for job in jobs:
                if job['id'] not in seen_ids:
                    seen_ids.add(job['id'])
                    all_jobs.append(job)

        logger.info(f"總共找到 {len(all_jobs)} 個不重複職缺")
        return all_jobs


if __name__ == "__main__":
    # 測試
    logging.basicConfig(level=logging.INFO)

    scraper = Platform104Scraper()

    # 測試單一關鍵字
    jobs = scraper.search("報關 半導體")

    for job in jobs[:5]:
        print(f"\n職缺: {job['title']}")
        print(f"公司: {job['company']}")
        print(f"地點: {job['location']}")
        print(f"薪資: {job['salary']}")
        print(f"連結: {job['url']}")
