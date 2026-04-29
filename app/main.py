from app.ingestion.loader import load_notes

notes = load_notes()

print(f"Found {len(notes)} notes")

for note in notes:
    print(note["path"])