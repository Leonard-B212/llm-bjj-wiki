from app.ingestion.loader import load_notes
from app.vectorstore.chroma_store import add_notes, query_notes, reset_collection
from app.config import OPENAI_API_KEY

notes = load_notes()
reset_collection()
add_notes(notes)

print("✅ Notes in Chroma gespeichert")
print("API Key loaded:", OPENAI_API_KEY is not None)

# Test Query
results = query_notes("how does a knee elbow escape work?", max_distance=1.3)

docs = results["documents"][0]
ids = results["ids"][0]
distances = results["distances"][0]

for i in range(len(docs)):
    print(f"\n--- Treffer {i+1} ---")
    print(f"ID: {ids[i]}")
    print(f"Distance: {distances[i]}")
    print(docs[i][:200])
    