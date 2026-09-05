# Entry point for the interactive BJJ LLM Wiki CLI.
# Coordinates command handling and delegates application logic to the corresponding services.

import os

from app.repositories.note_repository import load_notes, get_existing_note_titles
from app.matching.note_name_matcher import (
    find_exact_normalized_match,
    find_similar_note_names,
)
from app.vectorstore.chroma_store import add_notes, reset_collection
from app.services.rag_service import ask
from app.cli.command_handler import handle_command
from app.services.note_writer_service import generate_note_draft, save_note_draft, load_global_rules
from app.config import LANGUAGE, TYPE_TO_FOLDER, VAULT_PATH
from app.services.note_update_service import generate_note_update, save_note_update
from app.cli.diff_printer import print_diff
from app.cli.spinner import Spinner


# Rebuilds the vector index from the current Markdown notes in the configured vault.
def reindex_notes():
    notes = load_notes()
    reset_collection()
    add_notes(notes)

# Prints validation warnings returned by the deterministic note validator.
def print_validation_result(validation_result):
    forbidden_links = validation_result["forbidden_wiki_links"]
    perspective_aliases = validation_result["perspective_aliases"]

    if not forbidden_links and not perspective_aliases:
        return

    print("\nValidation warnings:")

    for link in forbidden_links:
        print(f"- Generic BJJ concept should not be a Wiki-Link: [[{link}]]")

    for alias, canonical in perspective_aliases.items():
        print(f"- Perspective-specific Wiki-Link: [[{alias}]] → [[{canonical}]]")


def print_banner():
    print(r"""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║          🥋  B J J   L L M   W I K I  🥋     ║
    ║                                              ║
    ╠══════════════════════════════════════════════╣
    ║  ✓ Notes indexed                             ║
    ║  ✓ Embeddings loaded                         ║
    ║  ✓ ChromaDB ready                            ║
    ║  ✓ OpenAI configured                         ║
    ╠══════════════════════════════════════════════╣
    ║                                              ║
    ║                 OSS. 🤙                      ║
    ║              Ready to Roll                   ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
""")


def print_sources(sources):
    print("\nSources:")
    for source in sources:
        print(f"- {os.path.basename(source)}")


# Initializes the index and runs the interactive command loop.
def main():
    
    reindex_notes()
    print_banner()
    print(f"Vault: {VAULT_PATH}")
    print(f"Content language: {LANGUAGE}\n")
    print("Commands: /exit, /reindex, /write <filename> <description>, /update <filename> <new information>\n")

    while True:
        user_input = input(">> ")
        cmd = handle_command(user_input)

        if cmd["type"] == "exit":
            break

        elif cmd["type"] == "reindex":
            reindex_notes()
            continue

        elif cmd["type"] == "write":
            parts = cmd["content"].split(" ", 1)

            if len(parts) < 2:
                print("\nUsage: /write <Note-Name> <description>")
                print("Example: /write Knee-Elbow-Escape Escape aus der Side Control gegen Druck von oben.")
                print("\n---\n")
                continue

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
            continue

        elif cmd["type"] == "unknown":
            print("Unknown command.")
            continue

        elif cmd["type"] == "update":
            try:
                parts = cmd["content"].split(" ", 1)

                if len(parts) < 2:
                    print("\nUsage: /update <Note-Name> <new information>")
                    print("Example: /update Knee-Elbow-Escape Neue Side-Control Variante gelernt.")
                    continue

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
                            continue

                        suggested_name = matches[0]

                        print(f'\nNote not found: "{note_name}"')
                        confirm_match = input(
                            f'Did you mean "{suggested_name}"? (y/n): '
                        )

                        if confirm_match.lower() != "y":
                            print("\nUpdate cancelled.")
                            continue

                        note_name = suggested_name

                        with Spinner("Updating note..."):
                            update_result = generate_note_update(note_name, new_info)

                print_diff(
                    update_result["old_content"],
                    update_result["new_content"]
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
            continue

        elif cmd["type"] == "question":
            answer, sources = ask(cmd["content"])

            print("\nAnswer:")
            print(answer)

            print_sources(sources)

            print("\n---\n")


if __name__ == "__main__":
    main()