'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

export default function SearchBar() {
  const [query, setQuery] = useState('');
  const router = useRouter();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (query.trim()) {
      router.push(`/search?q=${encodeURIComponent(query.trim())}`);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full max-w-2xl mx-auto">
      <div className="relative">
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="搜尋電影新聞..."
          className="w-full px-6 py-4 text-lg rounded-full border-2 border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white placeholder-gray-500 dark:placeholder-gray-400 focus:outline-none focus:border-blue-500 dark:focus:border-blue-400 shadow-lg"
        />
        <button
          type="submit"
          className="absolute right-3 top-1/2 -translate-y-1/2 px-6 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-full transition-colors"
        >
          搜尋
        </button>
      </div>
    </form>
  );
}
