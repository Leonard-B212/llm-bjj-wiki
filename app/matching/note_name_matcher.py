# Provides deterministic matching for BJJ note names.
# Supports normalized exact matching and fuzzy suggestions while preserving canonical note titles.

from difflib import get_close_matches


# Normalizes a note name for comparison without changing the canonical title.
def normalize_note_name(name):
    return "".join(
        char
        for char in name.casefold()
        if char.isalnum()
    )


# Returns the canonical title when a normalized exact match exists.
def find_exact_normalized_match(note_name, existing_titles):
    normalized_name = normalize_note_name(note_name)

    for title in existing_titles:
        if normalize_note_name(title) == normalized_name:
            return title

    return None


# Returns similar existing note titles ordered by similarity.
def find_similar_note_names(note_name, existing_titles, limit=3, cutoff=0.7):
    normalized_name = normalize_note_name(note_name)

    normalized_titles = {}

    for title in existing_titles:
        normalized_title = normalize_note_name(title)
        normalized_titles.setdefault(normalized_title, title)

    matches = get_close_matches(
        normalized_name,
        normalized_titles.keys(),
        n=limit,
        cutoff=cutoff,
    )

    return [
        normalized_titles[match]
        for match in matches
    ]