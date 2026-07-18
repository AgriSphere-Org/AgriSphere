import os
from typing import Dict

from dotenv import load_dotenv

import google.generativeai as genai

from rag.rag_service import RAGService

load_dotenv()


class KnowledgeAgent:
    """
    Knowledge Agent

    Responsibilities:
    - Receive farmer's question
    - Retrieve relevant knowledge
    - Generate grounded answer using Gemini
    """

    def __init__(self):

        self.rag_service = RAGService()

        genai.configure(

            api_key=os.getenv("GEMINI_API_KEY")

        )

        self.model = genai.GenerativeModel(

            "gemini-2.5-flash"

        )

    # --------------------------------------------------

    def ask(self, question: str) -> Dict:

        documents = self.rag_service.retrieve(question)

        context = self._build_context(documents)

        prompt = self._build_prompt(

            context,

            question

        )

        response = self.model.generate_content(

            prompt

        )

        return {

            "question": question,

            "answer": response.text,

            "sources": self._extract_sources(documents)

        }

    # --------------------------------------------------

    def _build_context(

        self,

        documents

    ) -> str:

        context = ""

        for document in documents:

            context += document.page_content

            context += "\n\n"

        return context

    # --------------------------------------------------

    def _build_prompt(

        self,

        context: str,

        question: str

    ) -> str:

        return f"""

You are AgriSphere AI.

You are an agricultural expert.

Answer ONLY using the information provided below.

If the answer cannot be found in the provided context,

reply with:

"I could not find reliable information in the knowledge base."

-------------------------

Context

{context}

-------------------------

Question

{question}

Answer:

"""

    # --------------------------------------------------

    def _extract_sources(

        self,

        documents

    ):

        sources = []

        for document in documents:

            source = document.metadata.get(

                "source",

                "Unknown"

            )

            if source not in sources:

                sources.append(source)

        return sources