# TODO

## Planned

- [x] RAG retrieval improvements
- [x] Configurable note content language
- [ ] Smart Router: detect whether free-text input should trigger write, update, or question
- [ ] Fuzzy matching for note names (case differences, typos)
- [ ] Duplicate check for `/write`
- [ ] Undo functionality for `/update`
- [ ] Support multiple LLM providers (e.g. OpenAI, Anthropic Claude)
- [ ] Wiki linter: automatically detect schema violations, broken links, duplicates, and orphaned notes
- [ ] Derive a Knowledge Graph from existing Markdown relationships, with the option to later combine graph-based and Chroma-based retrieval
- [ ] Provenance / personal technique status: optionally store where a technique was learned and whether it is learned, tested, or reliable

## Ideas / Needs Evaluation

- [ ] Automatically link existing BJJ terms in descriptive text, potentially serving as the basis for the Knowledge Graph and improving Obsidian visualization
- [ ] Router: ask a clarification question when input is ambiguous or incomplete (single-turn clarification first, no persistent memory)
- [ ] Router: detect and split multiple intents within a single message (more complex, long-term)
- [ ] Build a standalone frontend without requiring Obsidian, providing a simple UI for users without CLI or Obsidian experience
- [ ] Make repository public-ready: remove secrets/personal data, add example configuration, documentation, and setup instructions