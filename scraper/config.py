"""
Configuration for movie news scraper
"""

NEWS_SOURCES = {
    'variety': {
        'name': 'Variety',
        'url': 'https://variety.com/v/film/news/',
        'enabled': True,
        'max_articles': 3
    },
    'deadline': {
        'name': 'Deadline',
        'url': 'https://deadline.com/category/movies/',
        'enabled': True,
        'max_articles': 3
    },
    'hollywoodreporter': {
        'name': 'The Hollywood Reporter',
        'url': 'https://www.hollywoodreporter.com/c/movies/',
        'enabled': True,
        'max_articles': 1
    }
}

# Default number of articles to scrape per source (if not specified)
MAX_ARTICLES_PER_SOURCE = 3  # Total: 3+3+1 = 7 articles per day

# Output settings
OUTPUT_DIR = '../data/news'  # Relative to project root
OUTPUT_FORMAT = 'json'
