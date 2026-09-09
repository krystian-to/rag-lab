from app.ingestion.cleaner import clean_pages, clean_text
from app.ingestion.models import ParsedPage


def test_clean_text_normalizes_pdf_line_breaks_and_whitespace() -> None:
    text = "Taxi-out  time\r\npre-\ndiction.\n\n\nNext paragraph.\x00"

    assert clean_text(text) == "Taxi-out time prediction.\n\nNext paragraph."


def test_clean_pages_preserves_provenance() -> None:
    page = ParsedPage(
        document_id="manual",
        filename="manual.pdf",
        page_number=7,
        text="A\nline",
        used_ocr=True,
    )

    assert clean_pages([page])[0] == page.model_copy(update={"text": "A line"})
