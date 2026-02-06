import { Article } from '@/types/article';

interface NewsCardProps {
  article: Article;
}

export default function NewsCard({ article }: NewsCardProps) {
  return (
    <article className="bg-white dark:bg-gray-800 rounded-lg shadow-lg overflow-hidden hover:shadow-xl transition-shadow duration-300">
      <div className="p-6">
        {/* Source Badge */}
        <div className="flex items-center justify-between mb-3">
          <span className="inline-block px-3 py-1 text-xs font-semibold text-white bg-red-600 rounded-full">
            {article.source}
          </span>
          <span className="text-xs text-gray-500 dark:text-gray-400">
            {new Date(article.published_date).toLocaleDateString('zh-TW')}
          </span>
        </div>

        {/* Title */}
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-3 line-clamp-2">
          {article.title_zh || article.title}
        </h2>

        {/* Description */}
        <p className="text-gray-600 dark:text-gray-300 mb-4 line-clamp-3">
          {article.description_zh || article.description}
        </p>

        {/* Original Title (if translated) */}
        {article.title_zh && (
          <p className="text-sm text-gray-500 dark:text-gray-400 italic mb-4 line-clamp-1">
            原標題: {article.title}
          </p>
        )}

        {/* Read More Link */}
        <a
          href={article.url}
          target="_blank"
          rel="noopener noreferrer"
          className="inline-flex items-center text-blue-600 dark:text-blue-400 hover:text-blue-800 dark:hover:text-blue-300 font-medium"
        >
          閱讀更多
          <svg
            className="w-4 h-4 ml-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M9 5l7 7-7 7"
            />
          </svg>
        </a>
      </div>
    </article>
  );
}
