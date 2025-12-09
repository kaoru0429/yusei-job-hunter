"""
職缺媒合引擎 - 根據 Yusei 的專長計算匹配度
"""
import yaml
import re
from fuzzywuzzy import fuzz
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class MatchResult:
    """匹配結果"""
    job_id: str
    title: str
    company: str
    location: str
    salary: Optional[str]
    url: str
    score: int
    level: str  # high, medium, low
    matched_skills: List[str]
    matched_keywords: List[str]
    details: Dict[str, Any]


class JobMatcher:
    """職缺媒合引擎"""
<<<<<<< HEAD
    
    def __init__(self, profile_path: str = "config/profile.yaml"):
        """
        初始化媒合引擎
        
=======

    def __init__(self, profile_path: str = "config/profile.yaml"):
        """
        初始化媒合引擎

>>>>>>> origin/setup-job-hunter-project
        Args:
            profile_path: 個人專長配置檔路徑
        """
        with open(profile_path, 'r', encoding='utf-8') as f:
            self.profile = yaml.safe_load(f)
<<<<<<< HEAD
            
=======

>>>>>>> origin/setup-job-hunter-project
        self.core_skills = self.profile.get('core_skills', {})
        self.industry_exp = self.profile.get('industry_experience', [])
        self.certifications = self.profile.get('certifications', [])
        self.target_positions = self.profile.get('target_positions', {})
        self.search_criteria = self.profile.get('search_criteria', {})
        self.exclusions = self.profile.get('exclusions', {})
        self.matching_rules = self.profile.get('matching_rules', {})
<<<<<<< HEAD
        
        logger.info("JobMatcher 初始化完成")
        
    def match(self, job: Dict[str, Any]) -> Optional[MatchResult]:
        """
        計算單一職缺的匹配度
        
        Args:
            job: 職缺資料字典
            
=======

        logger.info("JobMatcher 初始化完成")

    def match(self, job: Dict[str, Any]) -> Optional[MatchResult]:
        """
        計算單一職缺的匹配度

        Args:
            job: 職缺資料字典

>>>>>>> origin/setup-job-hunter-project
        Returns:
            MatchResult 或 None（如果被排除）
        """
        # 1. 檢查排除條件
        if self._should_exclude(job):
            logger.debug(f"職缺被排除: {job.get('title')}")
            return None
<<<<<<< HEAD
            
=======

>>>>>>> origin/setup-job-hunter-project
        # 2. 計算基礎分數
        score = 0
        matched_skills = []
        matched_keywords = []
        details = {}
<<<<<<< HEAD
        
        job_text = self._get_job_text(job)
        
=======

        job_text = self._get_job_text(job)

>>>>>>> origin/setup-job-hunter-project
        # 3. 核心技能匹配
        skill_score, skill_matches = self._match_core_skills(job_text)
        score += skill_score
        matched_skills.extend(skill_matches)
        details['skill_score'] = skill_score
<<<<<<< HEAD
        
=======

>>>>>>> origin/setup-job-hunter-project
        # 4. 產業經驗匹配
        industry_score, industry_matches = self._match_industry(job)
        score += industry_score
        matched_keywords.extend(industry_matches)
        details['industry_score'] = industry_score
<<<<<<< HEAD
        
=======

>>>>>>> origin/setup-job-hunter-project
        # 5. 目標職位匹配
        position_score = self._match_target_position(job)
        score += position_score
        details['position_score'] = position_score
<<<<<<< HEAD
        
=======

>>>>>>> origin/setup-job-hunter-project
        # 6. 地點匹配
        location_score = self._match_location(job)
        score += location_score
        details['location_score'] = location_score
<<<<<<< HEAD
        
=======

>>>>>>> origin/setup-job-hunter-project
        # 7. 薪資檢查
        salary_score = self._check_salary(job)
        score += salary_score
        details['salary_score'] = salary_score
<<<<<<< HEAD
        
=======

>>>>>>> origin/setup-job-hunter-project
        # 8. 認證匹配加分
        cert_score = self._match_certifications(job_text)
        score += cert_score
        details['cert_score'] = cert_score
<<<<<<< HEAD
        
=======

>>>>>>> origin/setup-job-hunter-project
        # 9. 確定匹配等級
        thresholds = self.matching_rules.get('thresholds', {})
        if score >= thresholds.get('high', 80):
            level = 'high'
        elif score >= thresholds.get('medium', 60):
            level = 'medium'
        elif score >= thresholds.get('low', 40):
            level = 'low'
        else:
            return None  # 分數太低，不記錄
<<<<<<< HEAD
            
=======

>>>>>>> origin/setup-job-hunter-project
        return MatchResult(
            job_id=job.get('id', ''),
            title=job.get('title', ''),
            company=job.get('company', ''),
            location=job.get('location', ''),
            salary=job.get('salary'),
            url=job.get('url', ''),
            score=min(score, 100),  # 最高 100 分
            level=level,
            matched_skills=matched_skills,
            matched_keywords=matched_keywords,
            details=details
        )
<<<<<<< HEAD
        
=======

