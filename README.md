# 🎯 Yusei Job Hunter - 自動化職缺搜尋系統

## 專案說明

這是一個專為 **Yusei** 設計的自動化職缺搜尋系統，基於你的專業背景每日自動搜尋並推送適合的職缺。

## 🚀 功能特點

- **每日自動執行**：透過 GitHub Actions 排程每日搜尋
- **多平台搜尋**：支援 104、LinkedIn、CakeResume、Yourator
- **智能媒合**：根據專長關鍵字計算匹配度
- **即時通知**：透過 Email/LINE 推送高度匹配職缺
- **報告生成**：每日生成 Markdown 格式報告

## 📋 目標職缺類型

根據 Yusei 的專業背景，系統優先搜尋以下類型：

### 主要目標
1. **報關/通關協調專員** - ASML、半導體設備商
2. **貿易合規專員** - 外商物流、科技業
3. **空運出口 OP/主管** - 國際快遞、貨運承攬

### 關鍵字組合
- `報關` + `半導體` / `自貿區` / `保稅`
- `Export Control` + `Compliance` / `LECO`
- `空運` + `出口` + `資深` / `主管`
- `Customs` + `Coordinator` + `ASML` / `半導體`
- `物流` + `系統` + `開發` / `整合`

## 🔧 安裝設定

### 本地執行

```bash
# 克隆專案
git clone https://github.com/yourusername/yusei-job-hunter.git
cd yusei-job-hunter

# 安裝依賴
pip install -r requirements.txt

# 設定環境變數
cp .env.example .env
# 編輯 .env 填入 API keys

# 執行
python src/main.py
```

### GitHub Actions 自動執行

1. Fork 此專案到你的 GitHub
2. 設定 Repository Secrets：
   - `EMAIL_USER`: 發送通知的 Email
   - `EMAIL_PASS`: Email 密碼/App Password
   - `LINE_TOKEN`: LINE Notify Token（選用）
3. 專案會在每天台灣時間 08:00 自動執行

## 📊 輸出範例

每日報告會生成在 `reports/daily_report_{date}.md`，格式如下：

```markdown
# 職缺報告 - 2025-12-10

## 🔥 高度匹配 (>80%)

### 1. [ASML] 報關協調專員 - 桃園大園
- **匹配度**: 92%
- **薪資**: 60,000-75,000
- **關鍵命中**: 報關、自貿區、半導體、AEO
- **連結**: https://www.104.com.tw/job/xxxxx

...
```

## 📁 專案結構

```
yusei-job-hunter/
├── config/
│   ├── profile.yaml      # 個人專長配置
│   └── platforms.yaml    # 平台搜尋配置
├── src/
│   ├── scrapers/         # 各平台爬蟲
│   ├── matcher/          # 媒合引擎
│   ├── notifier/         # 通知模組
│   └── main.py           # 主程式
├── data/                 # 資料儲存
├── reports/              # 每日報告
└── .github/workflows/    # CI/CD 設定
```

## ⚙️ 設定說明

### profile.yaml - 個人專長配置

這是系統的核心配置，定義了你的專業背景和目標職缺。詳見 `config/profile.yaml`。

### platforms.yaml - 平台搜尋配置

定義各職缺平台的搜尋參數和 API 設定。

## 🔄 更新記錄

- **v1.0.0** (2025-12-09): 初始版本

## 📝 授權

MIT License
