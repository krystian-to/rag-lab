from dataclasses import dataclass
from typing import Protocol

import pymupdf


@dataclass(frozen=True)
class OcrPolicy:
    """Thresholds used to identify suspicious native text extraction."""

    min_alphanumeric_characters: int = 10
    min_alphanumeric_ratio: float = 0.5


class OcrEngine(Protocol):
    """Interface implemented by a concrete OCR provider."""

    def extract_text(self, page: pymupdf.Page) -> str:
        """Recognize text from the visual content of one PDF page."""


def needs_ocr(page_text: str, policy: OcrPolicy | None = None) -> bool:
    """Return whether native extraction looks too weak to trust by itself."""

    active_policy = policy or OcrPolicy()
    non_whitespace = [character for character in page_text if not character.isspace()]
    alphanumeric_count = sum(character.isalnum() for character in non_whitespace)

    if alphanumeric_count < active_policy.min_alphanumeric_characters:
        return True

    alphanumeric_ratio = alphanumeric_count / len(non_whitespace)
    return alphanumeric_ratio < active_policy.min_alphanumeric_ratio

