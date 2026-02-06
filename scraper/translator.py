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

    def translate_article(self, article: dict) -> dict:
        """
        Translate article title and content
        """
        translated = article.copy()

        print(f"Translating: {article.get('title', 'Untitled')[:50]}...")

        if 'title' in article:
            translated['title_zh'] = self.translate_to_traditional_chinese(article['title'])

        if 'description' in article:
            translated['description_zh'] = self.translate_to_traditional_chinese(article['description'])

        if 'content' in article:
            translated['content_zh'] = self.translate_to_traditional_chinese(article['content'])

        return translated
