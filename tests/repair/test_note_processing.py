from app.repair.note_processing import process_note


def test_process_note_returns_clean_content_unchanged():
    content = "Maintain control from [[Side-Control]]."

    result = process_note(content)

    assert result["content"] == content
    assert result["repairs_applied"] == []
    assert result["validation_result"] == {
        "forbidden_wiki_links": [],
        "perspective_aliases": {},
    }


def test_process_note_repairs_validation_issues():
    content = "Use [[Scramble]] from [[Top-Side-Control]]."

    result = process_note(content)

    assert result["content"] == "Use Scramble from [[Side-Control]]."

    assert result["validation_result"] == {
        "forbidden_wiki_links": [],
        "perspective_aliases": {},
    }

    assert len(result["repairs_applied"]) == 2