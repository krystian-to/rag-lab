# PRC AI Research Assistant

Projekt edukacyjny RAG dla dokumentów lotniczych PRC.

## Aktualny stan — Phase 2

- FastAPI z endpointem `GET /health`
- odczyt tekstu z PDF przez PyMuPDF
- zapis stron i metadanych do JSONL
- wykrywanie stron wymagających OCR
- interfejs OCR (bez zainstalowanego silnika OCR)
- 3 publiczne dokumenty NASA: 34 strony o taxi-out i ML
- 10 testów

## Uruchomienie

```powershell
.\.venv\Scripts\Activate.ps1
python scripts/parse_documents.py
pytest -q
```

Pliki PDF umieszczamy w `data/raw`. Wyniki trafiają do `data/processed`.

## Najbliższy plan

1. Czyszczenie tekstu i chunking
2. Embeddingi i dense search w Qdrant
3. BM25, hybrid search i RRF
4. Reranking i ewaluacja retrievalu
5. Odpowiedzi LLM z cytowaniem źródeł

Neo4j, LangGraph i lokalny vLLM dodamy dopiero po działającym i zmierzonym podstawowym RAG.
