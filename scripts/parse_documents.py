import argparse
from pathlib import Path

from app.ingestion.pipeline import process_pdf_directory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Parse, clean, and chunk PDF files into JSONL artifacts."
    )
    parser.add_argument("source", nargs="?", type=Path, default=Path("data/raw"))
    parser.add_argument("--output", type=Path, default=Path("data/processed"))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_paths = process_pdf_directory(args.source, args.output)
    print(f"Wrote {len(output_paths)} artifact(s).")
    for output_path in output_paths:
        print(output_path)


if __name__ == "__main__":
    main()
