# PRC AI Research Assistant

A step-by-step learning project for building and evaluating a retrieval-augmented generation (RAG) system over PRC aviation documents.

## Current status

Phase 1: the FastAPI shell is operational, and native PDF text extraction produces structured, page-level JSONL records with source provenance.

## Local Python environment

Activate the existing virtual environment in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Verify the interpreter:

```powershell
python --version
python -c "import sys; print(sys.executable)"
```

## Parse source documents

Place PDF files in `data/raw`, then run:

```powershell
python scripts/parse_documents.py
```

Page records are written to `data/processed/*.pages.jsonl`. The processed directory is intentionally ignored because its contents can be regenerated from source documents.

Native extraction is checked with a small OCR-candidate heuristic. The parser accepts an OCR engine through an explicit interface, but no system OCR provider is installed yet. Without a configured engine, suspicious or empty native text is preserved for inspection with `used_ocr=false`.
