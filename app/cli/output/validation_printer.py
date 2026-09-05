# Formats and prints deterministic validation warnings for generated and updated notes.


def print_validation_result(validation_result):
    forbidden_links = validation_result["forbidden_wiki_links"]
    perspective_aliases = validation_result["perspective_aliases"]

    if not forbidden_links and not perspective_aliases:
        return

    print("\nValidation warnings:")

    for link in forbidden_links:
        print(f"- Generic BJJ concept should not be a Wiki-Link: [[{link}]]")

    for alias, canonical in perspective_aliases.items():
        print(f"- Perspective-specific Wiki-Link: [[{alias}]] → [[{canonical}]]")