# Handles the interactive CLI workflow for updating existing BJJ wiki notes.
# Coordinates note resolution, fuzzy matching, generation, diff output, validation, and save confirmation.

from app.cli.output.diff_printer import print_diff
from app.cli.output.validation_printer import print_validation_result
from app.cli.spinner import Spinner
from app.matching.note_name_matcher import (
    find_exact_normalized_match,
    find_similar_note_names,
)
from app.repositories.note_repository import get_existing_note_titles
from app.services.note_update_service import generate_note_update, save_note_update


def handle_update(content):
    try:
        parts = content.split(" ", 1)

        if len(parts) < 2:
            print("\nUsage: /update <Note-Name> <new information>")
            print("Example: /update Knee-Elbow-Escape Neue Side-Control Variante gelernt.")
            return

        note_name = parts[0]
        new_info = parts[1]

        try:
            with Spinner("Updating note..."):
                update_result = generate_note_update(note_name, new_info)

        except FileNotFoundError:
            existing_titles = get_existing_note_titles()

            exact_match = find_exact_normalized_match(
                note_name,
                existing_titles,
            )

            if exact_match:
                note_name = exact_match

                with Spinner("Updating note..."):
                    update_result = generate_note_update(note_name, new_info)

            else:
                matches = find_similar_note_names(
                    note_name,
                    existing_titles,
                )

                if not matches:
                    print(f'\nNote not found: "{note_name}"')
                    return

                suggested_name = matches[0]

                print(f'\nNote not found: "{note_name}"')
                confirm_match = input(
                    f'Did you mean "{suggested_name}"? (y/n): '
                )

                if confirm_match.lower() != "y":
                    print("\nUpdate cancelled.")
                    return

                note_name = suggested_name

                with Spinner("Updating note..."):
                    update_result = generate_note_update(note_name, new_info)

        print_diff(
            update_result["old_content"],
            update_result["new_content"],
        )

        print_validation_result(update_result["validation_result"])

        confirm = input("\nSave update? (y/n): ")

        if confirm.lower() == "y":
            path = save_note_update(update_result)
            print(f"\nUpdated: {path}")
        else:
            print("\nUpdate cancelled.")

    except Exception as e:
        print(f"\nError: {e}")

    print("\n---\n")