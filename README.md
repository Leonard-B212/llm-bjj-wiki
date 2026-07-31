# BJJ LLM Wiki

A terminal-based tool to build and query a personal Brazilian Jiu-Jitsu knowledge base, stored as Markdown notes in an Obsidian vault, using an LLM for retrieval, writing, and updating.

## Goal

* Use Markdown notes (Obsidian) as a structured knowledge base
* Let an LLM write and update notes for you in a consistent format
* Ask questions via terminal and get answers grounded in your own notes

---

## Concept

The system combines note generation with a Retrieval-Augmented Generation (RAG) approach:

---

### Components

* **Markdown Notes** (Obsidian Vault) — the knowledge base itself
* **ChromaDB** — vector database for semantic search
* **OpenAI API (gpt-4.1-mini)** — note generation, note classification, and question answering
* **Hybrid Retrieval** — combines semantic search with exact/normalized title matching, so short or sparsely-written notes are still found reliably even if their embedding is weak

---

## Project Structure

```text
LLM-BJJ-Wiki/
│
├── app/
│   ├── main.py
│   ├── config.py
│   │
│   ├── cli/
│   │   ├── command_handler.py
│   │   └── diff_printer.py
│   │
│   ├── ingestion/
│   │   └── loader.py
│   │
│   ├── schemas/
│   │   ├── escape_schema.md
│   │   ├── global_rules.md
│   │   ├── pass_schema.md
│   │   ├── position_schema.md
│   │   ├── submission_schema.md
│   │   ├── sweep_schema.md
│   │   ├── takedown_schema.md
│   │   └── throw_schema.md
│   │
│   ├── services/
│   │   ├── note_update_service.py
│   │   ├── note_writer_service.py
│   │   └── rag_service.py
│   │
│   └── vectorstore/
│       ├── chroma_store.py
│       └── retrieval.py
│
├── .env
├── .gitignore
├── requirements.txt
├── todo.md
└── README.md
```

---

## Setup

### 1. Clone the repository

```bash
git clone https://github.com/Leonard-B212/llm-bjj-wiki.git
cd llm-bjj-wiki
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

or manually:

```bash
pip install chromadb openai python-dotenv
```

### 3. Set your API key

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_api_key
```

Important: `.env` is listed in `.gitignore` so your key is never committed to the repo.

### 4. Configure your vault path

Set your Obsidian vault path in `app/config.py`:

```python
VAULT_PATH = r"C:\Users\leona\Documents\Obsidian\BJJ"
```

Note folders are mapped by technique type in `TYPE_TO_FOLDER` in the same file. Add a new type there if you want a new category (and a matching `*_schema.md` in `app/schemas/`).

---

## Run the project

```bash
python -m app.main
```

On startup, all notes in the vault are indexed into ChromaDB.

### Commands

| Command | Description |
|---|---|
| `<free text>` | Ask a question about your notes (RAG) |
| `/write <filename> <description>` | Create a new note. You provide the filename, the LLM classifies the technique type, fills in the schema, and drafts the content |
| `/update <filename> <new information>` | Merge new information into an existing note, keeping its structure |
| `/reindex` | Rebuild the vector index (e.g. after manual edits in Obsidian) |
| `/exit` | Quit |

Example:

```text
>> /write Rear-Naked-Choke Klassischer Choke von der Rückenkontrolle aus, Arm um den Hals, Griff einhaken, Ellenbogen zusammenziehen.
```

The generated note is shown as a preview before saving, and you're asked to confirm.

---

## How note generation works

Each technique type (`submission`, `escape`, `sweep`, `pass`, `position`, `takedown`, `throw`) has a corresponding schema file in `app/schemas/` that defines the expected structure (headings, sections, level of detail). When you run `/write`:

1. The LLM classifies the technique into one of the defined types
2. The matching schema is loaded
3. The LLM drafts the note content in German, following the schema structure, with technique names and links in English (`[[Armbar]]`, `[[Side-Control]]`)
4. The filename you provided is used as-is (normalized to end in `.md`)

`/update` follows the same principle but works against an existing note: it loads the current content, merges the new information into the correct section, and preserves structure and existing content.

---

## How retrieval works

Questions are answered using hybrid retrieval:

1. **Semantic search** via ChromaDB embeddings — finds notes that are thematically related to the question
2. **Lexical title matching** — if a note's title (normalized, hyphen- and case-insensitive) appears in the question, it is included regardless of its embedding score

This avoids a common RAG failure mode: short or sparsely-filled notes (e.g. a note that's mostly headings with little content) can have weak embeddings and get outranked by longer, unrelated notes that happen to mention the same term in passing.

---

## Current Status

* Terminal-based interaction
* Note creation and updates follow enforced per-type schemas
* Hybrid retrieval (semantic + lexical) for question answering

See `todo.md` for planned features and open ideas.

---

## Notes

* Do not store sensitive data in your notes
* OpenAI API usage may incur costs
* This is currently a learning/personal project, not intended for production use