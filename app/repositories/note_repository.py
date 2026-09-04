# Handles all filesystem access to Markdown notes in the configured BJJ vault.
# Keeps vault-specific file operations and note type folder mappings out of application services.

import os

from app.config import VAULT_PATH, TYPE_TO_FOLDER


# Loads all Markdown notes from the vault in the format expected by the retrieval pipeline.
def load_notes():
    notes = []

    for root, dirs, files in os.walk(VAULT_PATH):
        for filename in files:
            if filename.endswith(".md"):
                path = os.path.join(root, filename)

                with open(path, "r", encoding="utf-8") as file:
                    content = file.read()

                notes.append({
                    "id": path,
                    "title": filename.replace(".md", ""),
                    "path": path,
                    "content": content
                })

    return notes


def get_existing_note_titles():
    titles = []

    for root, dirs, files in os.walk(VAULT_PATH):
        for filename in files:
            if filename.endswith(".md"):
                titles.append(filename.replace(".md", ""))

    return sorted(titles)


# Finds the filesystem path of a note across all configured note type folders.
def find_note_path(note_name):
    filename = f"{note_name}.md"

    for folder in TYPE_TO_FOLDER.values():
        path = os.path.join(VAULT_PATH, folder, filename)

        if os.path.exists(path):
            return path

    raise FileNotFoundError(f"Note not found: {filename}")


# Finds a note and derives its note type from the folder it is stored in.
def find_note(note_name):
    filename = f"{note_name}.md"

    for note_type, folder in TYPE_TO_FOLDER.items():
        path = os.path.join(VAULT_PATH, folder, filename)

        if os.path.exists(path):
            return {
                "path": path,
                "note_type": note_type,
            }

    raise FileNotFoundError(f"Note not found: {filename}")


def read_note(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


# Builds the target path for a note and ensures its type-specific folder exists.
def build_note_path(note_type, filename):
    folder = TYPE_TO_FOLDER.get(note_type)

    if not folder:
        raise ValueError(f"No folder mapping for type: {note_type}")

    folder_path = os.path.join(VAULT_PATH, folder)
    os.makedirs(folder_path, exist_ok=True)

    return os.path.join(folder_path, filename)


def write_note(file_path, content):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(content)

    return file_path