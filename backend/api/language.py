from fastapi import APIRouter, HTTPException

from agents.language_agent import LanguageAgent
from models.language_models import (
    LanguageRequest,
    TranslationRequest,
    LanguageResponse,
    TranslationResponse,
)

router = APIRouter(
    prefix="/language",
    tags=["Language"]
)

language_agent = LanguageAgent()


@router.post(
    "/detect",
    response_model=LanguageResponse
)
def detect_language(request: LanguageRequest):
    """
    Detect the language of the input text and
    translate it to English.
    """

    try:

        result = language_agent.process_question(
            request.text
        )

        return LanguageResponse(
            detected_language=result["detected_language"],
            english_text=result["english_question"]
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post(
    "/translate",
    response_model=TranslationResponse
)
def translate_text(request: TranslationRequest):
    """
    Translate English text into the requested language.
    """

    try:

        translated = language_agent.translate(
            request.text,
            request.target_language
        )

        return TranslationResponse(
            translated_text=translated
        )

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


@router.post("/detect-only")
def detect_only(request: LanguageRequest):
    """
    Detect only the language without translating.
    """

    try:

        language = language_agent.detect_language(
            request.text
        )

        return {
            "detected_language": language
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )