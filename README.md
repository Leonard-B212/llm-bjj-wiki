# BJJ LLM Wiki

A terminal-based tool to build and query a personal Brazilian Jiu-Jitsu knowledge base, stored as Markdown notes in an Obsidian vault, using an LLM for retrieval, writing, and updating.

## Goal

* Use Markdown notes (Obsidian) as a structured knowledge base
* Let an LLM write and update notes for you in a consistent format
* Ask questions via terminal and get answers grounded in your own notes

---

## Concept

The system combines note generation with a Retrieval-Augmented Generation (RAG) approach.

### Components

* **Markdown Notes** (Obsidian Vault) — the knowledge base itself
* **ChromaDB** — vector database for semantic search
* **OpenAI API (gpt-4.1-mini)** — note generation, note classification, and question answering
* **Hybrid Retrieval** — combines semantic search with exact/normalized title matching, so short or sparsely-written notes are still found reliably even if their embedding is weak

### Obsidian as the Frontend

This project is designed to work together with [Obsidian](https://obsidian.md/), which acts as the visual frontend for the knowledge base.

The BJJ LLM Wiki manages and interacts with the Markdown data by creating and updating notes, searching the knowledge base, and answering questions through RAG.

Obsidian provides the visual layer for browsing and manually editing notes, following `[[Wiki-Links]]`, and exploring relationships between techniques using features such as the Graph View.

Obsidian must be installed separately and is not included with this project.

The Markdown files remain the source of truth, so the vault can still be viewed and edited directly in Obsidian without running the LLM application.

---

## Project Structure

```text
LLM-BJJ-Wiki/
│
├── app/                         # Core application
│   ├── main.py
│   ├── config.py
│   │
│   ├── cli/                     # Terminal commands and output handling
│   │   ├── command_handler.py
│   │   └── diff_printer.py
│   │
│   ├── ingestion/               # Loads Markdown notes from the vault
│   │   └── loader.py
│   │
│   ├── schemas/                 # Defines the structure of each BJJ note type
│   │   ├── escape_schema.md
│   │   ├── global_rules.md
│   │   ├── pass_schema.md
│   │   ├── position_schema.md
│   │   ├── submission_schema.md
│   │   ├── sweep_schema.md
│   │   ├── takedown_schema.md
│   │   └── throw_schema.md
│   │
│   ├── services/                # LLM, note writing/update and RAG logic
│   │   ├── note_update_service.py
│   │   ├── note_writer_service.py
│   │   └── rag_service.py
│   │
│   └── vectorstore/             # ChromaDB storage and retrieval
│       ├── chroma_store.py
│       └── retrieval.py
│
├── .env.example
├── .gitignore
├── LICENSE
├── requirements.txt
├── start.py
├── todo.md
└── README.md
```

---

## Setup

### Requirements

Before starting, you need:

* **Python 3** installed
* An **OpenAI API key**
* **Obsidian** installed separately
* An **Obsidian vault** where the Markdown notes should be stored

The launcher handles the remaining setup and can install the required Python packages for you.

### 1. Clone the repository

```bash
git clone https://github.com/Leonard-B212/llm-bjj-wiki.git
cd llm-bjj-wiki
```

### 2. Start the launcher

```bash
python start.py
```

On the first start, the launcher detects that no `.env` configuration exists and starts the setup automatically.

You will be asked for:

```text
First-time setup
----------------
OpenAI API key:
Obsidian vault path:
Content language [English]:
```

#### OpenAI API key

Enter your OpenAI API key directly:

```text
OpenAI API key: sk-your-api-key-here
```

The key is stored locally in `.env` and is not committed to the repository.

#### Obsidian vault path

Enter the full path to your BJJ Obsidian vault.

For example, on Windows:

```text
Obsidian vault path: C:\Users\YourName\Documents\Obsidian\BJJ
```

* Enter the path directly. Do **not** add quotation marks or additional spaces.
* Spaces that are actually part of a folder name are fine.
* The launcher checks whether the configured vault path exists before starting the Wiki.

#### Content language

Enter the language in which descriptive note content should be generated:

```text
Content language [English]: German
```

If you simply press Enter, `English` is used as the default.

`LANGUAGE` only controls descriptive note content. Schema headings, BJJ technique names, filenames, and links remain in English.

### 3. Install dependencies

After the initial setup, the launcher checks whether required Python packages are installed.

If packages are missing, you will see something like:

```text
Missing dependencies:
- chromadb
- openai
- python-dotenv

Install them now? (y/n):
```

Enter:

```text
y
```

The launcher installs the dependencies from `requirements.txt` using the same Python installation that started the launcher.

You can also reinstall or repair the dependencies later through the launcher menu.

### 4. Start the Wiki

After setup, the launcher displays:

```text
🥋 BJJ LLM Wiki
----------------
1. Start BJJ-LLM-Wiki
2. Settings
3. Install / Repair Dependencies
4. Exit
```

Select:

```text
1
```

The Wiki will start and index the notes in your configured vault into ChromaDB.

When you exit the Wiki with `/exit`, you return to the launcher. This allows you to change settings, repair dependencies, or start the Wiki again without restarting the launcher.

---

## Configuration

The launcher stores its configuration locally in a `.env` file.

A configuration looks like this:

```text
OPENAI_API_KEY=your_api_key_here
VAULT_PATH=C:\Users\YourName\Documents\Obsidian\BJJ
LANGUAGE=English
```

Normally, you do not need to edit this file manually. Use the **Settings** option in `start.py` instead.

The settings menu allows you to change:

```text
1. Change vault path
2. Change content language
3. Change OpenAI API key
4. Back
```

The API key itself is never displayed by the launcher. It only shows whether an API key is configured.

`.env` is listed in `.gitignore`, so your local configuration and API key are not committed to the repository.

`.env.example` is included as a template for manual configuration.

Note folders are mapped by technique type in `TYPE_TO_FOLDER` in `app/config.py`. Add a new type there if you want a new category (and a matching `*_schema.md` in `app/schemas/`).

---

## Run the project

For normal use, start the launcher from the project directory:

```bash
python start.py
```

The application can also be started directly:

```bash
python -m app.main
```

Direct startup bypasses the launcher's setup, configuration validation, and dependency checks and is therefore mainly useful during development.

---

## Commands

| Command | Description |
|---|---|
| `<free text>` | Ask a question about your notes (RAG) |
| `/write <filename> <description>` | Create a new note. You provide the filename, the LLM classifies the technique type, fills in the schema, and drafts the content |
| `/update <filename> <new information>` | Merge new information into an existing note, keeping its structure |
| `/reindex` | Rebuild the vector index (e.g. after manual edits in Obsidian) |
| `/exit` | Exit the Wiki and return to the launcher |

Example:

```text
>> /write Rear-Naked-Choke Classic choke from back control. Wrap the arm around the neck, secure the grip and bring the elbows together.
```

The generated note is shown as a preview before saving, and you're asked to confirm.

---

## How note generation works

Each technique type (`submission`, `escape`, `sweep`, `pass`, `position`, `takedown`, `throw`) has a corresponding schema file in `app/schemas/` that defines the expected structure (headings, sections, level of detail).

When you run `/write`:

1. The LLM classifies the technique into one of the defined types
2. The matching schema is loaded
3. The LLM drafts the descriptive note content in the language configured through `LANGUAGE`, while schema headings, technique names, filenames, and links remain in English (`[[Armbar]]`, `[[Side-Control]]`)
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
* Guided first-time setup through `start.py`
* Configuration management through the launcher
* Automatic dependency checking and installation
* Note creation and updates follow enforced per-type schemas
* Configurable descriptive note language
* Hybrid retrieval (semantic + lexical) for question answering

See `todo.md` for planned features and open ideas.

---

## Notes

* Do not store sensitive data in your notes
* OpenAI API usage may incur costs
* Your OpenAI API key is stored locally in `.env`
* Your Markdown notes remain in your configured vault and are not part of this repository
* This is currently a learning/personal project, not intended for production use

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.