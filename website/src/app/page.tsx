import NewsCard from '@/components/NewsCard';
import SearchBar from '@/components/SearchBar';
import { Article } from '@/types/article';

async function getNews(): Promise<Article[]> {
  try {
    const fs = require('fs');
    const path = require('path');
    const newsDir = path.join(process.cwd(), '..', 'data', 'news');

    if (!fs.existsSync(newsDir)) {
      return [];
    }

    const files = fs.readdirSync(newsDir);
    const allArticles: Article[] = [];

    // Read all JSON files except latest.json
    for (const file of files) {
      if (file.endsWith('.json') && file !== 'latest.json') {
        const filePath = path.join(newsDir, file);
        const data = fs.readFileSync(filePath, 'utf8');
        const articles = JSON.parse(data);
        allArticles.push(...articles);
      }
    }

    // Sort by date, newest first
    allArticles.sort((a, b) =>
      new Date(b.published_date).getTime() - new Date(a.published_date).getTime()
    );

    // Return the 10 most recent articles
    return allArticles.slice(0, 10);
  } catch (error) {
    console.error('Error loading news:', error);
    return [];
  }
}

export default async function Home() {
  const articles = await getNews();
  const today = new Date().toLocaleDateString('zh-TW', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  });

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-md">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <h1 className="text-4xl font-bold text-gray-900 dark:text-white">
            🎬 每日電影新聞
          </h1>
          <p className="mt-2 text-gray-600 dark:text-gray-300">
            Daily Movie News - 來自好萊塢的最新消息
          </p>
          <p className="mt-1 text-sm text-gray-500 dark:text-gray-400">
            {today}
          </p>
        </div>
      </header>

      {/* Search Bar */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <SearchBar />
      </div>

      {/* Main Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {articles.length === 0 ? (
          <div className="text-center py-12">
            <p className="text-xl text-gray-600 dark:text-gray-400">
              目前沒有新聞，請稍後再來查看...
            </p>
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {articles.map((article, index) => (
              <NewsCard key={index} article={article} />
            ))}
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
