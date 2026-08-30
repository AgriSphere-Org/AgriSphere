import os

from dotenv import load_dotenv

import google.generativeai as genai

load_dotenv()


class LLMService:

    """
    Handles communication
    with Gemini.
    """

    def __init__(self):

        genai.configure(

            api_key=os.getenv("GEMINI_API_KEY")

        )

        self.model = genai.GenerativeModel(

            "gemini-2.5-flash"

        )

    # -----------------------------------------

    def generate(

        self,

        prompt: str

    ) -> str:

        response = self.model.generate_content(

            prompt

        )

        return response.text
    