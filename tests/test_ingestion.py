import json
from pathlib import Path

import pymupdf

from app.ingestion.pipeline import parse_pdf_directory


def test_parse_pdf_directory_writes_inspectable_jsonl(tmp_path: Path) -> None:
    source_dir = tmp_path / "raw"
    output_dir = tmp_path / "processed"
    source_dir.mkdir()

    document = pymupdf.open()
    document.new_page().insert_text((72, 72), "AOBT is a timestamp field.")
    document.save(source_dir / "fields.pdf")
    document.close()

    output_paths = parse_pdf_directory(source_dir, output_dir)

    assert output_paths == [output_dir / "fields.pages.jsonl"]
    records = [
        json.loads(line)
        for line in output_paths[0].read_text(encoding="utf-8").splitlines()
    ]
    assert records == [
        {
            "document_id": "fields",
            "filename": "fields.pdf",
            "page_number": 1,
            "text": "AOBT is a timestamp field.",
            "used_ocr": False,
        }
    ]

