import json
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google import genai

from services.rag_service import RAGService


load_dotenv()


class KnowledgeAgent:

    def __init__(self):

        # ==============================
        # RAG
        # ==============================

        self.rag_service = RAGService()

        # ==============================
        # GEMINI
        # ==============================

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-2.5-flash"

    # =========================================================
    # MAIN
    # =========================================================

    def ask(
        self,
        question: str,
        conversation_context: Optional[Dict[str, Any]] = None
    ) -> Dict:

        question = (question or "").strip()

        if not question:
            raise ValueError(
                "Please provide an agricultural question."
            )

        conversation_context = conversation_context or {}

        # -----------------------------------------------------
        # 1. UNDERSTAND
        # -----------------------------------------------------

        analysis = self._analyze_query(
            question,
            conversation_context
        )

        print("\n========== QUERY ANALYSIS ==========")
        print(
            json.dumps(
                analysis,
                indent=2,
                ensure_ascii=False
            )
        )

        # -----------------------------------------------------
        # 2. SPECIALIZED AGENT ROUTING
        # -----------------------------------------------------

        specialized = self._detect_specialized_agent(
            analysis
        )

        if specialized["requires_specialized_agent"]:

            return {
                "question": question,
                "answer": specialized["message"],
                "sources": [],
                "topic": analysis.get("topic"),
                "intent": analysis.get("intent"),
                "crop": analysis.get("crop"),
                "evidence_available": False,
                "evidence_sufficient": False,
                "requires_specialized_agent": True,
                "specialized_agent": specialized["specialized_agent"],
                "missing_information": analysis.get(
                    "missing_information", []
                ),
                "confidence": "Not applicable"
            }

        # -----------------------------------------------------
        # 3. CLARIFICATION
        # -----------------------------------------------------

        if analysis.get("needs_clarification", False):

            return {
                "question": question,
                "answer": analysis.get(
                    "clarification_question",
                    "Please provide a little more information."
                ),
                "sources": [],
                "topic": analysis.get("topic"),
                "intent": analysis.get("intent"),
                "crop": analysis.get("crop"),
                "evidence_available": False,
                "evidence_sufficient": False,
                "requires_specialized_agent": False,
                "specialized_agent": None,
                "missing_information": analysis.get(
                    "missing_information", []
                ),
                "confidence": "Insufficient information"
            }

        # -----------------------------------------------------
        # 4. RAG RETRIEVAL
        # -----------------------------------------------------

        search_query = analysis.get(
            "search_query",
            question
        )

        print("\n========== SEARCH QUERY ==========")
        print(search_query)

        try:

            documents = self.rag_service.retrieve(
                search_query,
                k=6
            )

        except Exception as e:

            print("RAG retrieval error:", e)

            documents = []

        print("\n========== RETRIEVAL ==========")
        print(
            f"Documents retrieved: {len(documents)}"
        )

        # -----------------------------------------------------
        # 5. BUILD CONTEXT
        # -----------------------------------------------------

        context = self._build_context(
            documents
        )

        # -----------------------------------------------------
        # 6. DIRECT REASONING + ANSWER
        # -----------------------------------------------------

        answer = self._generate_answer(
            question=question,
            analysis=analysis,
            conversation_context=conversation_context,
            context=context,
            evidence_available=len(documents) > 0
        )

        # -----------------------------------------------------
        # 7. RESPONSE
        # -----------------------------------------------------

        return {
            "question": question,
            "answer": answer,
            "sources": self._extract_sources(documents),
            "topic": analysis.get("topic"),
            "intent": analysis.get("intent"),
            "crop": analysis.get("crop"),
            "evidence_available": len(documents) > 0,
            "evidence_sufficient": len(documents) > 0,
            "requires_specialized_agent": False,
            "specialized_agent": None,
            "missing_information": analysis.get(
                "missing_information", []
            ),
            "confidence": "High" if documents else "Moderate"
        }

    # =========================================================
    # QUERY ANALYSIS
    # =========================================================

    def _analyze_query(
        self,
        question: str,
        conversation_context: Dict[str, Any]
    ) -> Dict:

        prompt = f"""
You are the query understanding component of an agricultural
AI assistant.

Understand the user's agricultural question.

Do NOT answer the question.

Determine:

- topic
- intent
- crop
- location
- season
- crop stage
- symptoms
- search query
- whether clarification is genuinely necessary

IMPORTANT:

Normal agricultural knowledge questions must NOT be routed
to the Knowledge Agent because this component is already
inside the Knowledge Agent.

Only route questions requiring CURRENT or SPECIALIZED data.

Examples:

"What is soil pH?"
"What is crop rotation?"
"Why is nitrogen important?"
"How does irrigation affect crops?"
"What is photosynthesis?"
"What is organic farming?"

These are normal Knowledge Agent questions.

========================================
QUESTION
========================================

{question}

========================================
CONVERSATION
========================================

{json.dumps(
    conversation_context,
    indent=2,
    ensure_ascii=False
)}

========================================
RETURN ONLY JSON
========================================

{{
    "topic": "soil",
    "intent": "explanation",
    "crop": null,
    "location": null,
    "season": null,
    "crop_stage": null,
    "symptoms": [],
    "user_goal": null,
    "needs_clarification": false,
    "missing_information": [],
    "clarification_question": null,
    "search_query": "{question}",
    "requires_specialized_agent": false,
    "specialized_agent": null
}}

"""

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            text = self._clean_json(
                response.text
            )

            result = json.loads(text)

            return self._normalize_analysis(
                result,
                question
            )

        except Exception as e:

            print("Query analysis error:", e)

            return {
                "topic": "agriculture",
                "intent": "general_agriculture",
                "crop": None,
                "location": None,
                "season": None,
                "crop_stage": None,
                "symptoms": [],
                "user_goal": None,
                "needs_clarification": False,
                "missing_information": [],
                "clarification_question": None,
                "search_query": question,
                "requires_specialized_agent": False,
                "specialized_agent": None
            }

    # =========================================================
    # NORMALIZE ANALYSIS
    # =========================================================

    def _normalize_analysis(
        self,
        result: Dict,
        question: str
    ) -> Dict:

        defaults = {
            "topic": "agriculture",
            "intent": "general_agriculture",
            "crop": None,
            "location": None,
            "season": None,
            "crop_stage": None,
            "symptoms": [],
            "user_goal": None,
            "needs_clarification": False,
            "missing_information": [],
            "clarification_question": None,
            "search_query": question,
            "requires_specialized_agent": False,
            "specialized_agent": None
        }

        for key, value in defaults.items():

            if key not in result:
                result[key] = value

        # Never allow Knowledge Agent to route to itself.

        agent = str(
            result.get(
                "specialized_agent",
                ""
            )
        ).lower().strip()

        if agent in [
            "knowledge",
            "knowledge agent",
            "knowledge assistant"
        ]:

            result["requires_specialized_agent"] = False
            result["specialized_agent"] = None

        if not result.get("search_query"):
            result["search_query"] = question

        return result

    # =========================================================
    # SPECIALIZED AGENT DETECTION
    # =========================================================

    def _detect_specialized_agent(
        self,
        analysis: Dict
    ) -> Dict:

        intent = str(
            analysis.get(
                "intent",
                ""
            )
        ).lower()

        topic = str(
            analysis.get(
                "topic",
                ""
            )
        ).lower()

        # -----------------------------------------------------
        # MARKET
        # -----------------------------------------------------

        if intent == "market":

            return {
                "requires_specialized_agent": True,
                "specialized_agent":
                    "Market Intelligence Agent",
                "message":
                    "This question requires current market information. "
                    "Please use the Market Intelligence Agent."
            }

        # -----------------------------------------------------
        # WEATHER / CLIMATE
        # -----------------------------------------------------

        if intent == "weather_agriculture":

            return {
                "requires_specialized_agent": True,
                "specialized_agent":
                    "Climate Intelligence Agent",
                "message":
                    "This question requires current weather or climate "
                    "information. Please use the Climate Intelligence Agent."
            }

        # -----------------------------------------------------
        # GOVERNMENT
        # -----------------------------------------------------

        if intent == "government_scheme":

            return {
                "requires_specialized_agent": True,
                "specialized_agent":
                    "Government Scheme Agent",
                "message":
                    "This question requires current government scheme "
                    "information. Please use the Government Scheme Agent."
            }

        # -----------------------------------------------------
        # CROP PLANNING
        # -----------------------------------------------------

        if intent == "crop_selection":

            return {
                "requires_specialized_agent": True,
                "specialized_agent":
                    "Crop Planning Agent",
                "message":
                    "This question requires crop suitability analysis. "
                    "Please use the Crop Planning Agent."
            }

        # -----------------------------------------------------
        # NORMAL KNOWLEDGE
        # -----------------------------------------------------

        return {
            "requires_specialized_agent": False,
            "specialized_agent": None
        }

    # =========================================================
    # BUILD RAG CONTEXT
    # =========================================================

    def _build_context(
        self,
        documents: List[Any]
    ) -> str:

        if not documents:
            return (
                "No relevant documents were retrieved from "
                "the agricultural knowledge base."
            )

        parts = []

        for index, document in enumerate(
            documents,
            start=1
        ):

            metadata = getattr(
                document,
                "metadata",
                {}
            )

            source = (
                metadata.get("document_name")
                or metadata.get("source")
                or "Agricultural knowledge source"
            )

            page = metadata.get("page")

            if isinstance(page, int):
                source += f", page {page + 1}"

            content = (
                getattr(
                    document,
                    "page_content",
                    ""
                )
                or ""
            ).strip()

            if not content:
                continue

            parts.append(
                f"""
SOURCE {index}
Source: {source}

{content}
"""
            )

        if not parts:
            return (
                "No usable information was retrieved."
            )

        return "\n".join(parts)

    # =========================================================
    # GENERATE ANSWER
    # =========================================================

    def _generate_answer(
        self,
        question: str,
        analysis: Dict,
        conversation_context: Dict[str, Any],
        context: str,
        evidence_available: bool
    ) -> str:

        prompt = f"""
You are AgriSphere AI's Knowledge Agent.

You are a general agricultural knowledge assistant.

Your job is to answer agricultural questions naturally,
accurately and intelligently.

========================================
USER QUESTION
========================================

{question}

========================================
QUERY ANALYSIS
========================================

{json.dumps(
    analysis,
    indent=2,
    ensure_ascii=False
)}

========================================
CONVERSATION CONTEXT
========================================

{json.dumps(
    conversation_context,
    indent=2,
    ensure_ascii=False
)}

========================================
RETRIEVED AGRICULTURAL KNOWLEDGE
========================================

{context}

========================================
CRITICAL ANSWERING RULES
========================================

1. ANSWER THE QUESTION DIRECTLY.

Do not start with:

"I can explain..."
"Based on the available information..."
"The provided evidence does not..."
"I don't have a direct definition..."

Just answer.

2. RAG IS SUPPORTING KNOWLEDGE.

Retrieved documents are useful evidence.

They are NOT a restriction on what you can explain.

If the documents contain relevant information, use it.

If the documents only partially cover the question, combine
the retrieved information with your general agricultural
knowledge.

3. DO NOT REQUIRE AN EXACT SENTENCE IN THE DOCUMENT.

For example, if the user asks:

"What is soil pH?"

and the documents discuss soil acidity, alkalinity,
nutrient availability and soil management, you can use
that information together with your general knowledge to
give a complete explanation.

4. DO NOT INVENT FACTS.

Never fabricate:

- chemical dosages
- pesticide quantities
- fertilizer application rates
- market prices
- weather information
- government scheme details
- disease diagnoses

5. CURRENT INFORMATION.

Do not pretend that the knowledge base contains current
weather, market prices or current government information.

Those belong to specialized agents.

6. AGRICULTURAL REASONING.

For questions such as:

"Why are leaves yellow?"
"What happens if soil is acidic?"
"Why is nitrogen important?"

explain the cause and reasoning.

7. PRACTICAL QUESTIONS.

For "how to" questions, provide clear steps.

8. UNCERTAIN QUESTIONS.

If several causes are possible, say:

"Possible causes include..."

Do not pretend one cause is certain.

9. SIMPLE LANGUAGE.

Answer like an agricultural expert explaining the concept
to a farmer or agriculture student.

10. DO NOT TALK ABOUT:

- RAG
- embeddings
- FAISS
- prompts
- Gemini
- vector databases
- internal agents
- evidence evaluation

11. FORMAT.

Use normal Markdown.

Use:

### headings

- bullet points

1. numbered steps

Do NOT output literal characters such as:

\\n

Use actual line breaks.

12. ANSWER LENGTH.

Simple question:
2-5 paragraphs.

Complex question:
Use headings and detailed explanation.

13. LANGUAGE.

Answer in the same language as the user whenever practical.

========================================
FINAL INSTRUCTION
========================================

Now answer the user's question directly.
"""

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            answer = (
                response.text or ""
            ).strip()

            # ---------------------------------------------
            # FIX LITERAL ESCAPED NEWLINES
            # ---------------------------------------------

            answer = answer.replace(
                "\\n",
                "\n"
            )

            # Remove accidental code fences
            if answer.startswith("```") and answer.endswith("```"):
                lines = answer.splitlines()

                if len(lines) > 2:
                    answer = "\n".join(
                        lines[1:-1]
                    )

            return answer.strip()

        except Exception as e:

            print(
                "Answer generation error:",
                e
            )

            return (
                "I couldn't generate a reliable answer "
                "right now. Please try again."
            )

    # =========================================================
    # SOURCES
    # =========================================================

    def _extract_sources(
        self,
        documents: List[Any]
    ) -> List[str]:

        sources = []

        for document in documents:

            metadata = getattr(
                document,
                "metadata",
                {}
            )

            source = (
                metadata.get("document_name")
                or metadata.get("source")
            )

            if source and source not in sources:
                sources.append(
                    str(source)
                )

        return sources

    # =========================================================
    # CLEAN JSON
    # =========================================================

    def _clean_json(
        self,
        text: str
    ) -> str:

        text = (
            text or ""
        ).strip()

        if text.startswith("```json"):
            text = text[7:]

        elif text.startswith("```"):
            text = text[3:]

        if text.endswith("```"):
            text = text[:-3]

        return text.strip()