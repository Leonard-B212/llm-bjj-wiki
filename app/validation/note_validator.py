# Validates generated Markdown notes against deterministic wiki rules.
# Currently checks wiki link targets that must not be used as standalone wiki entities.

import re

from app.validation.lists.forbidden_wiki_links import FORBIDDEN_WIKI_LINKS


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