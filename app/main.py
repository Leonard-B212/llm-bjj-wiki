# Entry point for the interactive BJJ LLM Wiki CLI.
# Coordinates command handling and delegates application logic to the corresponding services.

import os

from app.repositories.note_repository import load_notes
from app.vectorstore.chroma_store import add_notes, reset_collection
from app.cli.handlers.command_handler import handle_command
from app.cli.handlers.write_handler import handle_write
from app.cli.handlers.update_handler import handle_update
from app.cli.handlers.question_handler import handle_question
from app.cli.output.status_printer import format_success
from app.cli.output.check_printer import (
    print_check_summary,
    print_check_details,
)
from app.checks.runners.wiki_check_runner import run_wiki_checks
from app.config import LANGUAGE, VAULT_PATH


# Rebuilds the vector index from the current Markdown notes in the configured vault.
def reindex_notes():
    notes = load_notes()
    reset_collection()
    add_notes(notes)

def run_checks():
    notes = load_notes()
    return run_wiki_checks(notes)

def print_banner():
    print(r"""
    ╔══════════════════════════════════════════════╗
    ║                                              ║
    ║            B J J   L L M   W I K I           ║
    ║                                              ║
    ╠══════════════════════════════════════════════╣
""", end="")

    print(f"    ║  {format_success('Notes indexed')}                          ║")
    print(f"    ║  {format_success('Embeddings loaded')}                      ║")
    print(f"    ║  {format_success('ChromaDB ready')}                         ║")
    print(f"    ║  {format_success('OpenAI configured')}                      ║")

    print(r"""    ╠══════════════════════════════════════════════╣
    ║                                              ║
    ║                 OSS. 🤙                      ║
    ║              Ready to Roll                   ║
    ║                                              ║
    ╚══════════════════════════════════════════════╝
""")


# Initializes the index and runs the interactive command loop.
def main():
    
    reindex_notes()
    print_banner()
    check_results = run_checks()
    print_check_summary(check_results)
    print(f"Vault: {VAULT_PATH}")
    print(f"Content language: {LANGUAGE}\n")
    print("Commands: /exit, /reindex, /check, /write <filename> [description], /update <filename> [new information]\n")

    while True:
        user_input = input(">> ")
        cmd = handle_command(user_input)

        if cmd["type"] == "exit":
            break

        elif cmd["type"] == "reindex":
            reindex_notes()
            continue

        elif cmd["type"] == "check":
            check_results = run_checks()
            print_check_details(check_results)
            print("\n---\n")
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
            handle_question(cmd["content"])
            continue


if __name__ == "__main__":
    main()