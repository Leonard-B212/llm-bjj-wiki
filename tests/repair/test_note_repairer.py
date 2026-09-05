from app.repair.note_repairer import repair_note


def test_repair_note_applies_all_deterministic_repairs():
    content = """
Use an [[Underhook]] from [[Top-Side-Control]]
during a [[Scramble]].
"""

    validation_result = {
        "forbidden_wiki_links": [
            "Underhook",
            "Scramble",
        ],
        "perspective_aliases": {
            "Top-Side-Control": "Side-Control",
        },
    }

    result = repair_note(content, validation_result)

    assert "[[Underhook]]" not in result["content"]
    assert "[[Scramble]]" not in result["content"]
    assert "[[Top-Side-Control]]" not in result["content"]

    assert "Underhook" in result["content"]
    assert "Scramble" in result["content"]
    assert "[[Side-Control]]" in result["content"]

    assert result["validation_result"] == {
        "forbidden_wiki_links": [],
        "perspective_aliases": {},
    }

    assert len(result["repairs_applied"]) == 3


def test_repair_note_does_nothing_when_validation_is_clean():
    content = "Maintain control from [[Side-Control]]."

    validation_result = {
        "forbidden_wiki_links": [],
        "perspective_aliases": {},
    }

    result = repair_note(content, validation_result)

    assert result["content"] == content
    assert result["repairs_applied"] == []
    assert result["validation_result"] == {
        "forbidden_wiki_links": [],
        "perspective_aliases": {},
    }


def test_repair_note_preserves_unrelated_content():
    content = """
# Execution

Control the opponent carefully.

Use [[Scramble]] only when necessary.

Transition to [[Side-Control]] afterward.
"""

    validation_result = {
        "forbidden_wiki_links": ["Scramble"],
        "perspective_aliases": {},
    }

    result = repair_note(content, validation_result)

    assert "# Execution" in result["content"]
    assert "Control the opponent carefully." in result["content"]
    assert "Transition to [[Side-Control]] afterward." in result["content"]
    assert "Use Scramble only when necessary." in result["content"]