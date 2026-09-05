from unittest.mock import Mock

import app.cli.handlers.write_handler as write_handler


def test_exact_duplicate_can_be_redirected_to_update(monkeypatch):
    monkeypatch.setattr(
        write_handler,
        "get_existing_note_titles",
        lambda: ["Rear-Naked-Choke"],
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "u",
    )

    mock_update = Mock()
    monkeypatch.setattr(
        write_handler,
        "handle_update",
        mock_update,
    )

    result = write_handler.resolve_duplicate(
        "rear_naked_choke",
        "New finishing detail.",
    )

    assert result is None
    mock_update.assert_called_once_with(
        "Rear-Naked-Choke New finishing detail."
    )


def test_fuzzy_duplicate_can_be_ignored(monkeypatch):
    monkeypatch.setattr(
        write_handler,
        "get_existing_note_titles",
        lambda: ["Rear-Naked-Choke"],
    )
    monkeypatch.setattr(
        "builtins.input",
        lambda _: "w",
    )

    result = write_handler.resolve_duplicate(
        "Rear-Naked-Chok",
        "Technique description.",
    )

    assert result == "Rear-Naked-Chok"


def test_rename_runs_duplicate_check_again(monkeypatch):
    monkeypatch.setattr(
        write_handler,
        "get_existing_note_titles",
        lambda: ["Rear-Naked-Choke"],
    )

    answers = iter([
        "r",
        "Triangle-Choke",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers),
    )

    result = write_handler.resolve_duplicate(
        "rear_naked_choke",
        "Technique description.",
    )

    assert result == "Triangle-Choke"


def test_rename_rejects_empty_filename(monkeypatch):
    answers = iter([
        "",
        "   ",
        "Triangle-Choke",
    ])

    monkeypatch.setattr(
        "builtins.input",
        lambda _: next(answers),
    )

    result = write_handler.ask_for_new_filename()

    assert result == "Triangle-Choke"