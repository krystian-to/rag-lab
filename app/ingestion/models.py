from pydantic import BaseModel, Field


class ParsedPage(BaseModel):
    """Text and provenance extracted from one PDF page."""

    document_id: str = Field(min_length=1)
    filename: str = Field(min_length=1)
    page_number: int = Field(ge=1)
    text: str
    used_ocr: bool = False

