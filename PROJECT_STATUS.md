# 專案進度記錄

## 📅 最後更新：2026-02-08

## ✅ 已完成的功能

### 1. 核心功能
- [x] Python 爬蟲系統（Variety、Deadline、Hollywood Reporter）
- [x] OpenAI GPT-4o-mini 翻譯整合
- [x] Next.js 靜態網站生成
- [x] GitHub Actions 每日自動執行（台灣時間早上 8:00）
- [x] 自動 commit 並 push 到 GitHub
- [x] Vercel 自動部署

### 2. 配置設定
- [x] 每日抓取 7 篇新聞（Variety 3篇 + Deadline 3篇 + Hollywood Reporter 1篇）
- [x] OpenAI API 整合完成
- [x] GitHub Secrets 設定完成
- [x] Git 推送權限設定完成

### 3. 部署狀態
- [x] GitHub Repository: https://github.com/befine23/newnew
- [x] Vercel 網站: https://newnew-orcin-five.vercel.app/
- [x] 網站成功上線並自動同步

## 🔧 已解決的技術問題

### 問題 1: OpenAI API Key 設定
- **問題**: 環境變數命名不一致導致無法讀取
- **解決**: 統一使用 `OPENAI_API_KEY` 命名

### 問題 2: 文件路徑錯誤
- **問題**: 相對路徑導致文件保存位置錯誤
- **解決**: 使用 `Path(__file__).parent` 計算絕對路徑

### 問題 3: GitHub Actions 推送權限
- **問題**: 403 錯誤無法推送到 repository
- **解決**: 在 workflow 添加 `permissions: contents: write`

### 問題 4: Vercel 部署配置衝突
- **問題**: vercel.json 與 Root Directory 設定衝突
- **解決**: 刪除根目錄 vercel.json，使用 Root Directory 設定

## 📊 目前系統運作狀態

### 爬蟲
- **狀態**: ✅ 正常運作
- **執行頻率**: 每天台灣時間早上 8:00
- **數據來源**: 3 個新聞網站
- **每日文章數**: 7 篇

### 翻譯
- **服務**: OpenAI GPT-4o-mini
- **狀態**: ✅ 正常運作
- **翻譯範圍**: 目前僅翻譯標題
- **月費用**: 約 $0.30-0.50

### 網站
- **框架**: Next.js 14 (Static Export)
- **樣式**: Tailwind CSS
- **託管**: Vercel
- **狀態**: ✅ 已上線

## 🤔 待討論的功能改進

### 內容抓取範圍
目前爬蟲只抓取：
- ✅ 新聞標題
- ✅ 新聞連結
- ❌ 新聞摘要/內容（空的）

### 改進方案選項

#### 選項 A: 保持現狀（推薦）
- 只翻譯標題
- 點擊「閱讀更多」跳轉到原文網站
- **優點**: 簡單、穩定、無版權問題、費用低
- **缺點**: 用戶需跳轉才能看完整內容

#### 選項 B: 抓取完整文章
- 爬取並翻譯完整文章內容
- 在網站上顯示完整翻譯
- **優點**: 用戶體驗好，不需跳轉
- **缺點**: 複雜度高、費用增加 5-10 倍、可能有版權問題

#### 選項 C: 折衷方案 - 抓取摘要
- 只抓取新聞摘要（前 200 字或第一段）
- 翻譯摘要並顯示
- **優點**: 平衡體驗和成本
- **缺點**: 仍需處理不同網站的結構差異

### 待決定
用戶目前在考慮採用哪個方案。

## 📝 技術棧總結

### 後端
- Python 3.11
- Beautiful Soup 4
- OpenAI API
- Requests

### 前端
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS

### DevOps
- GitHub Actions
- Vercel
- Git

## 💰 成本估算

### 目前配置（每天 7 篇，僅標題）
- OpenAI API: $0.30-0.50/月
- GitHub Actions: 免費（2000 分鐘/月額度內）
- Vercel: 免費
- **總計**: ~$0.50/月

### 如果改為完整內容
- OpenAI API: $2.50-5.00/月
- 其他: 免費
- **總計**: ~$5/月

## 🎯 下一步

1. 用戶決定內容抓取範圍
2. 根據選擇改進爬蟲（如需要）
3. 可能的其他功能：
   - 添加搜索功能
   - 添加分類/標籤
   - 添加 RSS 訂閱
   - 添加深色模式
