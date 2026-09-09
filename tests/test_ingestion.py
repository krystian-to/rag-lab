import json
from pathlib import Path

import pymupdf

from app.ingestion.chunker import ChunkingConfig
from app.ingestion.pipeline import parse_pdf_directory, process_pdf_directory


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


def test_process_pdf_directory_writes_pages_and_chunks_for_uppercase_pdf(
    tmp_path: Path,
) -> None:
    source_dir = tmp_path / "raw"
    output_dir = tmp_path / "processed"
    source_dir.mkdir()

    document = pymupdf.open()
    document.new_page().insert_text((72, 72), "one two three")
    document.new_page().insert_text((72, 72), "four five six")
    document.save(source_dir / "Manual.PDF")
    document.close()

    output_paths = process_pdf_directory(
        source_dir,
        output_dir,
        chunking_config=ChunkingConfig(target_tokens=4, overlap_tokens=1),
    )

    assert output_paths == [
        output_dir / "manual.pages.jsonl",
        output_dir / "manual.chunks.jsonl",
    ]
    chunks = [
        json.loads(line)
        for line in output_paths[1].read_text(encoding="utf-8").splitlines()
    ]
    assert [(chunk["page_start"], chunk["page_end"]) for chunk in chunks] == [
        (1, 2),
        (2, 2),
    ]
