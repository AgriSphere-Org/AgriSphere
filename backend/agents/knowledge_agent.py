import json
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google import genai

from services.rag_service import RAGService


load_dotenv()


class KnowledgeAgent:

    def __init__(self):

        # =====================================================
        # RAG SERVICE
        # =====================================================

        self.rag_service = RAGService()

        # =====================================================
        # GEMINI
        # =====================================================

        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured."
            )

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
                "Please provide a question."
            )

        conversation_context = (
            conversation_context or {}
        )

        # -----------------------------------------------------
        # 1. UNDERSTAND USER QUESTION
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
        # 2. CHECK SPECIALIZED AGENT
        # -----------------------------------------------------

        specialized = self._detect_specialized_agent(
            analysis
        )

        if specialized["requires_specialized_agent"]:

            return {
                "question": question,

                "answer": specialized["message"],

                "sources": [],

                "topic": analysis.get(
                    "topic"
                ),

                "intent": analysis.get(
                    "intent"
                ),

                "crop": analysis.get(
                    "crop"
                ),

                "evidence_available": False,

                "evidence_sufficient": False,

                "requires_specialized_agent": True,

                "specialized_agent":
                    specialized[
                        "specialized_agent"
                    ],

                "missing_information":
                    analysis.get(
                        "missing_information",
                        []
                    ),

                "confidence":
                    "Not applicable"
            }

        # -----------------------------------------------------
        # 3. CLARIFICATION
        # -----------------------------------------------------

        if analysis.get(
            "needs_clarification",
            False
        ):

            return {
                "question": question,

                "answer": analysis.get(
                    "clarification_question",
                    "Could you provide a little more information?"
                ),

                "sources": [],

                "topic": analysis.get(
                    "topic"
                ),

                "intent": analysis.get(
                    "intent"
                ),

                "crop": analysis.get(
                    "crop"
                ),

                "evidence_available": False,

                "evidence_sufficient": False,

                "requires_specialized_agent": False,

                "specialized_agent": None,

                "missing_information":
                    analysis.get(
                        "missing_information",
                        []
                    ),

                "confidence":
                    "Insufficient information"
            }

        # -----------------------------------------------------
        # 4. BUILD BETTER SEARCH QUERY
        # -----------------------------------------------------

        search_query = analysis.get(
            "search_query"
        )

        if not search_query:

            search_query = question

        print("\n========== SEARCH QUERY ==========")
        print(search_query)

        # -----------------------------------------------------
        # 5. RAG RETRIEVAL
        # -----------------------------------------------------

        try:

            documents = self.rag_service.retrieve(
                search_query,
                k=6
            )

        except Exception as e:

            print(
                "RAG retrieval error:",
                e
            )

            documents = []

        print("\n========== RETRIEVAL ==========")

        print(
            f"Documents retrieved: {len(documents)}"
        )

        # -----------------------------------------------------
        # 6. BUILD CONTEXT
        # -----------------------------------------------------

        context = self._build_context(
            documents
        )

        # -----------------------------------------------------
        # 7. GENERATE ANSWER
        # -----------------------------------------------------

        answer = self._generate_answer(
            question=question,

            analysis=analysis,

            conversation_context=
                conversation_context,

            context=context,

            evidence_available=
                len(documents) > 0
        )

        # -----------------------------------------------------
        # 8. DETERMINE EVIDENCE STATUS
        # -----------------------------------------------------

        evidence_available = (
            len(documents) > 0
        )

        evidence_sufficient = (
            self._has_useful_context(
                context
            )
        )

        # -----------------------------------------------------
        # 9. RESPONSE
        # -----------------------------------------------------

        return {

            "question":
                question,

            "answer":
                answer,

            "sources":
                self._extract_sources(
                    documents
                ),

            "topic":
                analysis.get(
                    "topic"
                ),

            "intent":
                analysis.get(
                    "intent"
                ),

            "crop":
                analysis.get(
                    "crop"
                ),

            "evidence_available":
                evidence_available,

            "evidence_sufficient":
                evidence_sufficient,

            "requires_specialized_agent":
                False,

            "specialized_agent":
                None,

            "missing_information":
                analysis.get(
                    "missing_information",
                    []
                ),

            "confidence":
                (
                    "Grounded"
                    if evidence_sufficient
                    else "General knowledge"
                )
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
You are the query-understanding component of AgriSphere AI.

Your task is to understand the user's question.
DO NOT answer the question.

The user is interacting with an agriculture-focused
AI assistant.

The Knowledge Agent should handle normal agricultural
knowledge and educational questions.

Examples:

- What is soil pH?
- What are plant nutrients?
- Why is nitrogen important?
- What is NPK?
- What is crop rotation?
- What is organic farming?
- What is irrigation?
- Why do leaves turn yellow?
- How can soil fertility be improved?
- What is photosynthesis?
- What is mulching?
- What is intercropping?
- What causes fungal diseases?
- How can pests be controlled?

These should normally remain inside the Knowledge Agent.

ONLY identify a specialized agent when the question
requires information that another specialized agent
is specifically designed to provide.

SPECIALIZED AGENTS:

Market Intelligence Agent:
- current mandi prices
- current market conditions
- market trends
- selling decisions based on current market data

Climate Intelligence Agent:
- current weather
- current forecast
- location-specific weather
- current climate conditions

Government Scheme Agent:
- current government schemes
- current eligibility
- current subsidy information
- current application information

Crop Planning Agent:
- crop selection based on soil/location/conditions
- crop suitability analysis
- detailed crop planning decisions

Crop Health Agent:
- image-based crop disease/health diagnosis

IMPORTANT:

A general agriculture question is NOT a specialized-agent
question.

For example:

"What fertilizer is good for nitrogen deficiency?"
is agricultural knowledge.

"Why are plant leaves yellow?"
is agricultural knowledge.

"What is the best soil for wheat?"
is agricultural knowledge unless the user is asking
for a complete crop-selection recommendation.

FOLLOW-UP QUESTIONS:

Use the conversation context.

For example:

Previous:
"What is NPK?"

Current:
"Which one helps leaf growth?"

The search query should become something like:

"Which NPK nutrient helps leaf and vegetative growth?"

Another example:

Previous:
"What causes yellow leaves?"

Current:
"How can I prevent it?"

The search query should include the relevant context
about yellow leaves.

Do NOT ask for information that is unnecessary.

A question such as:

"What is photosynthesis?"

does not require crop, location or season.

Only mark clarification as necessary when the question
cannot reasonably be answered without missing information.

========================================
CURRENT QUESTION
========================================

{question}

========================================
CONVERSATION CONTEXT
========================================

{json.dumps(
    conversation_context,
    indent=2,
    ensure_ascii=False
)}

========================================
RETURN ONLY VALID JSON
========================================

{{
    "topic": "agriculture",
    "intent": "agricultural_knowledge",
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

            result = json.loads(
                text
            )

            return self._normalize_analysis(
                result,
                question
            )

        except Exception as e:

            print(
                "Query analysis error:",
                e
            )

            # Safe fallback:
            # treat the question as normal
            # agriculture knowledge.

            return {

                "topic":
                    "agriculture",

                "intent":
                    "agricultural_knowledge",

                "crop":
                    None,

                "location":
                    None,

                "season":
                    None,

                "crop_stage":
                    None,

                "symptoms":
                    [],

                "user_goal":
                    None,

                "needs_clarification":
                    False,

                "missing_information":
                    [],

                "clarification_question":
                    None,

                "search_query":
                    question,

                "requires_specialized_agent":
                    False,

                "specialized_agent":
                    None
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

            "topic":
                "agriculture",

            "intent":
                "agricultural_knowledge",

            "crop":
                None,

            "location":
                None,

            "season":
                None,

            "crop_stage":
                None,

            "symptoms":
                [],

            "user_goal":
                None,

            "needs_clarification":
                False,

            "missing_information":
                [],

            "clarification_question":
                None,

            "search_query":
                question,

            "requires_specialized_agent":
                False,

            "specialized_agent":
                None
        }

        for key, value in defaults.items():

            if key not in result:

                result[key] = value

        # -----------------------------------------------------
        # NEVER ROUTE TO KNOWLEDGE AGENT ITSELF
        # -----------------------------------------------------

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

            result[
                "requires_specialized_agent"
            ] = False

            result[
                "specialized_agent"
            ] = None

        # -----------------------------------------------------
        # SAFETY CHECK FOR SEARCH QUERY
        # -----------------------------------------------------

        if not result.get(
            "search_query"
        ):

            result[
                "search_query"
            ] = question

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
        ).lower().strip()

        # -----------------------------------------------------
        # MARKET
        # -----------------------------------------------------

        if intent in [
            "market",
            "current_market",
            "market_price",
            "market_trend"
        ]:

            return {

                "requires_specialized_agent":
                    True,

                "specialized_agent":
                    "Market Intelligence Agent",

                "message":
                    (
                        "This question requires current "
                        "market information. Please use "
                        "the Market Intelligence Agent."
                    )
            }

        # -----------------------------------------------------
        # WEATHER / CLIMATE
        # -----------------------------------------------------

        if intent in [
            "weather",
            "weather_agriculture",
            "current_weather",
            "climate_current"
        ]:

            return {

                "requires_specialized_agent":
                    True,

                "specialized_agent":
                    "Climate Intelligence Agent",

                "message":
                    (
                        "This question requires current "
                        "weather or climate information. "
                        "Please use the Climate Intelligence Agent."
                    )
            }

        # -----------------------------------------------------
        # GOVERNMENT SCHEMES
        # -----------------------------------------------------

        if intent in [
            "government_scheme",
            "current_scheme",
            "government_subsidy"
        ]:

            return {

                "requires_specialized_agent":
                    True,

                "specialized_agent":
                    "Government Scheme Agent",

                "message":
                    (
                        "This question requires current "
                        "government scheme information. "
                        "Please use the Government Scheme Agent."
                    )
            }

        # -----------------------------------------------------
        # CROP PLANNING
        # -----------------------------------------------------

        if intent in [
            "crop_selection",
            "crop_planning",
            "crop_suitability"
        ]:

            return {

                "requires_specialized_agent":
                    True,

                "specialized_agent":
                    "Crop Planning Agent",

                "message":
                    (
                        "This question requires crop "
                        "suitability or crop planning analysis. "
                        "Please use the Crop Planning Agent."
                    )
            }

        # -----------------------------------------------------
        # CROP HEALTH
        # -----------------------------------------------------

        if intent in [
            "crop_health_image",
            "disease_image",
            "plant_diagnosis"
        ]:

            return {

                "requires_specialized_agent":
                    True,

                "specialized_agent":
                    "Crop Health Agent",

                "message":
                    (
                        "This question requires crop health "
                        "or image-based disease analysis. "
                        "Please use the Crop Health Agent."
                    )
            }

        # -----------------------------------------------------
        # NORMAL KNOWLEDGE
        # -----------------------------------------------------

        return {

            "requires_specialized_agent":
                False,

            "specialized_agent":
                None
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
                "No relevant agricultural documents "
                "were retrieved."
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
                metadata.get(
                    "document_name"
                )
                or metadata.get(
                    "source"
                )
                or "Agricultural knowledge source"
            )

            page = metadata.get(
                "page"
            )

            if isinstance(
                page,
                int
            ):

                source += (
                    f", page {page + 1}"
                )

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
                "No usable agricultural information "
                "was retrieved."
            )

        return "\n".join(
            parts
        )

    # =========================================================
    # CHECK CONTEXT
    # =========================================================

    def _has_useful_context(
        self,
        context: str
    ) -> bool:

        if not context:

            return False

        invalid_messages = [
            "No relevant agricultural documents",
            "No usable agricultural information",
            "No relevant documents"
        ]

        for message in invalid_messages:

            if message in context:

                return False

        return len(
            context.strip()
        ) > 100

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

You are an agriculture-focused conversational
knowledge assistant.

Your job is to answer the user's question naturally,
clearly and accurately.

You should behave like a helpful agricultural expert
explaining concepts to a farmer or agriculture student.

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
AGRICULTURAL KNOWLEDGE
========================================

{context}

========================================
IMPORTANT RULES
========================================

1. ANSWER DIRECTLY.

Do not begin with:

"I can explain..."
"Based on the information..."
"According to the retrieved documents..."

Start with the actual answer.

2. UNDERSTAND CONTEXT.

If the user asks a follow-up question, use the
conversation context to understand what they mean.

Example:

User:
"What is NPK?"

Follow-up:
"Which one helps leaf growth?"

Understand that "which one" refers to the
NPK nutrients.

3. USE RETRIEVED KNOWLEDGE WHEN AVAILABLE.

The agricultural knowledge provided above is the
primary evidence for your answer.

Use it when relevant.

4. DO NOT REQUIRE AN EXACT SENTENCE.

You can combine related information from multiple
retrieved passages to explain the concept.

5. ACCURACY IS MORE IMPORTANT THAN COMPLETENESS.

Never invent specific agricultural facts.

Do NOT fabricate:

- fertilizer doses
- pesticide doses
- chemical concentrations
- market prices
- weather information
- government scheme eligibility
- subsidy amounts
- disease diagnoses
- crop yields
- scientific measurements

6. GENERAL AGRICULTURAL KNOWLEDGE.

If the retrieved documents do not completely cover
a simple educational agriculture question, you may
use reliable general agricultural knowledge to
complete the explanation.

However, do not invent specific numerical
recommendations.

For example, for:

"What is photosynthesis?"

you can provide a normal scientific explanation.

For:

"How many kg of fertilizer should I apply per acre?"

do not invent a number unless reliable information
supports the recommendation.

7. UNCERTAINTY.

When multiple causes are possible, say:

"Possible causes include..."

Do not present an uncertain diagnosis as a fact.

8. PRACTICAL QUESTIONS.

For "how to" questions, give clear numbered steps
when appropriate.

9. AGRICULTURE CONTEXT.

Prefer agriculture-related examples.

10. SPECIALIZED DATA.

Do not invent current information.

Current:

- market prices
- weather
- forecasts
- government schemes

should come from their respective specialized agents.

11. LANGUAGE.

Answer in the same language as the user whenever
practical.

12. FORMAT.

Use normal Markdown.

Use:

### headings

- bullet points

1. numbered steps

Do not output literal escaped newline characters.

13. ANSWER LENGTH.

For simple questions:
2-5 short paragraphs.

For complex questions:
use headings and detailed explanation.

14. DO NOT DISCUSS INTERNAL TECHNOLOGY.

Never mention:

- RAG
- FAISS
- embeddings
- vector databases
- Gemini
- prompts
- internal agents
- retrieval systems

unless the user specifically asks how AgriSphere works.

========================================
FINAL INSTRUCTION
========================================

Answer the user's question now.
"""

        try:

            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            answer = (
                response.text or ""
            ).strip()

            # -------------------------------------------------
            # FIX ESCAPED NEWLINES
            # -------------------------------------------------

            answer = answer.replace(
                "\\n",
                "\n"
            )

            # -------------------------------------------------
            # REMOVE ACCIDENTAL CODE FENCES
            # -------------------------------------------------

            if (
                answer.startswith("```")
                and answer.endswith("```")
            ):

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
                metadata.get(
                    "document_name"
                )
                or metadata.get(
                    "source"
                )
            )

            if (
                source
                and source not in sources
            ):

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

        if text.startswith(
            "```json"
        ):

            text = text[7:]

        elif text.startswith(
            "```"
        ):

            text = text[3:]

        if text.endswith(
            "```"
        ):

            text = text[:-3]

        return text.strip()