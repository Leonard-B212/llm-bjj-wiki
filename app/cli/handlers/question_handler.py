# Handles the interactive CLI workflow for answering BJJ wiki questions.
# Coordinates RAG execution, loading feedback, answer output, and source display.

import os
import time

from app.cli.spinner import Spinner
from app.cli.output.status_printer import print_success
from app.services.rag_service import ask


def print_sources(sources):
    print("\nSources:")
    for source in sources:
        print(f"- {os.path.basename(source)}")


def handle_question(content):
    with Spinner("Finding relevant notes...") as spinner:
        current_status = "Finding relevant notes..."
        status_started_at = time.monotonic()

        def update_status(new_status):
            nonlocal current_status, status_started_at

            if new_status == current_status:
                return

            elapsed = time.monotonic() - status_started_at

            if elapsed < 0.5:
                time.sleep(0.5 - elapsed)

            spinner.stop()
            print_success(current_status.removesuffix("..."))
            spinner.message = new_status
            spinner.start()

            current_status = new_status
            status_started_at = time.monotonic()

        answer, sources = ask(
            content,
            status_callback=update_status,
        )

        elapsed = time.monotonic() - status_started_at

        if elapsed < 0.5:
            time.sleep(0.5 - elapsed)

    print_success(current_status.removesuffix("..."))

    print("\nAnswer:")
    print(answer)

    print_sources(sources)

    print("\n---\n")