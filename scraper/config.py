"""
Configuration for movie news scraper
"""

NEWS_SOURCES = {
    'variety': {
        'name': 'Variety',
        'url': 'https://variety.com/v/film/news/',
        'enabled': True,
        'max_articles': 1  # Only scrape 1 article per day
    },
    'deadline': {
        'name': 'Deadline',
        'url': 'https://deadline.com/category/movies/',
        'enabled': True,
        'max_articles': 1
    },
    'hollywoodreporter': {
        'name': 'The Hollywood Reporter',
        'url': 'https://www.hollywoodreporter.com/c/movies/',
        'enabled': True,
        'max_articles': 1
    }
}

# Strategy: Pick ONE random source per day, scrape 1 full article
MAX_ARTICLES_PER_SOURCE = 1
RANDOM_SOURCE_SELECTION = True  # Enable random source selection

# Output settings (Note: main.py uses absolute path calculation)
OUTPUT_DIR = 'data/news'
OUTPUT_FORMAT = 'json'
