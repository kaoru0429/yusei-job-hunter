# 🌙 Operation Moonlight: Jules Pro 過夜任務清單

**目標**: 充分利用 Jules Pro 的 15-Agent 並行能力，在今晚完成所有核心功能開發  
**預估時間**: 8-10 小時 (並行執行)  
**優先順序**: P0 (關鍵) → P1 (重要) → P2 (加分項)

---

## 📋 Team A: 爬蟲完善隊 (Agents 1-5)

### P0: LinkedIn 爬蟲實作 (Agent 1)
**現況**: 骨架已建立，但需要完善登入與解析邏輯  
**任務**:
1. 測試並修復 LinkedIn 登入流程
2. 完善職缺卡片解析 (處理多種 DOM 結構)
3. 加入錯誤重試機制
4. 測試至少能抓取 20+ 筆職缺

**驗證**: `python -c "from src.scrapers.scraper_linkedin import *; s=LinkedInScraper('config/platforms.yaml'); print(len(s.search('報關')))"`

### P1: 1111 人力銀行爬蟲 (Agent 2)
**現況**: 僅有空殼  
**任務**:
1. 研究 1111 網站結構
2. 選擇適當方法 (Requests vs Selenium)
3. 實作 `search()` 方法
4. 測試並調整

**目標產出**: 至少 30+ 筆職缺

### P1: Meet.jobs 爬蟲 (Agent 3)
**現況**: 僅有空殼  
**任務**:
1. 研究 Meet.jobs API
2. 實作國際化職缺爬蟲
3. 處理英文職缺標題與描述

**目標產出**: 至少 15+ 筆國際職缺

---

## 🤖 Team B: AI 核心隊 (Agents 6-8)

### P0: JobMatcher 調參 (Agent 6)
**現況**: Matcher 過濾太嚴格，導致 0 結果  
**任務**:
1. 分析 `config/profile.yaml` 的匹配邏輯
2. 降低 `thresholds.medium` 從 60 → 40
3. 調整技能權重
4. 測試確保至少 30% 職缺能通過篩選

**驗證**: API 應返回至少 30+ 筆 matched 職缺

### P1: AI 語意搜尋 (Agent 7)
**任務**:
1. 整合 OpenAI Embeddings API
2. 實作職缺描述的向量化
3. 建立語意相似度搜尋
4. 加入 "相似職缺推薦" 功能

**產出**: `/api/similar-jobs` endpoint

---

## 🎨 Team C: 前端優化隊 (Agents 9-10)

### P0: 前端功能完善 (Agent 9)
**現況**: 基本搜尋完成，但缺少細節  
**任務**:
1. 加入 Loading 動畫 (Skeleton Screen)
2. 實作職缺詳情 Modal
3. 加入篩選器: 地點、薪資範圍、發布時間
4. 優化移動端響應式設計

### P1: Dashboard 儀表板 (Agent 10)
**任務**:
1. 建立職缺統計圖表 (Recharts)
2. 顯示平台來源分布 (Pie Chart)
3. 薪資分布直方圖
4. 每日新增職缺趨勢圖

**路由**: `/dashboard`

---

## 🐳 Team D: DevOps 隊 (Agents 11-12)

### P0: Docker 實際部署測試 (Agent 11)
**現況**: `Dockerfile` 與 `docker-compose.yml` 已建立但未測試  
**任務**:
1. 執行 `docker-compose up` 確保能正常啟動
2. 修復所有 Docker 相關錯誤
3. 加入環境變數管理
4. 測試容器內爬蟲能否正常運作

**驗證**: 容器內 API 能回傳職缺

### P1: GitHub Actions CI/CD (Agent 12)
**任務**:
1. 建立 `.github/workflows/test.yml`
2. 設定自動化測試
3. 設定自動化 Docker build & push
4. 加入 Linting

---

## 📧 Team E: 通知與排程 (Agents 13-14)

### P1: Email 通知系統測試 (Agent 13)
**現況**: `notifier.py` 已存在但未整合  
**任務**:
1. 測試 Gmail SMTP 連線
2. 整合到 API
3. 設計 HTML Email 模板
4. 加入 "訂閱每日職缺" 功能

### P2: 定時任務排程 (Agent 14)
**任務**:
1. 使用 APScheduler 或 Celery
2. 設定每日自動搜尋 (早上 8:00)
3. 搜尋結果自動發送到信箱
4. 建立任務執行日誌

---

## 🎯 關鍵里程碑

**2:00 AM**: Team A 完成 3 個新爬蟲  
**4:00 AM**: Team B 完成 Matcher 調參，AI 功能上線  
**6:00 AM**: Team C 前端 v2.0 完成  
**8:00 AM**: 全系統整合測試通過

---

**Jules Pro 加油！** 🚀
