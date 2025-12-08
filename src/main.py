"""
Yusei Job Hunter - 主程式
每日自動搜尋職缺並生成報告
"""
import os
import sys
import json
import logging
from datetime import datetime
from typing import List, Dict, Any
from pathlib import Path

# 設定路徑
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.scrapers.scraper_104 import Platform104Scraper
from src.matcher.job_matcher import JobMatcher, MatchResult, batch_match

# 設定日誌
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler(PROJECT_ROOT / 'data' / 'job_hunter.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)


class JobHunter:
    """職缺獵人主程式"""

    def __init__(self):
        """初始化"""
        self.project_root = PROJECT_ROOT
        self.data_dir = self.project_root / 'data'
        self.reports_dir = self.project_root / 'reports'

        # 確保目錄存在
        self.data_dir.mkdir(exist_ok=True)
        self.reports_dir.mkdir(exist_ok=True)

        # 初始化元件
        self.matcher = JobMatcher(str(self.project_root / 'config' / 'profile.yaml'))

        logger.info("JobHunter 初始化完成")

    def run(self) -> Dict[str, Any]:
        """
        執行完整的職缺搜尋流程

        Returns:
            執行結果摘要
        """
        logger.info("=" * 50)
        logger.info("開始執行職缺搜尋")
        logger.info("=" * 50)

        start_time = datetime.now()
        results = {
            'date': start_time.strftime('%Y-%m-%d'),
            'start_time': start_time.isoformat(),
            'jobs_found': 0,
            'jobs_matched': 0,
            'high_matches': 0,
            'medium_matches': 0,
            'errors': []
        }

        all_jobs = []
        matched_results = []

        # 1. 爬取職缺
        logger.info("\n📥 步驟 1: 爬取職缺")

        # 104 人力銀行
        try:
            logger.info("搜尋 104 人力銀行...")
            scraper_104 = Platform104Scraper(str(self.project_root / 'config' / 'platforms.yaml'))
            jobs_104 = scraper_104.search_all()
            all_jobs.extend(jobs_104)
            logger.info(f"104 找到 {len(jobs_104)} 個職缺")
        except Exception as e:
            logger.error(f"104 爬取失敗: {e}")
            results['errors'].append(f"104: {str(e)}")

        # TODO: 加入其他平台爬蟲
        # - LinkedIn
        # - CakeResume
        # - Yourator

        results['jobs_found'] = len(all_jobs)
        logger.info(f"\n總共找到 {len(all_jobs)} 個職缺")

        # 2. 匹配職缺
        logger.info("\n🎯 步驟 2: 匹配職缺")
        matched_results = batch_match(all_jobs, str(self.project_root / 'config' / 'profile.yaml'))

        results['jobs_matched'] = len(matched_results)
        results['high_matches'] = len([r for r in matched_results if r.level == 'high'])
        results['medium_matches'] = len([r for r in matched_results if r.level == 'medium'])

        logger.info(f"匹配結果: {len(matched_results)} 個職缺")
        logger.info(f"  - 高度匹配: {results['high_matches']}")
        logger.info(f"  - 中度匹配: {results['medium_matches']}")

        # 3. 儲存資料
        logger.info("\n💾 步驟 3: 儲存資料")
        self._save_jobs(all_jobs)
        self._save_matches(matched_results)

        # 4. 生成報告
        logger.info("\n📊 步驟 4: 生成報告")
        report_path = self._generate_report(matched_results, results)
        results['report_path'] = str(report_path)

        # 5. 發送通知
        logger.info("\n📧 步驟 5: 發送通知")
        high_matches = [r for r in matched_results if r.level == 'high']
        if high_matches:
            self._send_notification(high_matches)
        else:
            logger.info("沒有高度匹配的職缺，不發送通知")

        # 完成
        end_time = datetime.now()
        results['end_time'] = end_time.isoformat()
        results['duration'] = str(end_time - start_time)

        logger.info("\n" + "=" * 50)
        logger.info("✅ 職缺搜尋完成")
        logger.info(f"耗時: {results['duration']}")
        logger.info("=" * 50)

        return results

    def _save_jobs(self, jobs: List[Dict[str, Any]]):
        """儲存職缺資料"""
        jobs_file = self.data_dir / 'jobs.json'

        # 讀取現有資料
        existing = []
        if jobs_file.exists():
            with open(jobs_file, 'r', encoding='utf-8') as f:
                existing = json.load(f)

        # 合併新資料（去重）
        existing_ids = {j.get('id') for j in existing}
        new_jobs = [j for j in jobs if j.get('id') not in existing_ids]

        # 更新時間戳記
        for job in new_jobs:
            job['added_date'] = datetime.now().isoformat()

        combined = existing + new_jobs

        # 儲存
        with open(jobs_file, 'w', encoding='utf-8') as f:
            json.dump(combined, f, ensure_ascii=False, indent=2)

        logger.info(f"儲存 {len(new_jobs)} 個新職缺，總共 {len(combined)} 個")

    def _save_matches(self, matches: List[MatchResult]):
        """儲存匹配結果"""
        matches_file = self.data_dir / f'matches_{datetime.now().strftime("%Y%m%d")}.json'

        data = [
            {
                'job_id': m.job_id,
                'title': m.title,
                'company': m.company,
                'location': m.location,
                'salary': m.salary,
                'url': m.url,
                'score': m.score,
                'level': m.level,
                'matched_skills': m.matched_skills,
                'matched_keywords': m.matched_keywords,
                'details': m.details
            }
            for m in matches
        ]

        with open(matches_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

        logger.info(f"儲存匹配結果至 {matches_file}")

    def _generate_report(self, matches: List[MatchResult], summary: Dict) -> Path:
        """生成每日報告"""
        date_str = datetime.now().strftime('%Y-%m-%d')
        report_file = self.reports_dir / f'daily_report_{date_str}.md'

        # 分類
        high = [m for m in matches if m.level == 'high']
        medium = [m for m in matches if m.level == 'medium']
        low = [m for m in matches if m.level == 'low']

        # 生成報告內容
        content = f"""# 📊 職缺報告 - {date_str}

## 📈 總覽

| 項目 | 數量 |
|------|------|
| 搜尋到的職缺 | {summary['jobs_found']} |
| 匹配的職缺 | {summary['jobs_matched']} |
| 🔥 高度匹配 | {len(high)} |
| ⭐ 中度匹配 | {len(medium)} |
| 📝 低度匹配 | {len(low)} |

---

## 🔥 高度匹配 (≥80%)

"""
        if high:
            for i, m in enumerate(high, 1):
                content += self._format_job(m, i)
        else:
            content += "_今日沒有高度匹配的職缺_\n\n"

        content += """
---

## ⭐ 中度匹配 (60-79%)

"""
        if medium:
            for i, m in enumerate(medium, 1):
                content += self._format_job(m, i)
        else:
            content += "_今日沒有中度匹配的職缺_\n\n"

        content += f"""
---

## 📝 執行資訊

- 開始時間: {summary.get('start_time', 'N/A')}
- 結束時間: {summary.get('end_time', 'N/A')}
- 耗時: {summary.get('duration', 'N/A')}

"""
        if summary.get('errors'):
            content += "### ⚠️ 錯誤\n\n"
            for error in summary['errors']:
                content += f"- {error}\n"

        # 寫入檔案
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(content)

        logger.info(f"報告已生成: {report_file}")
        return report_file

    def _format_job(self, match: MatchResult, index: int) -> str:
        """格式化單一職缺"""
        emoji = '🔥' if match.level == 'high' else '⭐' if match.level == 'medium' else '📝'

        return f"""### {index}. [{match.company}] {match.title}

- **匹配度**: {emoji} {match.score}%
- **地點**: {match.location}
- **薪資**: {match.salary or '面議'}
- **匹配技能**: {', '.join(match.matched_skills[:5]) if match.matched_skills else 'N/A'}
- **連結**: [{match.url}]({match.url})

---

"""

    def _send_notification(self, high_matches: List[MatchResult]):
        """發送通知（高度匹配職缺）"""
        # TODO: 實作 Email 和 LINE 通知

        logger.info(f"需要通知 {len(high_matches)} 個高度匹配職缺")

        # 簡易版本：輸出到 console
        print("\n" + "=" * 60)
        print("🔔 高度匹配職缺通知")
        print("=" * 60)

        for m in high_matches:
            print(f"\n🔥 [{m.score}%] {m.title}")
            print(f"   公司: {m.company}")
            print(f"   地點: {m.location}")
            print(f"   薪資: {m.salary or '面議'}")
            print(f"   連結: {m.url}")

        print("\n" + "=" * 60)


def main():
    """主程式進入點"""
    hunter = JobHunter()
    results = hunter.run()

    # 輸出結果摘要
    print("\n📊 執行結果摘要:")
    print(json.dumps(results, ensure_ascii=False, indent=2))

    return results


if __name__ == "__main__":
    main()
