# Coordinates note repairs based on deterministic validation results.
# Provides a central repair entry point that can later delegate unresolved issues to LLM-based repair.

from app.repair.deterministic_repairer import (
    repair_forbidden_wiki_links,
    repair_perspective_aliases,
)
from app.validation.note_validator import validate_note


def repair_note(content, validation_result):
    repaired_content = content
    repairs_applied = []

    repaired_content, repairs = repair_forbidden_wiki_links(
        repaired_content,
        validation_result["forbidden_wiki_links"],
    )
    repairs_applied.extend(repairs)

    repaired_content, repairs = repair_perspective_aliases(
        repaired_content,
        validation_result["perspective_aliases"],
    )
    repairs_applied.extend(repairs)

    final_validation_result = validate_note(repaired_content)

    return {
        "content": repaired_content,
        "repairs_applied": repairs_applied,
        "validation_result": final_validation_result,
    }