# 🎬 每日電影新聞 | Daily Movie News

自動化的每日電影新聞部落格 - 從好萊塢主要媒體自動抓取、翻譯成繁體中文並發布到網站。

## ✨ 功能特色

- 🤖 **全自動化**: 每天台灣時間早上 8:00 自動執行
- 🌐 **多來源爬蟲**: 從 Variety、Deadline、The Hollywood Reporter 等主流媒體抓取新聞
- 🇹🇼 **繁體中文翻譯**: 使用 OpenAI API 自動翻譯成流暢的繁體中文
- 📱 **響應式網站**: 使用 Next.js 構建的現代化靜態網站
- 💰 **完全免費**: 使用 GitHub Actions + Vercel 免費託管

## 🏗️ 專案架構

```
newnew/
├── scraper/              # Python 爬蟲模組
│   ├── main.py          # 主程式
│   ├── scrapers.py      # 各網站爬蟲
│   ├── translator.py    # 翻譯模組
│   └── config.py        # 配置文件
├── website/             # Next.js 網站
│   ├── src/
│   │   ├── app/        # Next.js App Router
│   │   ├── components/ # React 組件
│   │   └── types/      # TypeScript 類型定義
│   └── public/         # 靜態資源
├── data/               # 爬取的新聞數據
│   └── news/
│       ├── latest.json # 最新新聞
│       └── news_YYYY-MM-DD.json # 每日存檔
└── .github/workflows/  # GitHub Actions 自動化
```

## 🚀 快速開始

### 1. 環境要求

- Python 3.11+
- Node.js 18+
- OpenAI API Key

### 2. 安裝依賴

#### Python 依賴
```bash
pip install -r requirements.txt
```

#### Node.js 依賴
```bash
cd website
npm install
```

### 3. 設定環境變數

創建 `.env` 文件：
```bash
cp .env.example .env
```

編輯 `.env` 並填入您的 OpenAI API Key：
```
OPENAI_API_KEY=sk-your-api-key-here
```

### 4. 本地測試

#### 測試爬蟲
```bash
cd scraper
python main.py
```

#### 測試網站
```bash
cd website
npm run dev
```

訪問 http://localhost:3000 查看網站。

## 🔧 部署指南

### GitHub Actions 設定

1. 在 GitHub Repository 設定中添加 Secret：
   - 進入 `Settings` → `Secrets and variables` → `Actions`
   - 添加 `OPENAI_API_KEY`

2. GitHub Actions 會每天台灣時間早上 8:00 自動執行
3. 也可以手動觸發：`Actions` → `Daily Movie News Scraper` → `Run workflow`

### Vercel 部署

1. 前往 [Vercel](https://vercel.com) 並登入
2. 點擊 "Import Project"
3. 連接您的 GitHub repository
4. Vercel 會自動識別 Next.js 專案並部署
5. 每次 GitHub 有新的 commit，Vercel 會自動重新部署

## 📝 配置說明

### 調整新聞來源

編輯 `scraper/config.py`:

```python
NEWS_SOURCES = {
    'variety': {
        'name': 'Variety',
        'url': 'https://variety.com/v/film/news/',
        'enabled': True  # 設為 False 可停用此來源
    },
    # 添加更多來源...
}

# 每個來源抓取的文章數量
MAX_ARTICLES_PER_SOURCE = 5
```

### 調整執行時間

編輯 `.github/workflows/daily-scraper.yml`:

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC 00:00 = 台灣時間 08:00
```

## 📊 工作流程

```
每天早上 8:00 (台灣時間)
       ↓
GitHub Actions 觸發
       ↓
執行 Python 爬蟲
       ↓
抓取電影新聞
       ↓
翻譯成繁體中文
       ↓
儲存為 JSON 文件
       ↓
Commit 並 Push 到 GitHub
       ↓
Vercel 自動偵測並重新部署網站
       ↓
✅ 網站更新完成！
```

## 🛠️ 技術棧

### 後端 (爬蟲)
- Python 3.11
- Beautiful Soup 4 (網頁解析)
- OpenAI API (翻譯)
- Requests (HTTP 請求)

### 前端 (網站)
- Next.js 14 (靜態網站生成)
- React 18
- TypeScript
- Tailwind CSS (樣式)

### DevOps
- GitHub Actions (自動化)
- Vercel (網站託管)

## 📄 授權

本專案採用 MIT 授權。

## 🤝 貢獻

歡迎提交 Issues 和 Pull Requests！

## 📧 聯繫方式

如有問題或建議，歡迎開 Issue 討論。

---

**自動化每日更新 | Powered by Next.js & Python**
