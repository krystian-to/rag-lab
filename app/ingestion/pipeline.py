from pathlib import Path

from app.ingestion.pdf_parser import parse_pdf


def parse_pdf_directory(source_dir: Path, output_dir: Path) -> list[Path]:
    """Parse every PDF in a directory and write one JSONL file per document."""

    if not source_dir.is_dir():
        raise NotADirectoryError(source_dir)

    output_dir.mkdir(parents=True, exist_ok=True)
    output_paths: list[Path] = []

    for pdf_path in sorted(source_dir.glob("*.pdf")):
        pages = parse_pdf(pdf_path)
        output_path = output_dir / f"{pages[0].document_id}.pages.jsonl"
        serialized_pages = "\n".join(page.model_dump_json() for page in pages)
        output_path.write_text(f"{serialized_pages}\n", encoding="utf-8")
        output_paths.append(output_path)

    return output_paths

