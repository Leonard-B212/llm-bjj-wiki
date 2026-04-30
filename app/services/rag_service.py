from openai import OpenAI
from app.config import OPENAI_API_KEY
from app.vectorstore.chroma_store import query_notes

client = OpenAI(api_key=OPENAI_API_KEY)

def ask(question):
    results = query_notes(question)
    
    documents_raw = results["documents"][0]
    ids_raw = results["ids"][0]
    distances = results["distances"][0]

    documents = []
    ids = []

    # beste Distanz als Referenz
    best_distance = distances[0]

    for doc, id_, dist in zip(documents_raw, ids_raw, distances):
        # nur behalten, wenn nicht deutlich schlechter als der beste Treffer
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

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    answer = response.choices[0].message.content

    return answer, ids