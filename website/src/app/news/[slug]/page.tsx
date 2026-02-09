import { Article } from '@/types/article';
import Link from 'next/link';
import Image from 'next/image';
import { notFound } from 'next/navigation';

async function getAllArticles(): Promise<Article[]> {
  try {
    const fs = require('fs');
    const path = require('path');
    const newsDir = path.join(process.cwd(), '..', 'data', 'news');

    if (!fs.existsSync(newsDir)) {
      return [];
    }

    const files = fs.readdirSync(newsDir);
    const allArticles: Article[] = [];

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

    return allArticles;
  } catch (error) {
    console.error('Error loading articles:', error);
    return [];
  }
}

async function getArticleBySlug(slug: string): Promise<Article | null> {
  const articles = await getAllArticles();
  return articles.find(article => article.slug === slug) || null;
}

export async function generateStaticParams() {
  const articles = await getAllArticles();
  return articles.map((article) => ({
    slug: article.slug,
  }));
}

interface PageProps {
  params: {
    slug: string;
  };
}

export default async function ArticlePage({ params }: PageProps) {
  const article = await getArticleBySlug(params.slug);

  if (!article) {
    notFound();
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 to-gray-100 dark:from-gray-900 dark:to-gray-800">
      {/* Header */}
      <header className="bg-white dark:bg-gray-800 shadow-md">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <Link
            href="/"
            className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 mb-4"
          >
            <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
            返回首頁
          </Link>

          <div className="flex items-center justify-between mb-3">
            <span className="inline-block px-3 py-1 text-sm font-semibold text-white bg-red-600 rounded-full">
              {article.source}
            </span>
            <span className="text-sm text-gray-500 dark:text-gray-400">
              {new Date(article.published_date).toLocaleDateString('zh-TW', {
                year: 'numeric',
                month: 'long',
                day: 'numeric'
              })}
            </span>
          </div>

          <h1 className="text-3xl md:text-4xl font-bold text-gray-900 dark:text-white mb-4">
            {article.title_zh || article.title}
          </h1>

          {article.title_zh && (
            <p className="text-lg text-gray-600 dark:text-gray-400 italic">
              {article.title}
            </p>
          )}
        </div>
      </header>

      {/* Article Image */}
      {article.image_url && (
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 mt-8">
          <div className="relative w-full h-96 rounded-lg overflow-hidden shadow-lg">
            <Image
              src={article.image_url}
              alt={article.title_zh || article.title}
              fill
              className="object-cover"
              priority
            />
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <article className="bg-white dark:bg-gray-800 rounded-lg shadow-lg p-8">
          {/* Article Content */}
          <div className="prose prose-lg dark:prose-invert max-w-none">
            {article.content_zh ? (
              <div className="whitespace-pre-wrap text-gray-800 dark:text-gray-200 leading-relaxed">
                {article.content_zh}
              </div>
            ) : (
              <div className="whitespace-pre-wrap text-gray-800 dark:text-gray-200 leading-relaxed">
                {article.content}
              </div>
            )}
          </div>

          {/* Original Article Link */}
          <div className="mt-8 pt-8 border-t border-gray-200 dark:border-gray-700">
            <a
              href={article.url}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium"
            >
              閱讀原文
              <svg className="w-4 h-4 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
            </a>
          </div>
        </article>
      </main>

      {/* Footer */}
      <footer className="bg-white dark:bg-gray-800 shadow-md mt-12">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <p className="text-center text-gray-600 dark:text-gray-400 text-sm">
            自動化每日更新 | Powered by Next.js & Python
          </p>
        </div>
      </footer>
    </div>
  );
}
