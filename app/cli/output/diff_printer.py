# Formats and prints the differences between an existing note and its updated version.
# Only added and removed lines are shown to keep update previews concise.

import difflib


def print_diff(old_content, new_content):
    old_lines = old_content.splitlines()
    new_lines = new_content.splitlines()

    diff = difflib.unified_diff(
        old_lines,
        new_lines,
        fromfile="OLD",
        tofile="NEW",
        lineterm=""
    )

    print("\n--- CHANGES ---")

    for line in diff:
        if line.startswith("+") and not line.startswith("+++"):
            print(f"+ {line[1:]}")
        elif line.startswith("-") and not line.startswith("---"):
            print(f"- {line[1:]}")