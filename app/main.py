# Entry point for the interactive BJJ LLM Wiki CLI.
# Coordinates command handling and delegates application logic to the corresponding services.

import os

from app.repositories.note_repository import load_notes
from app.vectorstore.chroma_store import add_notes, reset_collection
from app.services.rag_service import ask
from app.cli.handlers.command_handler import handle_command
from app.cli.handlers.write_handler import handle_write
from app.cli.handlers.update_handler import handle_update
from app.config import LANGUAGE, VAULT_PATH


# Rebuilds the vector index from the current Markdown notes in the configured vault.
def reindex_notes():
    notes = load_notes()
    reset_collection()
    add_notes(notes)

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
            handle_write(cmd["content"])
            continue

        elif cmd["type"] == "unknown":
            print("Unknown command.")
            continue

        elif cmd["type"] == "update":
            handle_update(cmd["content"])
            continue

        elif cmd["type"] == "question":
            answer, sources = ask(cmd["content"])

            print("\nAnswer:")
            print(answer)

            print_sources(sources)

            print("\n---\n")


if __name__ == "__main__":
    main()