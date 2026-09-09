import pytest

from app.ingestion.chunker import ChunkingConfig, chunk_pages
from app.ingestion.models import ParsedPage


def _page(number: int, text: str) -> ParsedPage:
    return ParsedPage(
        document_id="airport-manual",
        filename="airport-manual.pdf",
        page_number=number,
        text=text,
    )


def test_chunker_creates_no_empty_chunks() -> None:
    assert chunk_pages([_page(1, "  \n "), _page(2, "useful text")])[0].text == (
        "useful text"
    )
    assert chunk_pages([_page(1, "")]) == []


def test_chunk_ids_are_deterministic() -> None:
    pages = [_page(3, "one two three four five six")]
    config = ChunkingConfig(target_tokens=4, overlap_tokens=1)

    first = chunk_pages(pages, config)
    second = chunk_pages(pages, config)

    assert [chunk.chunk_id for chunk in first] == [
        "airport-manual-p3-c001",
        "airport-manual-p3-c002",
    ]
    assert first == second


def test_overlap_repeats_boundary_tokens() -> None:
    chunks = chunk_pages(
        [_page(1, "one two three four five six")],
        ChunkingConfig(target_tokens=4, overlap_tokens=2),
    )

    assert chunks[0].text.split()[-2:] == chunks[1].text.split()[:2]


def test_page_range_metadata_is_preserved() -> None:
    chunks = chunk_pages(
        [_page(4, "one two three"), _page(5, "four five three")],
        ChunkingConfig(target_tokens=4, overlap_tokens=1),
    )

    assert (chunks[0].page_start, chunks[0].page_end) == (4, 5)
    assert (chunks[1].page_start, chunks[1].page_end) == (5, 5)


def test_invalid_chunking_configuration_is_rejected() -> None:
    with pytest.raises(ValueError, match="smaller"):
        ChunkingConfig(target_tokens=5, overlap_tokens=5)
