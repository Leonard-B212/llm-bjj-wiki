# Handles question answering over the BJJ wiki using hybrid retrieval and grounded LLM responses.
# Retrieved notes are filtered before being assembled into the context passed to the LLM.

from app.config import CLASSIFIER_MODEL
from app.llm.client import create_chat_completion
from app.vectorstore.retrieval import hybrid_query


def ask(question):
    results = hybrid_query(question)

    documents_raw = results["documents"][0]
    ids_raw = results["ids"][0]
    distances = results["distances"][0]

    # Return early when retrieval found no relevant notes.
    if not results["documents"] or not results["documents"][0]:
        return "No relevant notes found.", []

    documents = []
    ids = []

    # Use the best semantic distance as the reference for filtering weaker matches.
    best_distance = distances[0]

    for doc, id_, dist in zip(documents_raw, ids_raw, distances):
        # Keep only results that are not significantly worse than the best match.
        if dist <= best_distance + 0.2:
            documents.append(doc)
            ids.append(id_)

    context_parts = []

    for doc, source_id in zip(documents, ids):
        context_parts.append(f"Source: {source_id}\n\n{doc}")

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""
You are a helpful BJJ coach.

Answer the question based only on the following notes.
If the notes do not contain enough information, say that clearly.

Notes:
{context}

Question:
{question}
"""

    response = create_chat_completion(
        model=CLASSIFIER_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    return answer, ids