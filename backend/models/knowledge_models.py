from typing import List, Optional

from pydantic import BaseModel, Field


# =========================================================
# KNOWLEDGE REQUEST
# =========================================================

class KnowledgeRequest(BaseModel):
    """
    Request sent to the Knowledge Agent.
    """

    question: str = Field(
        ...,
        min_length=1,
        description="User's agricultural question."
    )


# =========================================================
# KNOWLEDGE SOURCE
# =========================================================

class KnowledgeSource(BaseModel):
    """
    Agricultural evidence used to construct the answer.
    """

    source: str

    page: Optional[int] = None

    relevance: Optional[float] = None


# =========================================================
# KNOWLEDGE RESPONSE
# =========================================================

class KnowledgeResponse(BaseModel):
    """
    Response returned by the Knowledge Agent.
    """

    question: str

    answer: str

    sources: List[str] = Field(
        default_factory=list
    )

    # -----------------------------------------------------
    # Understanding
    # -----------------------------------------------------

    topic: Optional[str] = None

    intent: Optional[str] = None

    crop: Optional[str] = None

    # -----------------------------------------------------
    # Evidence status
    # -----------------------------------------------------

    evidence_available: bool = False

    evidence_sufficient: bool = False

    # -----------------------------------------------------
    # Agent routing
    # -----------------------------------------------------

    requires_specialized_agent: bool = False

    specialized_agent: Optional[str] = None

    # -----------------------------------------------------
    # Additional information
    # -----------------------------------------------------

    missing_information: List[str] = Field(
        default_factory=list
    )

    confidence: Optional[str] = None