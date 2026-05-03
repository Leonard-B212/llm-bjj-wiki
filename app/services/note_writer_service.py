import os
import json
from openai import OpenAI

from app.config import OPENAI_API_KEY, VAULT_PATH, TYPE_TO_FOLDER

client = OpenAI(api_key=OPENAI_API_KEY)

SCHEMA_DIR = os.path.join("app", "schemas")


def load_schema(note_type):
    schema_path = os.path.join(SCHEMA_DIR, f"{note_type}_schema.md")

    if not os.path.exists(schema_path):
        raise FileNotFoundError(f"Schema not found: {schema_path}")

    with open(schema_path, "r", encoding="utf-8") as file:
        return file.read()


def detect_note_type(user_input):
    text = user_input.lower()

    if "escape" in text:
        return "escape"

    if "sweep" in text:
        return "sweep"

    if "pass" in text:
        return "pass"

    if "takedown" in text or "single leg" in text or "double leg" in text:
        return "takedown"

    if "throw" in text or "uki goshi" in text:
        return "throw"

    if "submission" in text or "choke" in text or "armbar" in text or "triangle" in text:
        return "submission"

    if "mount" in text or "guard" in text or "side control" in text or "position" in text:
        return "position"

    return "submission"

def load_global_rules():
    path = os.path.join(SCHEMA_DIR, "global_rules.md")

    with open(path, "r", encoding="utf-8") as file:
        return file.read()

def generate_note_draft(user_input):
    note_type = detect_note_type(user_input)
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

Return a JSON object with exactly these fields:
{{
  "filename": "...",
  "content": "..."
}}

Rules:
- filename must end with .md
- filename should be concise and use hyphens instead of spaces
- content must follow the provided schema
- content must NOT include the title as a heading
- return ONLY raw, valid JSON
- Do not use markdown code fences.
- Do not wrap the JSON in ```json.

Language rules:
- Technique names and links must be in English (e.g. [[Armbar]], [[Triangle]], [[Knee-Elbow Escape]])
- The descriptive text (explanations, bullet points) must be in German
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    raw_output = response.choices[0].message.content
    raw_output = raw_output.strip()

    if raw_output.startswith("```json"):
        raw_output = raw_output.removeprefix("```json").removesuffix("```").strip()
    elif raw_output.startswith("```"):
        raw_output = raw_output.removeprefix("```").removesuffix("```").strip()

    data = json.loads(raw_output)
    data["note_type"] = note_type
    return data

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