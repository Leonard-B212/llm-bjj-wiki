# Handles the interactive CLI workflow for creating BJJ wiki notes.
# Coordinates input validation, generation, preview, validation output, and save confirmation.

import os

from app.cli.spinner import Spinner
from app.cli.output.validation_printer import print_validation_result
from app.config import TYPE_TO_FOLDER
from app.services.note_writer_service import generate_note_draft, save_note_draft


def handle_write(content):
    parts = content.split(" ", 1)

    if len(parts) < 2:
        print("\nUsage: /write <Note-Name> <description>")
        print("Example: /write Knee-Elbow-Escape Escape aus der Side Control gegen Druck von oben.")
        print("\n---\n")
        return

    filename = parts[0]
    user_input = parts[1]

    with Spinner("Generating note..."):
        draft = generate_note_draft(filename, user_input)

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