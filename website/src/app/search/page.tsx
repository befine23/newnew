'use client';

import { useEffect, useState, Suspense } from 'react';
import { useSearchParams } from 'next/navigation';
import NewsCard from '@/components/NewsCard';
import SearchBar from '@/components/SearchBar';
import Link from 'next/link';
import { Article } from '@/types/article';

function SearchContent() {
  const searchParams = useSearchParams();
  const query = searchParams.get('q') || '';
  const [articles, setArticles] = useState<Article[]>([]);
  const [filteredArticles, setFilteredArticles] = useState<Article[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Load all articles from static JSON file
    async function loadArticles() {
      try {
        const response = await fetch('/articles.json');
        if (!response.ok) {
          throw new Error('Failed to load articles');
        }
        const data = await response.json();
        setArticles(data);
      } catch (error) {
        console.error('Error loading articles:', error);
        setArticles([]);
      } finally {
        setLoading(false);
      }
    }

    loadArticles();
  }, []);

  useEffect(() => {
    if (!query.trim()) {
      setFilteredArticles([]);
      return;
    }

    const searchTerm = query.toLowerCase();
    const filtered = articles.filter(article => {
      const titleMatch = (article.title_zh || article.title).toLowerCase().includes(searchTerm);
      const contentMatch = (article.content_zh || article.content || '').toLowerCase().includes(searchTerm);
      const summaryMatch = (article.summary_zh || '').toLowerCase().includes(searchTerm);

      return titleMatch || contentMatch || summaryMatch;
    });

    setFilteredArticles(filtered);
  }, [query, articles]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Link
            href="/"
            className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 mb-4"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            返回首頁
          </Link>

          <h1 className="text-4xl font-bold text-gray-900 dark:text-white mb-6">
            🔍 搜尋電影新聞
          </h1>

          <SearchBar />
        </div>
      </header>

      {/* Search Results */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="text-center py-12">
            <p className="text-xl text-gray-600 dark:text-gray-400">載入中...</p>
          </div>
        ) : query.trim() ? (
          <>
            <div className="mb-6">
              <p className="text-gray-600 dark:text-gray-400">
                搜尋 <span className="font-semibold">"{query}"</span> 的結果：
                共找到 <span className="font-semibold">{filteredArticles.length}</span> 篇文章
              </p>
            </div>

            {filteredArticles.length === 0 ? (
              <div className="text-center py-12">
                <p className="text-xl text-gray-600 dark:text-gray-400">
                  找不到相關文章，請嘗試其他關鍵字
                </p>
              </div>
            ) : (
              <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
                {filteredArticles.map((article) => (
                  <NewsCard key={article.id} article={article} />
                ))}
              </div>
            )}
          </>
        ) : (
          <div className="text-center py-12">
            <p className="text-xl text-gray-600 dark:text-gray-400">
              請輸入關鍵字開始搜尋
            </p>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 shadow-md mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-gray-600 dark:text-gray-400 text-sm">
            自動化每日更新 | Powered by Next.js & Python
          </p>
        </div>
      </footer>
    </div>
  );
}

export default function SearchPage() {
  return (
    <Suspense fallback={<div>載入中...</div>}>
      <SearchContent />
    </Suspense>
  );
}
