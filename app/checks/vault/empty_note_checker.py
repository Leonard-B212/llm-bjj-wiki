# Detects empty Markdown notes in the configured BJJ vault.


def find_empty_notes(notes):
    empty_notes = []

    for note in notes:
        if not note["content"].strip():
            empty_notes.append(note["title"])

    return empty_notes