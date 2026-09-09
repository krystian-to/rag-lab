from pathlib import Path

from app.ingestion.chunker import ChunkingConfig, chunk_pages
from app.ingestion.ocr import OcrEngine, OcrPolicy
from app.ingestion.pdf_parser import parse_pdf


def _pdf_paths(source_dir: Path) -> list[Path]:
    return sorted(
        (path for path in source_dir.iterdir() if path.suffix.lower() == ".pdf"),
        key=lambda path: path.name.lower(),
    )


def parse_pdf_directory(
    source_dir: Path,
    output_dir: Path,
    *,
    ocr_engine: OcrEngine | None = None,
    ocr_policy: OcrPolicy | None = None,
) -> list[Path]:
    """Parse every PDF in a directory and write one JSONL file per document."""

    if not source_dir.is_dir():
        raise NotADirectoryError(source_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []

    for pdf_path in _pdf_paths(source_dir):
        pages = parse_pdf(pdf_path, ocr_engine=ocr_engine, ocr_policy=ocr_policy)
        output_path = output_dir / f"{pages[0].document_id}.pages.jsonl"
        serialized_pages = "\n".join(page.model_dump_json() for page in pages)
        output_path.write_text(f"{serialized_pages}\n", encoding="utf-8")
        output_paths.append(output_path)

    return output_paths


def process_pdf_directory(
    source_dir: Path,
    output_dir: Path,
    *,
    chunking_config: ChunkingConfig | None = None,
    ocr_engine: OcrEngine | None = None,
    ocr_policy: OcrPolicy | None = None,
) -> list[Path]:
    """Parse PDFs and write page-level plus retrieval-chunk JSONL artifacts."""

    if not source_dir.is_dir():
        raise NotADirectoryError(source_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []

    for pdf_path in _pdf_paths(source_dir):
        pages = parse_pdf(pdf_path, ocr_engine=ocr_engine, ocr_policy=ocr_policy)
        document_id = pages[0].document_id

        page_path = output_dir / f"{document_id}.pages.jsonl"
        serialized_pages = "\n".join(page.model_dump_json() for page in pages)
        page_path.write_text(f"{serialized_pages}\n", encoding="utf-8")

        chunks = chunk_pages(pages, chunking_config)
        chunk_path = output_dir / f"{document_id}.chunks.jsonl"
        serialized_chunks = "\n".join(chunk.model_dump_json() for chunk in chunks)
        chunk_path.write_text(
            f"{serialized_chunks}\n" if serialized_chunks else "",
            encoding="utf-8",
        )
        output_paths.extend((page_path, chunk_path))

    return output_paths
