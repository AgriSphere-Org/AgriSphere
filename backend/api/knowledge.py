from fastapi import APIRouter, HTTPException

from agents.knowledge_agent import KnowledgeAgent

from models.knowledge_models import (

    KnowledgeRequest,

    KnowledgeResponse

)

router = APIRouter(

    prefix="/knowledge",

    tags=["Knowledge Assistant"]

)

agent = KnowledgeAgent()


@router.post(

    "/ask",

    response_model=KnowledgeResponse

)

def ask_question(

    request: KnowledgeRequest

):

    try:

        result = agent.ask(

            request.question

        )

        return result

    except Exception as e:

        raise HTTPException(

            status_code=500,

            detail=str(e)

        )