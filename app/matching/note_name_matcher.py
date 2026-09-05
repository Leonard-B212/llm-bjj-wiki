# Provides deterministic fuzzy matching for BJJ note names.
# Suggests existing canonical note titles without modifying or resolving notes automatically.

from difflib import get_close_matches


# Returns similar existing note titles ordered by similarity.
def find_similar_note_names(note_name, existing_titles, limit=3, cutoff=0.6):
    return get_close_matches(
        note_name,
        existing_titles,
        n=limit,
        cutoff=cutoff,
    )