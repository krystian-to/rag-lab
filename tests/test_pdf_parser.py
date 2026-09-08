from pathlib import Path

import pymupdf
import pytest

from app.ingestion.pdf_parser import document_id_from_path, parse_pdf


@pytest.fixture
def sample_pdf(tmp_path: Path) -> Path:
    pdf_path = tmp_path / "Data Description.pdf"
    document = pymupdf.open()
    text_page = document.new_page()
    text_page.insert_text((72, 72), "Taxi-out starts at off-block time.")
    document.new_page()
    document.save(pdf_path)
    document.close()
    return pdf_path


def test_parse_pdf_extracts_text_and_provenance(sample_pdf: Path) -> None:
    pages = parse_pdf(sample_pdf)

    assert len(pages) == 2
    assert pages[0].document_id == "data-description"
    assert pages[0].filename == "Data Description.pdf"
    assert pages[0].page_number == 1
    assert pages[0].text == "Taxi-out starts at off-block time."
    assert pages[0].used_ocr is False


def test_parse_pdf_preserves_empty_pages(sample_pdf: Path) -> None:
    pages = parse_pdf(sample_pdf)

    assert pages[1].page_number == 2
    assert pages[1].text == ""


def test_document_id_is_stable_for_the_same_filename() -> None:
    first = document_id_from_path(Path("first/Data Description.pdf"))
    second = document_id_from_path(Path("elsewhere/Data Description.pdf"))

    assert first == second == "data-description"


def test_parse_pdf_rejects_non_pdf(tmp_path: Path) -> None:
    text_path = tmp_path / "notes.txt"
    text_path.write_text("not a PDF", encoding="utf-8")

    with pytest.raises(ValueError, match="Expected a PDF"):
        parse_pdf(text_path)

