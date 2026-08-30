from fastapi import APIRouter, HTTPException

from agents.knowledge_agent import KnowledgeAgent

from models.knowledge_models import (
    KnowledgeRequest,
    KnowledgeResponse
)


# =========================================================
# ROUTER
# =========================================================

router = APIRouter(
    prefix="/knowledge",
    tags=["Knowledge Assistant"]
)


# =========================================================
# AGENT
# =========================================================

agent = KnowledgeAgent()


# =========================================================
# ASK KNOWLEDGE AGENT
# =========================================================

@router.post(
    "/ask",
    response_model=KnowledgeResponse
)
def ask_question(
    request: KnowledgeRequest
):

    # -----------------------------------------------------
    # Validate question
    # -----------------------------------------------------

    question = (
        request.question
        .strip()
    )

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Please enter an agricultural question."
        )

    # -----------------------------------------------------
    # Knowledge Agent
    # -----------------------------------------------------

    try:

        result = agent.ask(
            question
        )

        return result

    # -----------------------------------------------------
    # Expected user/input errors
    # -----------------------------------------------------

    except ValueError as e:

        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

    # -----------------------------------------------------
    # Knowledge/RAG configuration errors
    # -----------------------------------------------------

    except FileNotFoundError as e:

        raise HTTPException(
            status_code=503,
            detail=str(e)
        )

    # -----------------------------------------------------
    # Unexpected errors
    # -----------------------------------------------------

    except Exception as e:

        print(
            f"Knowledge Agent error: {e}"
        )

        raise HTTPException(
            status_code=500,
            detail=(
                "The Knowledge Agent could not "
                "process the question."
            )
        )