>>>>>>> origin/setup-job-hunter-project
    def _should_exclude(self, job: Dict[str, Any]) -> bool:
        """檢查是否應該排除此職缺"""
        title = job.get('title', '').lower()
        company = job.get('company', '').lower()
        location = job.get('location', '').lower()
<<<<<<< HEAD
        
=======

>>>>>>> origin/setup-job-hunter-project
        # 檢查職稱排除
        for excluded_title in self.exclusions.get('titles', []):
            if excluded_title.lower() in title:
                return True
<<<<<<< HEAD
                
=======

>>>>>>> origin/setup-job-hunter-project
        # 檢查公司排除
        for excluded_company in self.exclusions.get('companies', []):
            if excluded_company.lower() in company:
                return True
<<<<<<< HEAD
                
=======

>>>>>>> origin/setup-job-hunter-project
        # 檢查地區排除
        for excluded_location in self.exclusions.get('locations', []):
            if excluded_location.lower() in location:
                return True
<<<<<<< HEAD
                
        return False
        
=======

        return False

>>>>>>> origin/setup-job-hunter-project
    def _get_job_text(self, job: Dict[str, Any]) -> str:
        """合併職缺所有文字內容用於匹配"""
        parts = [
            job.get('title', ''),
            job.get('description', ''),
            job.get('requirements', ''),
            job.get('company', ''),
            ' '.join(job.get('tags', []))
        ]
        return ' '.join(parts).lower()
<<<<<<< HEAD
        
    def _match_core_skills(self, job_text: str) -> tuple:
        """
        匹配核心技能
        
=======

    def _match_core_skills(self, job_text: str) -> tuple:
        """
        匹配核心技能

>>>>>>> origin/setup-job-hunter-project
        Returns:
            (score, matched_skills)
        """
        total_score = 0
        matched = []
        job_text_lower = job_text.lower()
<<<<<<< HEAD
        
        for skill_name, skill_data in self.core_skills.items():
            weight = skill_data.get('weight', 5)
            keywords = skill_data.get('keywords', {})
            
=======

        for skill_name, skill_data in self.core_skills.items():
            weight = skill_data.get('weight', 5)
            keywords = skill_data.get('keywords', {})

>>>>>>> origin/setup-job-hunter-project
            # 主要關鍵字（全分）
            for kw in keywords.get('primary', []):
                if kw.lower() in job_text_lower:
                    total_score += weight
                    matched.append(kw)
                    break  # 每個技能只計算一次
<<<<<<< HEAD
                    
=======

>>>>>>> origin/setup-job-hunter-project
            # 次要關鍵字（半分）
            for kw in keywords.get('secondary', []):
                if kw.lower() in job_text_lower:
                    total_score += weight * 0.5
                    matched.append(kw)
                    break
<<<<<<< HEAD
                    
        return int(total_score), matched
        
=======

        return int(total_score), matched

>>>>>>> origin/setup-job-hunter-project
    def _match_industry(self, job: Dict[str, Any]) -> tuple:
        """匹配產業經驗"""
        score = 0
        matched = []
        company = job.get('company', '').lower()
        job_text = self._get_job_text(job).lower()
<<<<<<< HEAD
        
        for industry in self.industry_exp:
            weight = industry.get('weight', 5)
            
=======

        for industry in self.industry_exp:
            weight = industry.get('weight', 5)

>>>>>>> origin/setup-job-hunter-project
            # 檢查是否為目標公司
            for comp in industry.get('companies', []):
                if comp.lower() in company or comp.lower() in job_text:
                    score += weight
                    matched.append(comp)
                    break
<<<<<<< HEAD
                    
        return score, matched
        
=======

        return score, matched

>>>>>>> origin/setup-job-hunter-project
    def _match_target_position(self, job: Dict[str, Any]) -> int:
        """匹配目標職位"""
        score = 0
        title = job.get('title', '').lower()
<<<<<<< HEAD
        
=======

>>>>>>> origin/setup-job-hunter-project
        # 檢查主要目標
        for target in self.target_positions.get('primary', []):
            target_title = target.get('title', '').lower()
            target_keywords = [kw.lower() for kw in target.get('keywords', [])]
<<<<<<< HEAD
            
=======

>>>>>>> origin/setup-job-hunter-project
            # 職稱相似度
            similarity = fuzz.partial_ratio(target_title, title)
            if similarity > 70:
                score += 15
                break
<<<<<<< HEAD
                
=======

>>>>>>> origin/setup-job-hunter-project
            # 關鍵字匹配
            for kw in target_keywords:
                if kw in title:
                    score += 10
                    break
<<<<<<< HEAD
                    
=======

>>>>>>> origin/setup-job-hunter-project
        # 檢查次要目標
        if score == 0:
            for target in self.target_positions.get('secondary', []):
                target_keywords = [kw.lower() for kw in target.get('keywords', [])]
                for kw in target_keywords:
                    if kw in title:
                        score += 5
                        break
<<<<<<< HEAD
                        
        return score
        
=======

        return score

>>>>>>> origin/setup-job-hunter-project
    def _match_location(self, job: Dict[str, Any]) -> int:
        """匹配地點"""
        location = job.get('location', '').lower()
        locations = self.search_criteria.get('locations', {})
        bonus = self.matching_rules.get('bonus_points', {})
        penalty = self.matching_rules.get('penalty_points', {})
<<<<<<< HEAD
        
=======

>>>>>>> origin/setup-job-hunter-project
        # 優先地點
        for pref_loc in locations.get('preferred', []):
            if pref_loc.lower() in location:
                return bonus.get('location_preferred', 10)
<<<<<<< HEAD
                
=======

>>>>>>> origin/setup-job-hunter-project
        # 可接受地點
        for acc_loc in locations.get('acceptable', []):
            if acc_loc.lower() in location:
                return penalty.get('location_acceptable', -5)
<<<<<<< HEAD
                
        return -10  # 其他地區扣分
        
=======

        return -10  # 其他地區扣分

>>>>>>> origin/setup-job-hunter-project
    def _check_salary(self, job: Dict[str, Any]) -> int:
        """檢查薪資"""
        salary_str = job.get('salary', '')
        if not salary_str:
            return 0
<<<<<<< HEAD
            
=======

>>>>>>> origin/setup-job-hunter-project
        # 嘗試解析薪資
        try:
            # 提取數字（假設格式如 "60,000-75,000" 或 "月薪 50,000 以上"）
            numbers = re.findall(r'[\d,]+', salary_str.replace(',', ''))
            if numbers:
                max_salary = max(int(n) for n in numbers)
                min_required = self.search_criteria.get('salary', {}).get('minimum', 50000)
<<<<<<< HEAD
                
=======

>>>>>>> origin/setup-job-hunter-project
                if max_salary >= min_required:
                    return self.matching_rules.get('bonus_points', {}).get('salary_above_min', 5)
        except:
            pass
<<<<<<< HEAD
            
        return 0
        
=======

        return 0

>>>>>>> origin/setup-job-hunter-project
    def _match_certifications(self, job_text: str) -> int:
        """匹配認證"""
        score = 0
        job_text_lower = job_text.lower()
        bonus = self.matching_rules.get('bonus_points', {}).get('certification_match', 10)
<<<<<<< HEAD
        
=======

>>>>>>> origin/setup-job-hunter-project
        for cert in self.certifications:
            for kw in cert.get('keywords', []):
                if kw.lower() in job_text_lower:
                    score += bonus
                    break
<<<<<<< HEAD
                    
=======

>>>>>>> origin/setup-job-hunter-project
        return min(score, bonus * 2)  # 最多兩個認證加分


def batch_match(jobs: List[Dict[str, Any]], profile_path: str = "config/profile.yaml") -> List[MatchResult]:
    """
    批次匹配職缺
