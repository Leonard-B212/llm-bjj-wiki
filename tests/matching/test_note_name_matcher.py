from app.matching.note_name_matcher import find_similar_note_names


def test_finds_similar_note_name():
    existing_titles = [
        "Rear-Naked-Choke",
        "Side-Control",
        "Butterfly-Sweep",
    ]

    matches = find_similar_note_names(
        "Rear-Nacked-Choke",
        existing_titles,
    )

    assert matches[0] == "Rear-Naked-Choke"


def test_returns_multiple_similar_matches():
    existing_titles = [
        "Armbar",
        "Armbar-From-Mount",
        "Armbar-From-Guard",
        "Triangle",
    ]

    matches = find_similar_note_names(
        "Armbar-From-Mout",
        existing_titles,
    )

    assert "Armbar-From-Mount" in matches


def test_returns_no_match_for_unrelated_name():
    existing_titles = [
        "Rear-Naked-Choke",
        "Side-Control",
        "Butterfly-Sweep",
    ]

    matches = find_similar_note_names(
        "Completely-Different-Technique",
        existing_titles,
    )

    assert matches == []


def test_respects_match_limit():
    existing_titles = [
        "Armbar",
        "Armbar-From-Mount",
        "Armbar-From-Guard",
        "Armbar-From-Side-Control",
    ]

    matches = find_similar_note_names(
        "Armbar-From",
        existing_titles,
        limit=2,
    )

    assert len(matches) <= 2