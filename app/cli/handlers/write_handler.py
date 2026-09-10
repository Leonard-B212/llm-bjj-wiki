# Handles the interactive CLI workflow for creating BJJ wiki notes.
# Coordinates input validation, generation, preview, validation output, and save confirmation.

import os
import time

from app.cli.spinner import Spinner
from app.cli.input.multiline_input import read_multiline
from app.cli.output.validation_printer import print_validation_result
from app.cli.handlers.update_handler import handle_update
from app.config import TYPE_TO_FOLDER
from app.matching.note_name_matcher import (
    find_exact_normalized_match,
    find_similar_note_names,
)
from app.repositories.note_repository import get_existing_note_titles
from app.services.note_writer_service import generate_note_draft, save_note_draft

def ask_for_new_filename():
    while True:
        new_filename = input("New filename: ").strip()

        if new_filename:
            return new_filename

        print("Filename cannot be empty.")

def resolve_duplicate(filename, user_input):
    existing_titles = get_existing_note_titles()

    exact_match = find_exact_normalized_match(
        filename,
        existing_titles,
    )

    if exact_match:
        print(f'\nA note with this name already exists: "{exact_match}"')
        print("\n[u] Update existing note")
        print("[r] Rename new note")
        print("[c] Cancel")

        choice = input("\nChoice: ").lower()

        if choice == "u":
            if user_input:
                handle_update(f"{exact_match} {user_input}")
            else:
                handle_update(exact_match)

            return None

        if choice == "r":
            new_filename = ask_for_new_filename()
            return resolve_duplicate(new_filename, user_input)

        print("\nWrite cancelled.")
        return None

    matches = find_similar_note_names(
        filename,
        existing_titles,
    )

    if not matches:
        return filename

    suggested_name = matches[0]

    print(f'\nPossible duplicate found: "{suggested_name}"')
    print("\n[u] Update existing note")
    print("[r] Rename new note")
    print("[w] Write anyway")
    print("[c] Cancel")

    choice = input("\nChoice: ").lower()

    if choice == "u":
        if user_input:
            handle_update(f"{suggested_name} {user_input}")
        else:
            handle_update(suggested_name)

        return None

    if choice == "r":
        new_filename = ask_for_new_filename()
        return resolve_duplicate(new_filename, user_input)

    if choice == "w":
        return filename

    print("\nWrite cancelled.")
    return None

def handle_write(content):
    parts = content.split(" ", 1)

    if not parts[0].strip():
        print("\nUsage: /write <Note-Name> [description]")
        print("Example: /write Knee-Elbow-Escape")
        print("\n---\n")
        return

    filename = parts[0].strip()

    inline_user_input = (
        parts[1].strip()
        if len(parts) == 2 and parts[1].strip()
        else None
    )

    filename = resolve_duplicate(filename, inline_user_input)

    if filename is None:
        return

    if inline_user_input:
        user_input = inline_user_input
    else:
        user_input = read_multiline(
            prompt="Describe the technique:"
        )

        if user_input is None:
            print("\nWrite cancelled.")
            return

        if not user_input:
            print("\nWrite cancelled: description cannot be empty.")
            return

    with Spinner("Generating note..."):
        draft = generate_note_draft(filename, user_input)

    if draft["repairs_applied"]:
        print("\n✓ Formatting fixed.")
        time.sleep(0.5)

    print("\nFilename:")
    print(draft["filename"])

    print("\nContent:")
    print(draft["content"])

    print_validation_result(draft["validation_result"])

    folder = TYPE_TO_FOLDER.get(draft["note_type"], "Unknown")
    print(f"\n→ Will be saved in: {folder}")

    confirm = input("\nSave this note? (y/n): ")

    if confirm.lower() == "y":
        result = save_note_draft(draft)

        if not result["saved"] and result["reason"] == "exists":
            print("\nFile already exists:")
            print(os.path.basename(result["path"]))

            choice = input("[o] overwrite, [c] cancel: ").lower()

            if choice == "o":
                result = save_note_draft(draft, overwrite=True)
                print(f"\nOverwritten: {result['path']}")
            else:
                print("\nCancelled.")
        else:
            print(f"\nSaved to: {result['path']}")
    else:
        print("\nNot saved.")

    print("\n---\n")