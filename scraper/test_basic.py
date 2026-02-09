"""
Basic test script for scraper components
"""
from utils import generate_slug, generate_article_id
from datetime import datetime

def test_slug_generation():
    """Test slug generation"""
    print("Testing slug generation...")

    test_cases = [
        "Kumail Nanjiani Opens Directors Guild Awards With Jokes",
        "Ted Sarandos Isn't Worried About Trump's Involvement",
        "'One Battle After Another' Director Paul Thomas Anderson Wins Top DGA Awards Prize"
    ]

    for title in test_cases:
        slug = generate_slug(title)
        print(f"  Title: {title[:50]}...")
        print(f"  Slug:  {slug}")
        print()

def test_id_generation():
    """Test article ID generation"""
    print("Testing article ID generation...")

    date = datetime.now().strftime('%Y-%m-%d')
    sources = ['Variety', 'Deadline', 'The Hollywood Reporter']
    slug = "kumail-nanjiani-opens-directors-guild"

    for source in sources:
        article_id = generate_article_id(source, date, slug)
        print(f"  Source: {source}")
        print(f"  ID:     {article_id}")
        print()

def test_config():
    """Test config loading"""
    print("Testing config...")
    from config import NEWS_SOURCES, RANDOM_SOURCE_SELECTION, MAX_ARTICLES_PER_SOURCE

    print(f"  Random selection: {RANDOM_SOURCE_SELECTION}")
    print(f"  Max articles: {MAX_ARTICLES_PER_SOURCE}")
    print(f"  Enabled sources: {len([s for s in NEWS_SOURCES.values() if s['enabled']])}")
    print()

def test_imports():
    """Test all imports"""
    print("Testing imports...")
    try:
        from config import NEWS_SOURCES
        from scrapers import get_scraper
        from translator import Translator
        from content_extractor import get_content_extractor
        from utils import generate_slug
        print("  ✓ All imports successful")
    except Exception as e:
        print(f"  ✗ Import error: {e}")
    print()

if __name__ == "__main__":
    print("=== Basic Component Tests ===\n")

    test_imports()
    test_config()
    test_slug_generation()
    test_id_generation()

    print("=== All basic tests complete! ===")
