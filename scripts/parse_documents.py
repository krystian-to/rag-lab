import argparse
from pathlib import Path

from app.ingestion.pipeline import parse_pdf_directory


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Extract native text from PDF files.")
    parser.add_argument("source", nargs="?", type=Path, default=Path("data/raw"))
    parser.add_argument("--output", type=Path, default=Path("data/processed"))
    return parser


def main() -> None:
    args = build_parser().parse_args()
    output_paths = parse_pdf_directory(args.source, args.output)
    print(f"Parsed {len(output_paths)} document(s).")
    for output_path in output_paths:
        print(output_path)


if __name__ == "__main__":
    main()

