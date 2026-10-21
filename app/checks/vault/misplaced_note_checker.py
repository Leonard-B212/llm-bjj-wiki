# Detects Markdown notes that are stored outside configured technique type folders.

import os

from app.config import VAULT_PATH, TYPE_TO_FOLDER


def find_misplaced_notes(notes):
    valid_folders = {
        os.path.normpath(os.path.join(VAULT_PATH, folder))
        for folder in TYPE_TO_FOLDER.values()
    }

    misplaced_notes = []

    for note in notes:
        note_folder = os.path.normpath(
            os.path.dirname(note["path"])
        )

        if note_folder not in valid_folders:
            relative_path = os.path.relpath(
                note["path"],
                VAULT_PATH,
            )
            misplaced_notes.append(relative_path)

    return misplaced_notes