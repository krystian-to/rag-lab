from pydantic import BaseModel, Field


class ParsedPage(BaseModel):
    """Text and provenance extracted from one PDF page."""

    document_id: str = Field(min_length=1)
    filename: str = Field(min_length=1)
    page_number: int = Field(ge=1)
    text: str
    used_ocr: bool = False


class DocumentChunk(BaseModel):
    """A deterministic retrieval unit with source-page provenance."""

    chunk_id: str = Field(min_length=1)
    document_id: str = Field(min_length=1)
    filename: str = Field(min_length=1)
    page_start: int = Field(ge=1)
    page_end: int = Field(ge=1)
    text: str = Field(min_length=1)
    section: str | None = None
