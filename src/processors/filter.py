from __future__ import annotations

import re

from src.models.paper import Paper
from src.utils.text_utils import build_search_text, normalize_text


def match_keywords(text: str, keywords: list[str]) -> list[str]:
    normalized = normalize_text(text)
    hits: list[str] = []
    for keyword in keywords:
        keyword_n = normalize_text(keyword)
        if keyword_n and keyword_n in normalized:
            hits.append(keyword)
    return hits


def should_exclude(text: str, exclude_keywords: list[str]) -> bool:
    normalized = normalize_text(text)
    for keyword in exclude_keywords:
        keyword_n = normalize_text(keyword)
        if keyword_n and keyword_n in normalized:
            return True
    return False


def passes_venue_specific_rules(paper: Paper, search_text: str) -> bool:
    venue_name = normalize_text(paper.venue_name or paper.venue_raw)
    if venue_name == "nature communications":
        return re.search(r"\brobot(ic)?\b", search_text) is not None
    return True


def filter_papers(
    papers: list[Paper],
    include_keywords: list[str],
    exclude_keywords: list[str],
    require_include_match: bool = True,
) -> list[Paper]:
    filtered: list[Paper] = []
    for paper in papers:
        search_text = build_search_text(paper.title, paper.abstract)
        if should_exclude(search_text, exclude_keywords):
            continue
        if not passes_venue_specific_rules(paper, search_text):
            continue

        hits = match_keywords(search_text, include_keywords)
        if require_include_match and not hits:
            continue

        paper.keywords_matched = hits
        filtered.append(paper)
    return filtered
