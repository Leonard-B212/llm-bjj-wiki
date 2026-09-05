# Validates generated Markdown notes against deterministic wiki rules.
# Currently checks wiki link targets that must not be used as standalone wiki entities.

import re

from app.validation.lists.forbidden_wiki_links import FORBIDDEN_WIKI_LINKS
from app.validation.lists.perspective_aliases import PERSPECTIVE_ALIASES

# Runs all deterministic validation checks for a generated note.
def validate_note(content):
    return {
        "forbidden_wiki_links": find_forbidden_wiki_links(content),
        "perspective_aliases": find_perspective_aliases(content),
    }

# Extracts all wiki link targets from Markdown content.
def extract_wiki_links(content):
    return re.findall(r"\[\[([^\]]+)\]\]", content)


# Returns forbidden wiki links found in the provided note content.
def find_forbidden_wiki_links(content):
    wiki_links = extract_wiki_links(content)

    return list(dict.fromkeys(
        link
        for link in wiki_links
        if link in FORBIDDEN_WIKI_LINKS
    ))

# Returns perspective-specific links together with their canonical wiki targets.
def find_perspective_aliases(content):
    wiki_links = extract_wiki_links(content)

    return {
        link: PERSPECTIVE_ALIASES[link]
        for link in wiki_links
        if link in PERSPECTIVE_ALIASES
    }