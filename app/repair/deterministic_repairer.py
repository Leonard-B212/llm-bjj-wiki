# Applies safe deterministic repairs to validated BJJ wiki notes.
# Only performs transformations whose intended result is explicitly known.


def repair_forbidden_wiki_links(content, forbidden_links):
    repaired_content = content
    repairs = []

    for link in forbidden_links:
        old = f"[[{link}]]"
        new = link

        if old in repaired_content:
            repaired_content = repaired_content.replace(old, new)
            repairs.append({
                "type": "forbidden_wiki_link",
                "from": old,
                "to": new,
            })

    return repaired_content, repairs


def repair_perspective_aliases(content, perspective_aliases):
    repaired_content = content
    repairs = []

    for alias, canonical in perspective_aliases.items():
        old = f"[[{alias}]]"
        new = f"[[{canonical}]]"

        if old in repaired_content:
            repaired_content = repaired_content.replace(old, new)
            repairs.append({
                "type": "perspective_alias",
                "from": old,
                "to": new,
            })

    return repaired_content, repairs