import os

from openai import OpenAI

from app.config import OPENAI_API_KEY, VAULT_PATH, TYPE_TO_FOLDER, LANGUAGE

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


def generate_note_draft(filename, user_input):
    note_type = classify_note_type(user_input)
    schema = load_schema(note_type)
    global_rules = load_global_rules()

    prompt = f"""
You create Obsidian markdown notes for a Brazilian Jiu-Jitsu wiki.

Global rules:
{global_rules}

User input:
{user_input}

Detected note type:
{note_type}

Use this schema:
{schema}

Rules:
- content must follow the provided schema
- Return ONLY the raw markdown content.
- Do NOT return JSON.
- Do NOT return a Python dictionary.
- Do NOT use markdown code fences.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
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
        "note_type": note_type
    }


def build_note_path(draft):
    note_type = draft["note_type"]
    filename = draft["filename"]

    folder = TYPE_TO_FOLDER.get(note_type)

    if not folder:
        raise ValueError(f"No folder mapping for type: {note_type}")

    folder_path = os.path.join(VAULT_PATH, folder)
    os.makedirs(folder_path, exist_ok=True)

    return os.path.join(folder_path, filename)


def save_note_draft(draft, overwrite=False):
    file_path = build_note_path(draft)

    if os.path.exists(file_path) and not overwrite:
        return {
            "saved": False,
            "reason": "exists",
            "path": file_path
        }

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(draft["content"])

    return {
        "saved": True,
        "path": file_path
    }