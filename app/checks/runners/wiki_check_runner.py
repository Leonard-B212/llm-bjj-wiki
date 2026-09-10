# Runs wiki health checks and returns their results in a structured format.

from app.checks.vault.empty_note_checker import find_empty_notes


def run_wiki_checks(notes):
    empty_notes = find_empty_notes(notes)

    return {
        "empty_notes": empty_notes,
    }