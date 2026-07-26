import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class TranslationService:
    """
    Handles:
    - Language Detection
    - Translation to English
    - Translation from English
    """

    def __init__(self):

        genai.configure(
            api_key=os.getenv("GEMINI_API_KEY")
        )

        self.model = genai.GenerativeModel(
            "gemini-2.5-flash"
        )

    # -------------------------------------------------

    def detect_language(self, text: str) -> str:
        """
        Detects the language of the given text.

        Returns only the language name.
        Example:
        English
        Hindi
        Marathi
        Tamil
        """

        prompt = f"""
Detect the language of the following text.

Return ONLY the language name.

Text:
{text}
"""

        response = self.model.generate_content(prompt)

        return response.text.strip()

    # -------------------------------------------------

    def translate_to_english(self, text: str) -> str:
        """
        Translates any language into English.
        """

        prompt = f"""
Translate the following text into English.

Only return the translated text.

Text:
{text}
"""

        response = self.model.generate_content(prompt)

        return response.text.strip()

    # -------------------------------------------------

    def translate_from_english(
        self,
        text: str,
        target_language: str
    ) -> str:
        """
        Translates English into the requested language.
        """

        prompt = f"""
Translate the following English text into {target_language}.

Only return the translated text.

Text:
{text}
"""

        response = self.model.generate_content(prompt)

        return response.text.strip()

    # -------------------------------------------------

    def process_input(self, text: str):
        """
        Detect language and translate to English.

        Returns:
        {
            language,
            english_text
        }
        """

        language = self.detect_language(text)

        if language.lower() == "english":

            english_text = text

        else:

            english_text = self.translate_to_english(text)

        return {

            "language": language,

            "english_text": english_text

        }

    # -------------------------------------------------

    def process_output(
        self,
        answer: str,
        language: str
    ):
        """
        Translate the final response back
        into the user's language.
        """

        if language.lower() == "english":

            return answer

        return self.translate_from_english(

            answer,

            language

        )