"""
Utility functions for the scraper
"""
import re
import unicodedata
from datetime import datetime


def generate_slug(title: str) -> str:
    """
    Generate a URL-friendly slug from article title
    Example: "Kumail Nanjiani Opens Directors Guild Awards" -> "kumail-nanjiani-opens-directors-guild-awards"
    """
    # Convert to lowercase
    slug = title.lower()

    # Remove special characters and punctuation
    slug = re.sub(r"[^\w\s-]", "", slug)

    # Replace spaces with hyphens
    slug = re.sub(r"[\s_]+", "-", slug)

    # Remove multiple hyphens
    slug = re.sub(r"-+", "-", slug)

    # Trim hyphens from ends
    slug = slug.strip("-")

    # Limit length
    if len(slug) > 100:
        slug = slug[:100].rsplit("-", 1)[0]  # Cut at word boundary

    return slug


def generate_article_id(source: str, date: str, slug: str) -> str:
    """
    Generate a unique article ID
    Format: {date}-{source}-{slug_hash}
    Example: "2026-02-08-variety-abc123"
    """
    # Get first 8 characters of slug for uniqueness
    slug_short = slug[:30] if len(slug) <= 30 else slug[:30]

    # Clean source name
    source_clean = source.lower().replace(" ", "").replace("the", "")

    article_id = f"{date}-{source_clean}-{slug_short}"

    return article_id


def format_date(date_str: str) -> str:
    """
    Format date string to YYYY-MM-DD
    """
    try:
        date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return date_obj.strftime('%Y-%m-%d')
    except:
        return datetime.now().strftime('%Y-%m-%d')
