# Coordinates validation and repair for generated or updated BJJ wiki notes.
# Keeps the validate-repair-revalidate workflow reusable across CLI use cases.

from app.repair.note_repairer import repair_note
from app.validation.note_validator import validate_note


def process_note(content):
    validation_result = validate_note(content)

    if (
        not validation_result["forbidden_wiki_links"]
        and not validation_result["perspective_aliases"]
    ):
        return {
            "content": content,
            "repairs_applied": [],
            "validation_result": validation_result,
        }

    return repair_note(content, validation_result)