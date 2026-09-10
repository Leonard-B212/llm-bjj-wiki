# Handles question answering over the BJJ wiki using hybrid retrieval and grounded LLM responses.
# Retrieved notes are filtered before being assembled into the context passed to the LLM.

from app.config import CLASSIFIER_MODEL
from app.llm.client import create_chat_completion
from app.vectorstore.retrieval import hybrid_query
from app.vectorstore.link_expansion import expand_linked_notes


def ask(question, status_callback=None):
    if status_callback:
        status_callback("Finding relevant notes...")

    results = hybrid_query(question)

    # Return early when retrieval found no relevant notes.
    if not results["documents"] or not results["documents"][0]:
        return "No relevant notes found.", []

    documents = results["documents"][0]
    ids = results["ids"][0]

    if status_callback:
        status_callback("Following wiki links...")

    linked_results = expand_linked_notes(
        primary_documents=documents,
        primary_ids=ids,
        limit=5,
    )

    documents.extend(linked_results["documents"])
    ids.extend(linked_results["ids"])

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

    if status_callback:
        status_callback("Writing answer...")

    response = create_chat_completion(
        model=CLASSIFIER_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    return answer, ids