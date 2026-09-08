import re
from pathlib import Path

import pymupdf

from app.ingestion.models import ParsedPage
from app.ingestion.ocr import OcrEngine, OcrPolicy, needs_ocr


def document_id_from_path(pdf_path: Path) -> str:
    """Create a stable, readable ID from a PDF filename."""

    normalized = re.sub(r"[^a-z0-9]+", "-", pdf_path.stem.lower()).strip("-")
    if not normalized:
        raise ValueError(f"Cannot create a document ID from filename: {pdf_path.name}")
    return normalized


def parse_pdf(
    pdf_path: Path,
    *,
    ocr_engine: OcrEngine | None = None,
    ocr_policy: OcrPolicy | None = None,
) -> list[ParsedPage]:
    """Extract text from every page, using OCR only when configured and needed."""

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError(f"Expected a PDF file, got: {pdf_path.name}")
    if not pdf_path.is_file():
        raise FileNotFoundError(pdf_path)

    document_id = document_id_from_path(pdf_path)
    pages: list[ParsedPage] = []

    with pymupdf.open(pdf_path) as document:
        for page_index, page in enumerate(document):
            text = page.get_text("text", sort=True).strip()
            used_ocr = False

            if ocr_engine is not None and needs_ocr(text, ocr_policy):
                text = ocr_engine.extract_text(page).strip()
                used_ocr = True

            pages.append(
                ParsedPage(
                    document_id=document_id,
                    filename=pdf_path.name,
                    page_number=page_index + 1,
                    text=text,
                    used_ocr=used_ocr,
                )
            )

    return pages
