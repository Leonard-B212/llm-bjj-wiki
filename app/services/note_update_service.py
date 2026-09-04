# Handles the note update workflow by combining existing note content with new user input.
# Applies the current schema, global writing rules, canonical note titles, and configured LLM model.

from app.config import WRITER_MODEL
from app.llm.client import create_chat_completion
from app.repositories.note_repository import (
    find_note,
    read_note,
    write_note,
    get_existing_note_titles,
)
from app.schemas.schema_loader import load_schema, load_global_rules


# Generates a complete updated note while preserving supported existing technical content.
def generate_note_update(note_name, user_input):
    note = find_note(note_name)

    file_path = note["path"]
    note_type = note["note_type"]

    existing_content = read_note(file_path)

    schema = load_schema(note_type)
    global_rules = load_global_rules()
    existing_note_titles = get_existing_note_titles()
    existing_notes_text = "\n".join(
        f"- {title}" for title in existing_note_titles
    )

    prompt = f"""
You update an existing Obsidian markdown note for a Brazilian Jiu-Jitsu wiki.

Follow the instruction hierarchy below.

PRIORITY 1 — EXISTING NOTE AND NEW INFORMATION
The existing note contains previously stored technical BJJ knowledge.
The new information contains additional technical BJJ knowledge provided by the user.

Preserve useful existing information and integrate the new information into the most semantically appropriate sections.
Only information supported by the existing note or the new information may be used.
Do not derive content for one section from another (e.g. an Attack detail must not be reversed into a Defense or Problem).

<existing_note>
{existing_content}
</existing_note>

<new_information>
{user_input}
</new_information>

PRIORITY 2 — GLOBAL RULES
These rules define how the note must be written and linked.

<global_rules>
{global_rules}
</global_rules>

PRIORITY 3 — NOTE SCHEMA
The updated note must follow this schema.
Preserve existing supported information while ensuring the final note follows the required structure.
You may rephrase existing information for clarity, but do not reinterpret, generalize, narrow, or change its technical meaning.
If a schema section is unsupported by both the existing note and the new information, use `* TBD`.

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
- Integrate the new information into the existing note.
- Preserve useful existing technical information.
- Do not duplicate information or sections.
- Follow the provided schema exactly.
- Keep the same general writing style where possible.
- Return only the complete updated raw markdown content.
- Do not return JSON.
- Do not return a Python dictionary.
- Do not use markdown code fences.
"""

    response = create_chat_completion(
        model=WRITER_MODEL,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    updated_content = response.choices[0].message.content.strip()

    return {
        "path": file_path,
        "old_content": existing_content,
        "new_content": updated_content,
        "note_type": note_type,
        "usage": {
            "input_tokens": response.usage.prompt_tokens,
            "output_tokens": response.usage.completion_tokens,
            "total_tokens": response.usage.total_tokens,
        }
    }


def save_note_update(update_result):
    return write_note(
        update_result["path"],
        update_result["new_content"]
    )