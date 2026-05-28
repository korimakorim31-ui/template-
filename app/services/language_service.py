"""Language detection and translation service"""

from typing import List, Dict
import asyncio

class LanguageService:
    """Service for multi-language support"""
    
    SUPPORTED_LANGUAGES = {
        "en": {"code": "en", "name": "English", "native_name": "English"},
        "es": {"code": "es", "name": "Spanish", "native_name": "Español"},
        "fr": {"code": "fr", "name": "French", "native_name": "Français"},
        "de": {"code": "de", "name": "German", "native_name": "Deutsch"},
        "it": {"code": "it", "name": "Italian", "native_name": "Italiano"},
        "pt": {"code": "pt", "name": "Portuguese", "native_name": "Português"},
        "ja": {"code": "ja", "name": "Japanese", "native_name": "日本語"},
        "ko": {"code": "ko", "name": "Korean", "native_name": "한국어"},
        "zh": {"code": "zh", "name": "Chinese", "native_name": "中文"},
        "ru": {"code": "ru", "name": "Russian", "native_name": "Русский"},
    }
    
    def get_supported_languages(self) -> List[Dict]:
        """Get list of supported languages"""
        return list(self.SUPPORTED_LANGUAGES.values())
    
    def detect_language(self, text: str) -> str:
        """Detect language of text"""
        try:
            import langdetect
            detected = langdetect.detect(text)
            return detected
        except:
            return "en"  # Default to English
    
    async def translate(
        self,
        content: str,
        source_language: str = "en",
        target_language: str = "es",
    ) -> str:
        """Translate content using Google Translate API"""
        try:
            import translators as ts
            translated = await asyncio.to_thread(
                ts.translate_text,
                content,
                from_language=source_language,
                to_language=target_language,
            )
            return translated
        except Exception as e:
            raise Exception(f"Translation failed: {str(e)}")
