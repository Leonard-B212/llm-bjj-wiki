import os

from app.config import VAULT_PATH


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