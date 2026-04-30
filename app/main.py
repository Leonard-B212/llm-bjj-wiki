import os

from app.ingestion.loader import load_notes
from app.vectorstore.chroma_store import add_notes, reset_collection
from app.services.rag_service import ask
from app.cli.command_handler import handle_command


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
            print("Write feature coming soon:")
            print(cmd["content"])
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