"""
Web scrapers for different movie news sources
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import time

class BaseScraper:
    """Base class for all scrapers"""

    def __init__(self, source_name: str, base_url: str):
        self.source_name = source_name
        self.base_url = base_url
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

    def fetch_page(self, url: str) -> BeautifulSoup:
        """Fetch and parse a web page"""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            return None

    def scrape(self, max_articles: int = 5) -> List[Dict]:
        """Override this method in subclasses"""
        raise NotImplementedError


class VarietyScraper(BaseScraper):
    """Scraper for Variety"""

    def scrape(self, max_articles: int = 5) -> List[Dict]:
        articles = []
        soup = self.fetch_page(self.base_url)

        if not soup:
            return articles

        # Find article elements (this is a simplified example)
        article_elements = soup.find_all('article', limit=max_articles)

        for article in article_elements:
            try:
                title_elem = article.find(['h2', 'h3'])
                link_elem = article.find('a', href=True)
                desc_elem = article.find('p')

                if title_elem and link_elem:
                    article_data = {
                        'source': self.source_name,
                        'title': title_elem.get_text(strip=True),
                        'url': link_elem['href'] if link_elem['href'].startswith('http') else f"https://variety.com{link_elem['href']}",
                        'description': desc_elem.get_text(strip=True) if desc_elem else '',
                        'scraped_at': datetime.now().isoformat(),
                        'published_date': datetime.now().strftime('%Y-%m-%d')
                    }
                    articles.append(article_data)
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue

        return articles


class DeadlineScraper(BaseScraper):
    """Scraper for Deadline"""

    def scrape(self, max_articles: int = 5) -> List[Dict]:
        articles = []
        soup = self.fetch_page(self.base_url)

        if not soup:
            return articles

        article_elements = soup.find_all('article', limit=max_articles)

        for article in article_elements:
            try:
                title_elem = article.find(['h2', 'h3'])
                link_elem = article.find('a', href=True)
                desc_elem = article.find('p')

                if title_elem and link_elem:
                    article_data = {
                        'source': self.source_name,
                        'title': title_elem.get_text(strip=True),
                        'url': link_elem['href'] if link_elem['href'].startswith('http') else f"https://deadline.com{link_elem['href']}",
                        'description': desc_elem.get_text(strip=True) if desc_elem else '',
                        'scraped_at': datetime.now().isoformat(),
                        'published_date': datetime.now().strftime('%Y-%m-%d')
                    }
                    articles.append(article_data)
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue

        return articles


class HollywoodReporterScraper(BaseScraper):
    """Scraper for The Hollywood Reporter"""

    def scrape(self, max_articles: int = 5) -> List[Dict]:
        articles = []
        soup = self.fetch_page(self.base_url)

        if not soup:
            return articles

        article_elements = soup.find_all('article', limit=max_articles)

        for article in article_elements:
            try:
                title_elem = article.find(['h2', 'h3', 'h4'])
                link_elem = article.find('a', href=True)
                desc_elem = article.find('p')

                if title_elem and link_elem:
                    article_data = {
                        'source': self.source_name,
                        'title': title_elem.get_text(strip=True),
                        'url': link_elem['href'] if link_elem['href'].startswith('http') else f"https://www.hollywoodreporter.com{link_elem['href']}",
                        'description': desc_elem.get_text(strip=True) if desc_elem else '',
                        'scraped_at': datetime.now().isoformat(),
                        'published_date': datetime.now().strftime('%Y-%m-%d')
                    }
                    articles.append(article_data)
            except Exception as e:
                print(f"Error parsing article: {e}")
                continue

        return articles


def get_scraper(source_name: str, url: str) -> BaseScraper:
    """Factory function to get the appropriate scraper"""
    scrapers = {
        'Variety': VarietyScraper,
        'Deadline': DeadlineScraper,
        'The Hollywood Reporter': HollywoodReporterScraper,
    }

    scraper_class = scrapers.get(source_name, BaseScraper)
    return scraper_class(source_name, url)
