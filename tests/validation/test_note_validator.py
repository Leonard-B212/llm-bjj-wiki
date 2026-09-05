from app.validation.note_validator import (
    extract_wiki_links,
    find_forbidden_wiki_links,
)


def test_extract_wiki_links():
    content = "Move from [[Side-Control]] to [[North-South]]."

    assert extract_wiki_links(content) == [
        "Side-Control",
        "North-South",
    ]


def test_find_forbidden_wiki_links():
    content = "Use an [[Underhook]] during the [[Scramble]]."

    assert find_forbidden_wiki_links(content) == [
        "Underhook",
        "Scramble",
    ]


def test_allows_valid_wiki_links():
    content = "Move from [[Side-Control]] to [[North-South]]."

    assert find_forbidden_wiki_links(content) == []


def test_no_wiki_links():
    content = "Use an Underhook during the Scramble."

    assert find_forbidden_wiki_links(content) == []


def test_guard_is_forbidden_as_wiki_link():
    content = "The technique starts from [[Guard]] and transitions to [[Closed-Guard]]."

    assert find_forbidden_wiki_links(content) == [
        "Guard",
    ]


def test_duplicate_forbidden_links_are_reported_once():
    content = "Use [[Scramble]], then later return to another [[Scramble]]."

    assert find_forbidden_wiki_links(content) == [
        "Scramble",
    ]