# Formats wiki health check results for CLI output.

from app.cli.output.status_printer import print_success, print_warning


def print_check_summary(results):
    empty_notes = results["empty_notes"]

    if not empty_notes:
        print_success("No empty notes found")
        return

    print()
    print_warning(f"{len(empty_notes)} empty notes found")


def print_check_details(results):
    empty_notes = results["empty_notes"]

    print("\nChecks\n")

    if not empty_notes:
        print_success("Empty notes: 0")
        return

    print_warning(f"Empty notes: {len(empty_notes)}")

    for note_name in empty_notes:
        print(f"- {note_name}")