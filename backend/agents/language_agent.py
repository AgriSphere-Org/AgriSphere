from services.translation_service import TranslationService


class LanguageAgent:
    """
    Handles multilingual communication for AgriSphere.

    Responsibilities:
    - Detect user language
    - Translate input to English
    - Translate English responses back to the user's language
    """

    def __init__(self):
        self.translation_service = TranslationService()

    # -------------------------------------------------

    def process_question(self, question: str) -> dict:
        """
        Detect the language of the user's question and
        translate it to English if necessary.

        Returns:
        {
            "detected_language": "...",
            "english_question": "..."
        }
        """

        processed = self.translation_service.process_input(question)

        return {
            "detected_language": processed["language"],
            "english_question": processed["english_text"]
        }

    # -------------------------------------------------

    def process_answer(self, answer: str, language: str) -> str:
        """
        Translate the English answer back to the user's
        original language.

        Parameters:
            answer: English response
            language: Original user language

        Returns:
            Translated response
        """

        return self.translation_service.process_output(
            answer,
            language
        )

    # -------------------------------------------------

    def translate(self, text: str, target_language: str) -> str:
        """
        Translate text directly into the specified language.
        """

        return self.translation_service.translate_from_english(
            text,
            target_language
        )

    # -------------------------------------------------

    def detect_language(self, text: str) -> str:
        """
        Detect the language of the given text.
        """

        return self.translation_service.detect_language(text)