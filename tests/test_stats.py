from src.models.paper import Paper
from src.processors.stats import build_venue_stats


def _paper(paper_id: str, venue_name: str) -> Paper:
    return Paper(
        paper_id=paper_id,
        title="paper",
        abstract="abstract",
        authors=["A"],
        published_date="2026-03-24T00:00:00+00:00",
        updated_date="2026-03-24T00:00:00+00:00",
        source="openalex",
        primary_category="robotics",
        categories=["robotics"],
        arxiv_url="https://example.org",
        pdf_url="https://example.org/pdf",
        venue_name=venue_name,
        venue_raw=venue_name,
        venue_type="journal",
    )


def test_build_venue_stats_tracks_fetched_and_filtered_counts() -> None:
    fetched = [
        _paper("1", "Science Robotics"),
        _paper("2", "Science Robotics"),
        _paper("3", "Nature Machine Intelligence"),
    ]
    filtered = [
        _paper("1", "Science Robotics"),
        _paper("3", "Nature Machine Intelligence"),
    ]

    stats = build_venue_stats(fetched, filtered)

    assert stats == [
        {"venue": "Nature Machine Intelligence", "fetched_count": 1, "filtered_count": 1},
        {"venue": "Science Robotics", "fetched_count": 2, "filtered_count": 1},
    ]
