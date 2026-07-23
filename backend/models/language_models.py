from pydantic import BaseModel


class LanguageRequest(BaseModel):
    text: str


class TranslationRequest(BaseModel):
    text: str
    target_language: str


class LanguageResponse(BaseModel):
    detected_language: str
    english_text: str


class TranslationResponse(BaseModel):
    translated_text: str