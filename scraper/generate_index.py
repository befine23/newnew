"""
Generate articles index for frontend search functionality
Reads all news JSON files and creates a combined index
"""
import json
import os
from pathlib import Path

def generate_articles_index():
    """Generate a combined index of all articles for search"""
    # Get paths
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / 'data' / 'news'
    website_public = script_dir.parent / 'website' / 'public'

    # Ensure website/public exists
    website_public.mkdir(parents=True, exist_ok=True)

    all_articles = []

    # Read all JSON files
    if data_dir.exists():
        for file_path in data_dir.glob('news_*.json'):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    articles = json.load(f)
                    all_articles.extend(articles)
            except Exception as e:
                print(f"Error reading {file_path}: {e}")

    # Sort by date, newest first
    all_articles.sort(key=lambda x: x.get('published_date', ''), reverse=True)

    # Save to website/public/articles.json
    output_path = website_public / 'articles.json'
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(all_articles, f, ensure_ascii=False, indent=2)

    print(f"✅ Generated articles index: {output_path}")
    print(f"   Total articles: {len(all_articles)}")

if __name__ == '__main__':
    generate_articles_index()
