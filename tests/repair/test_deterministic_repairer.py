from app.repair.deterministic_repairer import (
    repair_forbidden_wiki_links,
    repair_perspective_aliases,
)


def test_repairs_forbidden_wiki_link():
    content = "Use [[Scramble]] to recover position."

    repaired_content, repairs = repair_forbidden_wiki_links(
        content,
        ["Scramble"],
    )

    assert repaired_content == "Use Scramble to recover position."
    assert repairs == [
        {
            "type": "forbidden_wiki_link",
            "from": "[[Scramble]]",
            "to": "Scramble",
        }
    ]


def test_repairs_all_occurrences_of_forbidden_wiki_link():
    content = "Use [[Scramble]], then later enter another [[Scramble]]."

    repaired_content, repairs = repair_forbidden_wiki_links(
        content,
        ["Scramble"],
    )

    assert repaired_content == "Use Scramble, then later enter another Scramble."
    assert repairs == [
        {
            "type": "forbidden_wiki_link",
            "from": "[[Scramble]]",
            "to": "Scramble",
        }
    ]


def test_does_not_modify_unreported_forbidden_link():
    content = "Use [[Scramble]] with an [[Underhook]]."

    repaired_content, repairs = repair_forbidden_wiki_links(
        content,
        ["Scramble"],
    )

    assert repaired_content == "Use Scramble with an [[Underhook]]."
    assert repairs == [
        {
            "type": "forbidden_wiki_link",
            "from": "[[Scramble]]",
            "to": "Scramble",
        }
    ]


def test_repairs_perspective_alias():
    content = "Maintain pressure from [[Top-Side-Control]]."

    repaired_content, repairs = repair_perspective_aliases(
        content,
        {
            "Top-Side-Control": "Side-Control",
        },
    )

    assert repaired_content == "Maintain pressure from [[Side-Control]]."
    assert repairs == [
        {
            "type": "perspective_alias",
            "from": "[[Top-Side-Control]]",
            "to": "[[Side-Control]]",
        }
    ]


def test_repairs_multiple_perspective_aliases():
    content = "Move from [[Top-Side-Control]] to [[Top-North-South]]."

    repaired_content, repairs = repair_perspective_aliases(
        content,
        {
            "Top-Side-Control": "Side-Control",
            "Top-North-South": "North-South",
        },
    )

    assert repaired_content == "Move from [[Side-Control]] to [[North-South]]."

    assert repairs == [
        {
            "type": "perspective_alias",
            "from": "[[Top-Side-Control]]",
            "to": "[[Side-Control]]",
        },
        {
            "type": "perspective_alias",
            "from": "[[Top-North-South]]",
            "to": "[[North-South]]",
        },
    ]