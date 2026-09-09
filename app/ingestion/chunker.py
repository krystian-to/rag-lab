from dataclasses import dataclass

from app.ingestion.cleaner import clean_pages
from app.ingestion.models import DocumentChunk, ParsedPage


@dataclass(frozen=True)
class ChunkingConfig:
    """Initial chunking values to benchmark in later retrieval phases."""

    target_tokens: int = 500
    overlap_tokens: int = 75

    def __post_init__(self) -> None:
        if self.target_tokens < 1:
            raise ValueError("target_tokens must be positive")
        if self.overlap_tokens < 0:
            raise ValueError("overlap_tokens cannot be negative")
        if self.overlap_tokens >= self.target_tokens:
            raise ValueError("overlap_tokens must be smaller than target_tokens")


@dataclass(frozen=True)
class _PageToken:
    value: str
    page_number: int


def chunk_pages(
    pages: list[ParsedPage],
    config: ChunkingConfig | None = None,
) -> list[DocumentChunk]:
    """Clean pages and split them into overlapping, deterministic chunks.

    A whitespace-delimited item is used as an explicit token approximation. This
    keeps Phase 3 independent of the embedding model; model-specific tokenization
    can be benchmarked once that model is selected.
    """

    if not pages:
        return []

    document_id = pages[0].document_id
    filename = pages[0].filename
    if any(
        page.document_id != document_id or page.filename != filename for page in pages
    ):
        raise ValueError("All pages must belong to the same document")

    active_config = config or ChunkingConfig()
    tokens = [
        _PageToken(value=token, page_number=page.page_number)
        for page in clean_pages(pages)
        for token in page.text.split()
    ]
    if not tokens:
        return []

    chunks: list[DocumentChunk] = []
    step = active_config.target_tokens - active_config.overlap_tokens
    for start in range(0, len(tokens), step):
        window = tokens[start : start + active_config.target_tokens]
        if not window:
            break

        chunk_number = len(chunks) + 1
        page_start = window[0].page_number
        chunks.append(
            DocumentChunk(
                chunk_id=f"{document_id}-p{page_start}-c{chunk_number:03d}",
                document_id=document_id,
                filename=filename,
                page_start=page_start,
                page_end=window[-1].page_number,
                text=" ".join(token.value for token in window),
                section=None,
            )
        )

        if start + active_config.target_tokens >= len(tokens):
            break

    return chunks
