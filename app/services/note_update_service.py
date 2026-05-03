import os

from openai import OpenAI

from app.config import OPENAI_API_KEY, VAULT_PATH, TYPE_TO_FOLDER
from app.services.note_writer_service import load_global_rules

client = OpenAI(api_key=OPENAI_API_KEY)


def find_note_path(note_name):
    filename = f"{note_name}.md"

    for folder in TYPE_TO_FOLDER.values():
        path = os.path.join(VAULT_PATH, folder, filename)

        if os.path.exists(path):
            return path

    raise FileNotFoundError(f"Note not found: {filename}")


def generate_note_update(note_name, user_input):
    file_path = find_note_path(note_name)

    with open(file_path, "r", encoding="utf-8") as file:
        existing_content = file.read()

    global_rules = load_global_rules()

    prompt = f"""
You update an existing Obsidian markdown note for a Brazilian Jiu-Jitsu wiki.

Global rules:
{global_rules}

Existing note:
{existing_content}

New information:
{user_input}

Rules:
- Integrate the new information into the existing note.
- Keep the existing structure.
- Do NOT duplicate sections.
- Do NOT remove useful existing content.
- Return ONLY the updated markdown content.
- Do NOT return JSON.
- Do NOT return a Python dictionary.
- Do NOT use markdown code fences.
- Do NOT duplicate sections.
- Do NOT remove useful existing content.
- Keep the same headings and style as the existing note.
- Place new information in the most semantically fitting existing section.
- You may rephrase and improve the wording of the new information for clarity and correctness.
- Preserve the meaning, but do not keep the original wording if it is unclear or messy.
- Each bullet point should contain a complete and meaningful step, not just a single keyword.
"""

    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    updated_content = response.choices[0].message.content.strip()

    return {
        "path": file_path,
        "old_content": existing_content,
        "new_content": updated_content
    }


def save_note_update(update_result):
    with open(update_result["path"], "w", encoding="utf-8") as file:
        file.write(update_result["new_content"])

    return update_result["path"]