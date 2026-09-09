import re
import unicodedata

from app.ingestion.models import ParsedPage

_CONTROL_CHARACTERS = re.compile(r"[^\S\r\n\t]+|[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_LINE_BREAK_HYPHEN = re.compile(r"(?<=[^\W\d_])-\s*\n\s*(?=[^\W\d_])")
_SINGLE_LINE_BREAK = re.compile(r"(?<!\n)\n(?!\n)")
_EXCESSIVE_BLANK_LINES = re.compile(r"\n{3,}")


def clean_text(text: str) -> str:
    """Normalize common PDF extraction noise without discarding content."""

    normalized = (
        unicodedata.normalize("NFKC", text).replace("\r\n", "\n").replace("\r", "\n")
    )
    normalized = _CONTROL_CHARACTERS.sub(" ", normalized)
    normalized = re.sub(r"[ \t]+\n", "\n", normalized)
    normalized = re.sub(r"\n[ \t]+", "\n", normalized)
    normalized = _LINE_BREAK_HYPHEN.sub("", normalized)
    normalized = _SINGLE_LINE_BREAK.sub(" ", normalized)
    normalized = _EXCESSIVE_BLANK_LINES.sub("\n\n", normalized)
    normalized = re.sub(r"[ \t]{2,}", " ", normalized)
    return normalized.strip()


def clean_pages(pages: list[ParsedPage]) -> list[ParsedPage]:
    """Return cleaned copies while preserving all page-level provenance."""

    return [page.model_copy(update={"text": clean_text(page.text)}) for page in pages]
