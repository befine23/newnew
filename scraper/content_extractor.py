"""
Content extractor for different news sources
Extracts full article content from article pages
"""
import requests
from bs4 import BeautifulSoup
import time


class ContentExtractor:
    """Base class for content extraction"""

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36'
        }

    def fetch_article_page(self, url: str) -> BeautifulSoup:
        """Fetch article page and return parsed HTML"""
        try:
            time.sleep(1)  # Be respectful to the server
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return BeautifulSoup(response.content, 'lxml')
        except Exception as e:
            print(f"   Error fetching article page {url}: {e}")
            return None

    def extract_content(self, article_url: str) -> dict:
        """
        Extract full content from article URL
        Returns dict with: content, image_url
        Override this in subclasses
        """
        raise NotImplementedError


class VarietyExtractor(ContentExtractor):
    """Content extractor for Variety"""

    def extract_content(self, article_url: str) -> dict:
        """Extract full article content from Variety"""
        soup = self.fetch_article_page(article_url)
        if not soup:
            return {'content': '', 'image_url': ''}

        result = {'content': '', 'image_url': ''}

        try:
            # Extract main content
            # Variety uses <div class="c-content__body"> or similar
            content_div = soup.find('div', class_='c-content__body')
            if not content_div:
                content_div = soup.find('div', class_='article-body')
            if not content_div:
                content_div = soup.find('article')

            if content_div:
                # Get all paragraphs
                paragraphs = content_div.find_all('p')
                content_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                result['content'] = content_text

            # Extract featured image
            img = soup.find('meta', property='og:image')
            if img and img.get('content'):
                result['image_url'] = img['content']
            else:
                img_tag = soup.find('img', class_='c-picture__img')
                if img_tag and img_tag.get('src'):
                    result['image_url'] = img_tag['src']

        except Exception as e:
            print(f"   Error extracting Variety content: {e}")

        return result


class DeadlineExtractor(ContentExtractor):
    """Content extractor for Deadline"""

    def extract_content(self, article_url: str) -> dict:
        """Extract full article content from Deadline"""
        soup = self.fetch_article_page(article_url)
        if not soup:
            return {'content': '', 'image_url': ''}

        result = {'content': '', 'image_url': ''}

        try:
            # Extract main content
            # Deadline uses <div class="a-content"> or similar
            content_div = soup.find('div', class_='a-content')
            if not content_div:
                content_div = soup.find('div', {'id': 'article-content'})
            if not content_div:
                content_div = soup.find('article')

            if content_div:
                paragraphs = content_div.find_all('p')
                content_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                result['content'] = content_text

            # Extract featured image
            img = soup.find('meta', property='og:image')
            if img and img.get('content'):
                result['image_url'] = img['content']

        except Exception as e:
            print(f"   Error extracting Deadline content: {e}")

        return result


class HollywoodReporterExtractor(ContentExtractor):
    """Content extractor for The Hollywood Reporter"""

    def extract_content(self, article_url: str) -> dict:
        """Extract full article content from THR"""
        soup = self.fetch_article_page(article_url)
        if not soup:
            return {'content': '', 'image_url': ''}

        result = {'content': '', 'image_url': ''}

        try:
            # Extract main content
            # THR uses <div class="article-content"> or similar
            content_div = soup.find('div', class_='article-content')
            if not content_div:
                content_div = soup.find('div', class_='content-body')
            if not content_div:
                content_div = soup.find('article')

            if content_div:
                paragraphs = content_div.find_all('p')
                content_text = '\n\n'.join([p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)])
                result['content'] = content_text

            # Extract featured image
            img = soup.find('meta', property='og:image')
            if img and img.get('content'):
                result['image_url'] = img['content']

        except Exception as e:
            print(f"   Error extracting THR content: {e}")

        return result


def get_content_extractor(source_name: str) -> ContentExtractor:
    """Factory function to get the appropriate content extractor"""
    extractors = {
        'Variety': VarietyExtractor,
        'Deadline': DeadlineExtractor,
        'The Hollywood Reporter': HollywoodReporterExtractor,
    }

    extractor_class = extractors.get(source_name, ContentExtractor)
    return extractor_class()
