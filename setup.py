#!/usr/bin/env python3
"""
初始化腳本 - 設定專案環境
"""
import os
import sys
from pathlib import Path


def create_directories():
    """建立必要目錄"""
    dirs = ['data', 'reports', 'src/scrapers', 'src/matcher', 'src/notifier']
    for d in dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
        # 建立 __init__.py
        init_file = Path(d) / '__init__.py'
        if not init_file.exists() and d.startswith('src'):
            init_file.touch()
    print("✅ 目錄結構已建立")


def create_env_template():
    """建立環境變數範本"""
    env_content = """# Yusei Job Hunter 環境設定
# 複製此檔案為 .env 並填入實際值

# Email 通知設定
EMAIL_USER=your_email@gmail.com
EMAIL_PASS=your_app_password

# LINE Notify 設定（可選）
LINE_TOKEN=your_line_notify_token

# 其他設定
DEBUG=false
"""
    with open('.env.example', 'w', encoding='utf-8') as f:
        f.write(env_content)
    print("✅ 環境變數範本已建立 (.env.example)")


def create_gitignore():
    """建立 .gitignore"""
    content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
.venv/
ENV/
env/

# IDE
.idea/
.vscode/
*.swp
*.swo

# 專案特定
.env
data/*.json
data/*.log
reports/*.md

# 系統
.DS_Store
Thumbs.db
"""
    with open('.gitignore', 'w', encoding='utf-8') as f:
        f.write(content)
    print("✅ .gitignore 已建立")


def main():
    print("\n🚀 Yusei Job Hunter - 初始化設定\n")
    
    create_directories()
    create_env_template()
    create_gitignore()
    
    print("\n" + "=" * 50)
    print("✅ 初始化完成！")
    print("=" * 50)
    print("\n後續步驟：")
    print("1. 複製 .env.example 為 .env 並填入設定")
    print("2. 安裝依賴：pip install -r requirements.txt")
    print("3. 執行測試：python src/main.py")
    print("4. （可選）設定 GitHub Actions 自動執行")
    print()


if __name__ == "__main__":
    main()
