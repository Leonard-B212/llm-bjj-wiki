import os

from app.ingestion.loader import load_notes
from app.vectorstore.chroma_store import add_notes, reset_collection
from app.services.rag_service import ask
from app.cli.command_handler import handle_command
from app.services.note_writer_service import generate_note_draft, save_note_draft, load_global_rules
from app.config import TYPE_TO_FOLDER
from app.services.note_update_service import generate_note_update, save_note_update
from app.cli.diff_printer import print_diff


def reindex_notes():
    notes = load_notes()
    reset_collection()
    add_notes(notes)
    print("✅ Notes indexed")


def print_sources(sources):
    print("\nSources:")
    for source in sources:
        print(f"- {os.path.basename(source)}")


def main():
    reindex_notes()

    print("Type '/exit' to quit.")
    print("Commands: /exit, /reindex, /write <text>, /update <filename> <new information>\n")

    while True:
        user_input = input(">> ")
        cmd = handle_command(user_input)

        if cmd["type"] == "exit":
            break

        elif cmd["type"] == "reindex":
            reindex_notes()
            continue

        elif cmd["type"] == "write":
            draft = generate_note_draft(cmd["content"])

            print("\nFilename:")
            print(draft["filename"])

            print("\nContent:")
            print(draft["content"])

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

                update_result = generate_note_update(note_name, new_info)

                print_diff(
                    update_result["old_content"],
                    update_result["new_content"]
                )

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