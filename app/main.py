from app.ingestion.loader import load_notes
from app.vectorstore.chroma_store import add_notes, query_notes, reset_collection
from app.config import OPENAI_API_KEY
from app.services.rag_service import ask, client
import os

def main():
    notes = load_notes()

    reset_collection()
    add_notes(notes)

    print("✅ Notes indexed")
    print("Type 'exit' to quit.\n")

    while True:
        question = input("Question: ")

        if question.lower() in ["exit", "quit"]:
            break

        answer, sources = ask(question)

        print("\nAnswer:")
        print(answer)

        print("\nSources:")
        for source in sources:
            print(f"- {os.path.basename(source)}")

        print("\n---\n")

if __name__ == "__main__":
    main()
    