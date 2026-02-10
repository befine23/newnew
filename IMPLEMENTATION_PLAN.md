# 實作計劃：完整文章 + 搜尋功能

## 📅 分支資訊
- **分支名稱**: `feature/full-article-with-search`
- **基於**: `anthropic` branch
- **開始日期**: 2026-02-08

## 🎯 目標

將系統從「每天 7 篇標題摘要」改為「每天 1 篇完整文章翻譯」，並添加搜尋和歷史文章瀏覽功能。

## 📋 需求規格

### 1. 爬蟲改進
- [x] 每天隨機從三個網站（Variety、Deadline、THR）選一個
- [ ] 抓取當天最熱門的文章
- [ ] 提取完整文章內容（標題、正文、圖片等）
- [ ] 生成 URL slug（從標題轉換）
- [ ] 翻譯完整內容

### 2. 前端功能
- [ ] **首頁**:
  - 顯示最近 10 篇文章
  - 卡片式布局：標題 + 前 200 字預覽 + 日期 + 來源
  - 「繼續閱讀」按鈕
- [ ] **文章詳細頁** (`/news/[slug]/`):
  - 完整翻譯內容
  - 原文連結
  - 發布日期、來源標示
- [ ] **搜尋功能**:
  - Search Bar（固定在頂部）
  - 搜尋標題和內容
  - 搜尋結果頁面
- [ ] **歷史瀏覽**:
  - 保留所有歷史文章
  - 可以瀏覽過往文章

### 3. 數據結構

```json
{
  "id": "2026-02-08-variety-001",
  "slug": "kumail-nanjiani-dga-awards",
  "source": "Variety",
  "title": "Kumail Nanjiani Opens Directors Guild Awards...",
  "title_zh": "庫梅爾·南賈尼在導演工會獎...",
  "content": "Full article content in English...",
  "content_zh": "完整翻譯內容...",
  "summary_zh": "前 200 字摘要預覽...",
  "image_url": "https://...",
  "url": "https://variety.com/...",
  "published_date": "2026-02-08",
  "scraped_at": "2026-02-08T08:00:00"
}
```

## 🔧 技術實作細節

### Phase 1: 爬蟲改進（後端）

#### 1.1 修改 `scraper/config.py`
```python
# 改為每天只抓 1 篇
MAX_ARTICLES_PER_SOURCE = 1

# 所有來源預設啟用
# 執行時隨機選一個
```

#### 1.2 創建 `scraper/content_extractor.py`
- 針對每個網站實作內容提取
- 處理不同的 HTML 結構
- 提取：標題、正文、圖片、發布日期

#### 1.3 改進 `scraper/main.py`
- 隨機選擇一個新聞來源
- 調用 content_extractor 提取完整內容
- 生成 slug（使用 `slugify` 或自定義函數）
- 生成唯一 ID

#### 1.4 改進 `scraper/translator.py`
- 翻譯完整內容（可能需要分段翻譯）
- 生成摘要（前 200 字）
- 優化 token 使用

### Phase 2: 前端重構

#### 2.1 首頁 (`website/src/app/page.tsx`)
- 讀取最近 10 篇文章
- 卡片式列表布局
- 搜尋框元件

#### 2.2 文章詳細頁 (`website/src/app/news/[slug]/page.tsx`)
- 動態路由
- 從 JSON 讀取文章內容
- Markdown 渲染（如果需要）

#### 2.3 搜尋功能 (`website/src/app/search/page.tsx`)
- 客戶端搜尋（靜態網站）
- 搜尋所有歷史文章
- 結果高亮顯示

#### 2.4 組件
- `SearchBar.tsx`: 搜尋框
- `ArticleCard.tsx`: 文章卡片
- `ArticleContent.tsx`: 文章內容顯示

### Phase 3: 數據管理

#### 3.1 文件結構
```
data/
└── news/
    ├── articles/
    │   ├── 2026-02-08.json
    │   ├── 2026-02-09.json
    │   └── ...
    ├── index.json (所有文章索引)
    └── latest.json (最新文章)
```

#### 3.2 生成索引
- 創建 `generate_index.py` 腳本
- 在每次爬取後更新索引
- 索引包含：id, slug, title_zh, summary_zh, date

## 📊 網站爬取策略

### Variety
- **文章列表**: `<article>` 標籤
- **內容提取**: 進入文章頁面，抓取 `<div class="article-content">` 或類似
- **挑戰**: 需要進入詳細頁面

### Deadline
- **文章列表**: `<article>` 或特定 class
- **內容提取**: 文章主體在特定 div 中
- **挑戰**: 可能有廣告混入內容

### The Hollywood Reporter
- **文章列表**: 結構化列表
- **內容提取**: 主內容區域
- **挑戰**: 可能有訂閱牆

## ⚠️ 潛在挑戰

### 1. 網站結構變化
- **風險**: 網站改版可能導致爬蟲失效
- **對策**: 錯誤處理 + 降級策略（只抓標題）

### 2. 反爬蟲機制
- **風險**: IP 封鎖、Rate Limiting
- **對策**: 添加延遲、User-Agent 輪換

### 3. 翻譯成本
- **風險**: 完整文章翻譯費用增加
- **對策**: 使用 GPT-4o-mini（最便宜）、優化 prompt

### 4. 靜態網站搜尋
- **風險**: 無後端，搜尋需在客戶端
- **對策**: 預先建立搜尋索引 JSON

## 💰 成本估算

### 翻譯費用（OpenAI GPT-4o-mini）
- 每篇文章：~800-1500 字
- 輸入：$0.150 / 1M tokens
- 輸出：$0.600 / 1M tokens
- **每篇成本**: ~$0.05-0.08
- **每月成本** (30 篇): ~$1.50-2.50

## 📅 實作時程

### Phase 1: 爬蟲改進 (預估 2-3 小時)
1. 研究網站結構
2. 實作內容提取器
3. 測試爬取完整文章

### Phase 2: 前端開發 (預估 2-3 小時)
1. 重構首頁
2. 創建文章詳細頁
3. 實作搜尋功能

### Phase 3: 整合測試 (預估 1 小時)
1. 端到端測試
2. 修復 bug
3. 優化效能

## 🎯 成功指標

- [ ] 每天成功抓取並翻譯 1 篇完整文章
- [ ] 首頁顯示最近 10 篇文章預覽
- [ ] 可以點擊進入文章詳細頁
- [ ] 搜尋功能正常運作
- [ ] 歷史文章可查看
- [ ] 部署到 Vercel 成功

## 📝 備註

- 需要測試不同網站的內容提取是否穩定
- 可能需要針對不同網站寫專門的提取邏輯
- 搜尋功能在靜態網站上需要特殊處理（客戶端 JS）
