# Expands primary retrieval results with directly linked BJJ wiki notes.
# Keeps structural Wiki-Link retrieval separate from semantic and title-based retrieval.

import re

from app.vectorstore.chroma_store import collection, get_all_notes_meta


WIKI_LINK_PATTERN = re.compile(r"\[\[([^\]|]+)(?:\|[^\]]+)?\]\]")


# Extracts unique Wiki-Link targets from retrieved note content.
def extract_wiki_links(content):
    links = []
    seen = set()

    for match in WIKI_LINK_PATTERN.findall(content):
        target = match.strip()

        if target and target not in seen:
            links.append(target)
            seen.add(target)

    return links


# Loads existing notes linked directly from the primary retrieval results.
def expand_linked_notes(primary_documents, primary_ids, limit=5):
    notes_meta = get_all_notes_meta()
    title_to_id = {
        note["title"].casefold(): note["id"]
        for note in notes_meta
    }

    primary_id_set = set(primary_ids)
    linked_ids = []

    # Preserve primary result order so links from stronger results are considered first.
    for document in primary_documents:
        for linked_title in extract_wiki_links(document):
            linked_id = title_to_id.get(linked_title.casefold())

            if (
                linked_id
                and linked_id not in primary_id_set
                and linked_id not in linked_ids
            ):
                linked_ids.append(linked_id)

                if len(linked_ids) >= limit:
                    break

        if len(linked_ids) >= limit:
            break

    if not linked_ids:
        return {
            "documents": [],
            "ids": [],
        }

    result = collection.get(ids=linked_ids)

    documents_by_id = dict(zip(result["ids"], result["documents"]))

    # Chroma does not guarantee that get() preserves the requested ID order.
    documents = [
        documents_by_id[note_id]
        for note_id in linked_ids
        if note_id in documents_by_id
    ]
    ids = [
        note_id
        for note_id in linked_ids
        if note_id in documents_by_id
    ]

    return {
        "documents": documents,
        "ids": ids,
    }