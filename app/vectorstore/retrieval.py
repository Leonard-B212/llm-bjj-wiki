# Combines semantic ChromaDB retrieval with normalized title matching.
# Ensures directly referenced notes are included even when their semantic similarity is weak.

from app.vectorstore.chroma_store import query_notes, get_all_notes_meta, collection


def normalize(text):
    return text.lower().replace("-", " ").strip()


def normalize_compact(text):
    return normalize(text).replace(" ", "")


# Finds notes whose normalized titles are directly referenced in the question.
def find_title_matches(question, notes_meta):
    question_norm = normalize(question)
    question_compact = normalize_compact(question)

    matched_ids = []

    for note in notes_meta:
        title_norm = normalize(note["title"])
        title_compact = normalize_compact(note["title"])

        if title_norm in question_norm or title_compact in question_compact:
            matched_ids.append(note["id"])

    return matched_ids


# Fetches exact notes by ID and assigns them the strongest retrieval distance.
def fetch_by_ids(ids):
    if not ids:
        return {"documents": [], "ids": [], "distances": []}

    result = collection.get(ids=ids)

    documents = result["documents"]
    fetched_ids = result["ids"]
    distances = [0.0] * len(fetched_ids)

    return {"documents": documents, "ids": fetched_ids, "distances": distances}


# Merges semantic results with direct title matches and removes duplicate notes.
def hybrid_query(question, n_results=5):
    semantic_results = query_notes(question, n_results=n_results)

    notes_meta = get_all_notes_meta()
    title_match_ids = find_title_matches(question, notes_meta)
    title_results = fetch_by_ids(title_match_ids)

    documents = list(semantic_results["documents"][0]) if semantic_results["documents"] else []
    ids = list(semantic_results["ids"][0]) if semantic_results["ids"] else []
    distances = list(semantic_results["distances"][0]) if semantic_results["distances"] else []

    for doc, id_, dist in zip(title_results["documents"], title_results["ids"], title_results["distances"]):
        if id_ not in ids:
            documents.append(doc)
            ids.append(id_)
            distances.append(dist)

    combined = sorted(zip(distances, ids, documents), key=lambda x: x[0])
    distances, ids, documents = zip(*combined) if combined else ([], [], [])

    return {
        "documents": [list(documents)],
        "ids": [list(ids)],
        "distances": [list(distances)]
    }