import os

from openai import OpenAI

from app.repositories.note_repository import (
    get_existing_note_titles,
    build_note_path as build_repository_note_path,
    write_note,
)
from app.config import OPENAI_API_KEY, TYPE_TO_FOLDER, LANGUAGE, WRITER_MODEL

client = OpenAI(api_key=OPENAI_API_KEY)

SCHEMA_DIR = os.path.join("app", "schemas")


def load_schema(note_type):
    schema_path = os.path.join(SCHEMA_DIR, f"{note_type}_schema.md")

    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema not found: {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as file:
        return file.read()


def classify_note_type(user_input):
    valid_types = list(TYPE_TO_FOLDER.keys())

    prompt = f"""
You classify Brazilian Jiu-Jitsu techniques into exactly one category.

Valid categories:
{', '.join(valid_types)}

Technique description:
{user_input}

Rules:
- Return ONLY the single most fitting category from the list above.
- Return ONLY the category name, nothing else.
- No punctuation, no explanation, no markdown.
- The category must match one of the valid categories exactly (lowercase).
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        temperature=0,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    note_type = response.choices[0].message.content.strip().lower()

    if note_type not in valid_types:
        raise ValueError(f"Model returned invalid note type: '{note_type}'")

    return note_type


def load_global_rules():
    path = os.path.join(SCHEMA_DIR, "global_rules.md")

    with open(path, "r", encoding="utf-8") as file:
        return file.read().replace("{LANGUAGE}", LANGUAGE)


def generate_note_draft(filename, user_input, model=None):
    model = model or WRITER_MODEL
    note_type = classify_note_type(user_input)
    schema = load_schema(note_type)
    global_rules = load_global_rules()
    existing_note_titles = get_existing_note_titles()
    existing_notes_text = "\n".join(
        f"- {title}" for title in existing_note_titles
    )

    prompt = f"""
You create Obsidian markdown notes for a Brazilian Jiu-Jitsu wiki.

Follow the instruction hierarchy below.

PRIORITY 1 — USER INPUT
The user input is the only source of technical BJJ knowledge for this note.
Only information explicitly stated by the user may be used; do not derive content for one section from another (e.g. an Attack detail must not be reversed into a Defense or Problem).

<user_input>
{user_input}
</user_input>

PRIORITY 2 — GLOBAL RULES
These rules define how the note must be written and linked.

<global_rules>
{global_rules}
</global_rules>

PRIORITY 3 — NOTE SCHEMA
The schema defines the required structure and headings.
It does not authorize you to invent missing content.
If a schema section is unsupported by the user input, use `* TBD`.

<schema>
{schema}
</schema>

REFERENCE — EXISTING CANONICAL NOTE TITLES
Use these titles when a matching wiki entity is referenced.

<existing_note_titles>
{existing_notes_text}
</existing_note_titles>

Detected note type:
{note_type}

OUTPUT REQUIREMENTS
- Follow the provided schema exactly.
- Return only the raw markdown content.
- Do not return JSON.
- Do not return a Python dictionary.
- Do not use markdown code fences.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    content = response.choices[0].message.content.strip()

    if not filename.endswith(".md"):
        filename += ".md"

    return {
        "filename": filename,
        "content": content,
        "note_type": note_type,
        "usage": {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    }

def build_note_path(draft):
    return build_repository_note_path(
        draft["note_type"],
        draft["filename"]
    )


def save_note_draft(draft, overwrite=False):
    file_path = build_note_path(draft)

    if os.path.exists(file_path) and not overwrite:
        return {
            "saved": False,
            "reason": "exists",
            "path": file_path
        }

    write_note(file_path, draft["content"])

    return {
        "saved": True,
        "path": file_path
    }