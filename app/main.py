import os

from app.ingestion.loader import load_notes
from app.vectorstore.chroma_store import add_notes, reset_collection
from app.services.rag_service import ask
from app.cli.command_handler import handle_command
from app.services.note_writer_service import generate_note_draft, save_note_draft, load_global_rules
from app.config import TYPE_TO_FOLDER


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
    print("Commands: /exit, /reindex, /write <text>\n")

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
                path = save_note_draft(draft)
                print(f"\nSaved to: {path}")
            else:
                print("\nNot saved.")

            print("\n---\n")
            continue

        elif cmd["type"] == "unknown":
            print("Unknown command.")
            continue

        elif cmd["type"] == "question":
            answer, sources = ask(cmd["content"])

            print("\nAnswer:")
            print(answer)

            print_sources(sources)

            print("\n---\n")


if __name__ == "__main__":
    main()