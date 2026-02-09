"""
Translation module using OpenAI API
"""
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

class Translator:
    def __init__(self):
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        self.client = OpenAI(api_key=api_key)

    def translate_to_traditional_chinese(self, text: str) -> str:
        """
        Translate English text to Traditional Chinese
        """
        try:
            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a professional translator. Translate the following English movie news to Traditional Chinese (繁體中文). Keep the translation natural and fluent. Maintain proper names of people, movies, and studios in English or their commonly used Chinese names."
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                temperature=0.3
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Translation error: {e}")
            return text  # Return original text if translation fails

    def translate_long_text(self, text: str, max_length: int = 3000) -> str:
        """
        Translate long text by splitting into chunks if necessary
        """
        if not text or len(text) < max_length:
            return self.translate_to_traditional_chinese(text)

        # Split by paragraphs
        paragraphs = text.split('\n\n')
        translated_paragraphs = []
        current_chunk = ""

        for para in paragraphs:
            if len(current_chunk) + len(para) < max_length:
                current_chunk += para + "\n\n"
            else:
                # Translate current chunk
                if current_chunk:
                    translated_paragraphs.append(self.translate_to_traditional_chinese(current_chunk))
                current_chunk = para + "\n\n"

        # Translate remaining chunk
        if current_chunk:
            translated_paragraphs.append(self.translate_to_traditional_chinese(current_chunk))

        return '\n\n'.join(translated_paragraphs)

    def generate_summary(self, text: str, max_chars: int = 200) -> str:
        """
        Generate a summary from the translated text (first N characters)
        """
        if not text:
            return ""

        # Get first max_chars characters
        summary = text[:max_chars]

        # Try to end at a sentence boundary
        last_period = summary.rfind('。')
        last_exclaim = summary.rfind('！')
        last_question = summary.rfind('？')

        end_pos = max(last_period, last_exclaim, last_question)
        if end_pos > 0 and end_pos > max_chars * 0.5:  # At least 50% of desired length
            summary = summary[:end_pos + 1]
        elif len(text) > max_chars:
            summary += '...'

        return summary

    def translate_article(self, article: dict) -> dict:
        """
        Translate article title, description, and full content
        Also generate a summary
        """
        translated = article.copy()

        print(f"Translating: {article.get('title', 'Untitled')[:50]}...")

        # Translate title
        if 'title' in article and article['title']:
            translated['title_zh'] = self.translate_to_traditional_chinese(article['title'])

        # Translate description
        if 'description' in article and article['description']:
            translated['description_zh'] = self.translate_to_traditional_chinese(article['description'])

        # Translate full content (if available)
        if 'content' in article and article['content']:
            print(f"   Translating full article content ({len(article['content'])} chars)...")
            translated['content_zh'] = self.translate_long_text(article['content'])

            # Generate summary from translated content
            translated['summary_zh'] = self.generate_summary(translated['content_zh'], max_chars=200)
            print(f"   ✓ Translation complete. Summary: {len(translated['summary_zh'])} chars")

        return translated
