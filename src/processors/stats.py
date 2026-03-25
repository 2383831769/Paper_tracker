from __future__ import annotations

from src.models.paper import Paper


def build_venue_stats(
    fetched_papers: list[Paper],
    filtered_papers: list[Paper],
) -> list[dict[str, int | str]]:
    fetched_counts: dict[str, int] = {}
    filtered_counts: dict[str, int] = {}

    for paper in fetched_papers:
        venue = paper.venue_name or paper.venue_raw or "Unknown"
        fetched_counts[venue] = fetched_counts.get(venue, 0) + 1

    for paper in filtered_papers:
        venue = paper.venue_name or paper.venue_raw or "Unknown"
        filtered_counts[venue] = filtered_counts.get(venue, 0) + 1

    all_venues = sorted(set(fetched_counts) | set(filtered_counts))
    return [
        {
            "venue": venue,
            "fetched_count": fetched_counts.get(venue, 0),
            "filtered_count": filtered_counts.get(venue, 0),
        }
        for venue in all_venues
    ]
