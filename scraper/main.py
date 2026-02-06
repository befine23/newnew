"""
Main script to scrape movie news and translate to Traditional Chinese
"""
import json
import os
from datetime import datetime
from pathlib import Path
from config import NEWS_SOURCES, MAX_ARTICLES_PER_SOURCE, OUTPUT_DIR
from scrapers import get_scraper
from translator import Translator


def ensure_output_dir():
    """Create output directory if it doesn't exist"""
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)


def save_articles(articles: list, filename: str):
    """Save articles to JSON file"""
    ensure_output_dir()
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)

    print(f"Saved {len(articles)} articles to {filepath}")


def main():
    """Main execution function"""
    print("=== Movie News Scraper & Translator ===\n")

    all_articles = []
    translator = Translator()

    # Scrape from each enabled source
    for source_key, source_config in NEWS_SOURCES.items():
        if not source_config.get('enabled', False):
            continue

        print(f"\n📰 Scraping from {source_config['name']}...")
        scraper = get_scraper(source_config['name'], source_config['url'])

        try:
            max_articles = source_config.get('max_articles', MAX_ARTICLES_PER_SOURCE)
            articles = scraper.scrape(max_articles=max_articles)
            print(f"   Found {len(articles)} articles")

            # Translate each article
            for article in articles:
                translated_article = translator.translate_article(article)
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
