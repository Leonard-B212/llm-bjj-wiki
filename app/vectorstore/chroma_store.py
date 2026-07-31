import os
import chromadb

client = chromadb.Client()
collection = client.get_or_create_collection("bjj")

def add_notes(notes):
    documents = []
    ids = []

    for note in notes:
        documents.append(f"{note['title']}\n\n{note['content']}")
        ids.append(note["id"])

    collection.add(
        documents=documents,
        ids=ids
    )

def query_notes(query, n_results=5, max_distance=None):
    results = collection.query(
        query_texts=[query],
        n_results=n_results
    )

    if max_distance is None:
        return results

    filtered_documents = []
    filtered_ids = []
    filtered_distances = []

    for doc, id_, distance in zip(
        results["documents"][0],
        results["ids"][0],
        results["distances"][0]
    ):
        if distance <= max_distance:
            filtered_documents.append(doc)
            filtered_ids.append(id_)
            filtered_distances.append(distance)

    return {
        "documents": [filtered_documents],
        "ids": [filtered_ids],
        "distances": [filtered_distances]
    }

def reset_collection():
    existing = collection.get()

    if existing["ids"]:
        collection.delete(ids=existing["ids"])


def get_all_notes_meta():
    
    existing = collection.get()

    notes_meta = []

    for note_id in existing["ids"]:
        title = os.path.basename(note_id).replace(".md", "")
        notes_meta.append({"id": note_id, "title": title})

    return notes_meta