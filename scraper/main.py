"""
Main script to scrape movie news and translate to Traditional Chinese
"""
import json
import os
import random
from datetime import datetime
from pathlib import Path
from config import NEWS_SOURCES, MAX_ARTICLES_PER_SOURCE, OUTPUT_DIR, RANDOM_SOURCE_SELECTION
from scrapers import get_scraper
from translator import Translator
from utils import generate_slug, generate_article_id

# Calculate absolute path to output directory
# Get the directory where this script is located (scraper/)
SCRIPT_DIR = Path(__file__).parent
# Get project root (parent of scraper/)
PROJECT_ROOT = SCRIPT_DIR.parent
# Construct absolute path to data/news/
OUTPUT_PATH = PROJECT_ROOT / 'data' / 'news'


def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    OUTPUT_PATH.mkdir(parents=True, exist_ok=True)
    print(f"Output directory: {OUTPUT_PATH}")


def save_articles(articles: list, filename: str):
    """Save articles to JSON file"""
    ensure_output_dir()
    filepath = OUTPUT_PATH / filename

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(articles)} articles to {filepath}")


def main():
    """Main execution function"""
    print("=== Movie News Scraper & Translator ===\n")

    all_articles = []
    translator = Translator()

    # Select sources to scrape
    enabled_sources = {k: v for k, v in NEWS_SOURCES.items() if v.get('enabled', False)}

    if RANDOM_SOURCE_SELECTION and enabled_sources:
        # Randomly pick ONE source
        source_key = random.choice(list(enabled_sources.keys()))
        sources_to_scrape = {source_key: enabled_sources[source_key]}
        print(f"🎲 Randomly selected: {enabled_sources[source_key]['name']}\n")
    else:
        # Use all enabled sources (legacy mode)
        sources_to_scrape = enabled_sources

    # Scrape from selected source(s)
    for source_key, source_config in sources_to_scrape.items():
        print(f"\n📰 Scraping from {source_config['name']}...")
        scraper = get_scraper(source_config['name'], source_config['url'])

        try:
            max_articles = source_config.get('max_articles', MAX_ARTICLES_PER_SOURCE)
            articles = scraper.scrape(max_articles=max_articles)
            print(f"   Found {len(articles)} articles")

            # Translate each article
            for article in articles:
                translated_article = translator.translate_article(article)

                # Generate slug and ID
                title = translated_article.get('title', 'untitled')
                slug = generate_slug(title)
                article_id = generate_article_id(
                    source=translated_article['source'],
                    date=translated_article['published_date'],
                    slug=slug
                )

                translated_article['slug'] = slug
                translated_article['id'] = article_id

                print(f"   ✓ Generated: ID={article_id[:40]}... slug={slug[:40]}...")

                all_articles.append(translated_article)

        except Exception as e:
            print(f"   Error scraping {source_config['name']}: {e}")

    # Save all articles
    if all_articles:
        today = datetime.now().strftime('%Y-%m-%d')
        filename = f"news_{today}.json"
        save_articles(all_articles, filename)

        # Also save as latest.json for the website
        save_articles(all_articles, 'latest.json')

        print(f"\n✅ Successfully scraped and translated {len(all_articles)} articles!")
    else:
        print("\n⚠️  No articles were scraped.")


if __name__ == "__main__":
    main()