<<<<<<< HEAD
    
    Args:
        jobs: 職缺列表
        profile_path: 個人專長配置檔路徑
        
=======

    Args:
        jobs: 職缺列表
        profile_path: 個人專長配置檔路徑

>>>>>>> origin/setup-job-hunter-project
    Returns:
        排序後的匹配結果列表（分數高到低）
    """
    matcher = JobMatcher(profile_path)
    results = []
<<<<<<< HEAD
    
=======

>>>>>>> origin/setup-job-hunter-project
    for job in jobs:
        result = matcher.match(job)
        if result:
            results.append(result)
<<<<<<< HEAD
            
    # 按分數排序
    results.sort(key=lambda x: x.score, reverse=True)
    
=======

    # 按分數排序
    results.sort(key=lambda x: x.score, reverse=True)

>>>>>>> origin/setup-job-hunter-project
    return results


if __name__ == "__main__":
    # 測試用
    test_job = {
        'id': 'test001',
        'title': 'ASML 報關協調專員 - 桃園大園',
        'company': 'ASML Taiwan',
        'location': '桃園市大園區',
        'salary': '60,000-75,000',
        'url': 'https://example.com/job/test001',
        'description': '''
        職位說明：
        - 負責半導體設備進出口報關作業
        - 管理自由貿易港區保稅業務
        - 確保 AEO 認證合規
        - 處理危險品相關文件
<<<<<<< HEAD
        
=======

>>>>>>> origin/setup-job-hunter-project
        要求：
        - 5年以上報關經驗
        - 熟悉 HS Code 分類
        - 具備自貿區專責人員資格優先
        - 英文溝通能力
        ''',
        'requirements': '報關經驗, 半導體產業經驗, 英文能力',
        'tags': ['報關', '半導體', '物流']
    }
<<<<<<< HEAD
    
    matcher = JobMatcher()
    result = matcher.match(test_job)
    
=======

    matcher = JobMatcher()
    result = matcher.match(test_job)

>>>>>>> origin/setup-job-hunter-project
    if result:
        print(f"職缺: {result.title}")
        print(f"公司: {result.company}")
        print(f"匹配度: {result.score}% ({result.level})")
        print(f"匹配技能: {', '.join(result.matched_skills)}")
        print(f"匹配關鍵字: {', '.join(result.matched_keywords)}")
        print(f"詳細分數: {result.details}")
