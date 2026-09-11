# PRC AI Research Assistant

Projekt edukacyjny RAG dla dokumentów lotniczych PRC.

## Aktualny stan — Phase 3

- FastAPI z endpointem `GET /health`
- odczyt tekstu z PDF przez PyMuPDF
- zapis stron i metadanych do JSONL
- wykrywanie stron wymagających OCR
- interfejs OCR (bez zainstalowanego silnika OCR)
- ostrożne czyszczenie tekstu wyekstrahowanego z PDF
- deterministyczny chunking: około 500 słów/tokenów z overlapem 75
- metadane chunków z zakresem stron i stabilnym `chunk_id`
- 3 publiczne dokumenty NASA o taxi-out i ML oraz podręcznik Airport CDM
- 18 testów automatycznych

## Uruchomienie

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/parse_documents.py
pytest -q
```

Pliki PDF umieszczamy w `data/raw`. Dla każdego dokumentu skrypt zapisuje w
`data/processed` dwa czytelne pliki JSONL:

- `*.pages.jsonl` — surowy tekst i metadane każdej strony,
- `*.chunks.jsonl` — oczyszczone, nakładające się fragmenty do retrievalu.

## Co znajduje się w repozytorium

- `app/main.py` — utworzenie aplikacji FastAPI.
- `app/api/health.py` — endpoint kontrolny `GET /health`.
- `app/config.py` — ustawienia aplikacji i adres Qdrant.
- `app/ingestion/models.py` — modele strony PDF oraz chunku.
- `app/ingestion/pdf_parser.py` — ekstrakcja tekstu i metadanych przez PyMuPDF.
- `app/ingestion/ocr.py` — heurystyka i interfejs opcjonalnego OCR.
- `app/ingestion/cleaner.py` — normalizacja tekstu po ekstrakcji.
- `app/ingestion/chunker.py` — deterministyczny podział z overlapem.
- `app/ingestion/pipeline.py` — przetwarzanie katalogu PDF do plików JSONL.
- `scripts/parse_documents.py` — polecenie uruchamiające cały pipeline.
- `tests/` — testy API, parsera, OCR, czyszczenia, chunkingu i integracji.
- `data/raw/` — dokumenty źródłowe oraz rejestr `SOURCES.md`.

## Najbliższy plan

1. Embeddingi i dense search w Qdrant
2. BM25, hybrid search i RRF
3. Reranking i ewaluacja retrievalu
4. Odpowiedzi LLM z cytowaniem źródeł
