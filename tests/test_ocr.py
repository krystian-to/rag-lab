import pymupdf

from app.ingestion.ocr import OcrPolicy, needs_ocr


class FakeOcrEngine:
    def __init__(self, recognized_text: str) -> None:
        self.recognized_text = recognized_text
        self.calls = 0

    def extract_text(self, page: pymupdf.Page) -> str:
        self.calls += 1
        return self.recognized_text


def test_empty_native_text_needs_ocr() -> None:
    assert needs_ocr("") is True


def test_substantial_native_text_does_not_need_ocr() -> None:
    assert needs_ocr("Taxi-out starts when the aircraft leaves the stand.") is False


def test_symbol_heavy_extraction_needs_ocr() -> None:
    text = "A1" + "#%!?" * 10
    policy = OcrPolicy(min_alphanumeric_characters=2, min_alphanumeric_ratio=0.5)

    assert needs_ocr(text, policy) is True

