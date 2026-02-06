"""
Configuration for movie news scraper
"""

NEWS_SOURCES = {
    'variety': {
        'name': 'Variety',
        'url': 'https://variety.com/v/film/news/',
        'enabled': True
    },
    'deadline': {
        'name': 'Deadline',
        'url': 'https://deadline.com/category/movies/',
        'enabled': True
    },
    'hollywoodreporter': {
        'name': 'The Hollywood Reporter',
        'url': 'https://www.hollywoodreporter.com/c/movies/',
        'enabled': True
    }
}

# Number of articles to scrape per source
MAX_ARTICLES_PER_SOURCE = 5

# Output settings
OUTPUT_DIR = 'data/news'
OUTPUT_FORMAT = 'json'
