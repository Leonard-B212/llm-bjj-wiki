from unittest.mock import Mock, patch

from app.services.note_update_service import generate_note_update


@patch("app.services.note_update_service.create_chat_completion")
@patch("app.services.note_update_service.get_existing_note_titles")
@patch("app.services.note_update_service.load_global_rules")
@patch("app.services.note_update_service.load_schema")
@patch("app.services.note_update_service.read_note")
@patch("app.services.note_update_service.find_note")
def test_existing_note_is_repaired_before_llm_update(
    mock_find_note,
    mock_read_note,
    mock_load_schema,
    mock_load_global_rules,
    mock_get_existing_note_titles,
    mock_create_chat_completion,
):
    mock_find_note.return_value = {
        "path": "fake/path/Side-Control.md",
        "note_type": "position",
    }

    mock_read_note.return_value = (
        "Maintain pressure from [[Top-Side-Control]] "
        "with an [[Underhook]]."
    )

    mock_load_schema.return_value = "# Schema"
    mock_load_global_rules.return_value = "# Rules"
    mock_get_existing_note_titles.return_value = ["Side-Control"]

    response = Mock()
    response.choices = [
        Mock(
            message=Mock(
                content="Maintain pressure from [[Side-Control]] with an Underhook."
            )
        )
    ]
    response.usage.prompt_tokens = 10
    response.usage.completion_tokens = 5
    response.usage.total_tokens = 15

    mock_create_chat_completion.return_value = response

    result = generate_note_update(
        "Side-Control",
        "Add new information.",
    )

    assert result["old_content"] == (
        "Maintain pressure from [[Side-Control]] "
        "with an Underhook."
    )

    call_args = mock_create_chat_completion.call_args
    messages = call_args.kwargs["messages"]
    prompt = messages[0]["content"]

    assert "[[Top-Side-Control]]" not in prompt
    assert "[[Underhook]]" not in prompt

    assert "[[Side-Control]]" in prompt
    assert "Underhook" in prompt