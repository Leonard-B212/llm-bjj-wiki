# Formats wiki health check results for CLI output.

from app.cli.output.status_printer import print_success, print_warning


def print_check_summary(results):
    empty_notes = results["empty_notes"]
    misplaced_notes = results["misplaced_notes"]

    issues_found = False

    if empty_notes:
        print()
        print_warning(f"{len(empty_notes)} empty notes found")
        issues_found = True

    if misplaced_notes:
        if not issues_found:
            print()
        print_warning(f"{len(misplaced_notes)} misplaced notes found")
        issues_found = True

    if not issues_found:
        print_success("No wiki issues found")


def print_check_details(results):
    empty_notes = results["empty_notes"]
    misplaced_notes = results["misplaced_notes"]

    print("\nChecks\n")

    if empty_notes:
        print_warning(f"Empty notes: {len(empty_notes)}")

        for note_name in empty_notes:
            print(f"- {note_name}")
    else:
        print_success("Empty notes: 0")

    print()

    if misplaced_notes:
        print_warning(f"Misplaced notes: {len(misplaced_notes)}")

        for note_path in misplaced_notes:
            print(f"- {note_path}")
    else:
        print_success("Misplaced notes: 0")