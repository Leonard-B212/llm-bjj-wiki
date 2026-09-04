# BJJ LLM Wiki

A terminal-based tool for building and querying a personal Brazilian Jiu-Jitsu knowledge base using structured Markdown notes, Obsidian, LLM-assisted writing, and Retrieval-Augmented Generation (RAG).

![BJJ LLM Wiki CLI](assets/bjj-llm-wiki-cli.png)

## Goal

BJJ LLM Wiki is designed to turn personal BJJ knowledge into a structured and searchable wiki without replacing that knowledge with generic LLM-generated technique instructions.

- Markdown notes remain the source of truth
- Obsidian provides a visual frontend for browsing and editing the wiki
- LLMs structure personal BJJ knowledge using consistent schemas
- `[[Wiki-Links]]` connect related positions and techniques
- RAG allows questions to be answered from the existing knowledge base
- The vault remains portable and independent of the application

---

## Features

- Terminal-based interaction
- Guided first-time setup
- Structured note generation for seven BJJ entity types
- Schema-based note updates and legacy note migration
- Global terminology and Wiki-Linking rules
- Canonical entity awareness using existing note titles
- Configurable descriptive content language
- Configurable writer and classifier models
- Hybrid RAG retrieval using semantic and title matching
- Markdown/Obsidian as a portable source of truth
- Preview and confirmation before notes are saved
- Writer benchmark suite with deterministic regression checks
- Provider-neutral LLM application layer

---

## Quick Start

### Requirements

You need:

- **Python 3**
- an **OpenAI API key**
- **Obsidian**
- an Obsidian vault for your BJJ notes

An empty `example-vault/` with the expected folder structure is included in the repository and can be used to quickly get started.

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

You can point the vault path either to your own Obsidian vault or to the included `example-vault/`.

The API key is stored locally in `.env` and is not committed to the repository.

`LANGUAGE` controls the descriptive content of generated notes. Schema headings, BJJ terminology, filenames, and Wiki-Link targets remain in English.

### 3. Dependencies

The launcher checks whether the required Python packages are installed and can install missing dependencies from `requirements.txt`.

Dependencies can also be repaired or reinstalled later through the launcher menu.

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

When you exit the Wiki with `/exit`, you return to the launcher.

---

## Usage

### Commands

| Command | Description |
|---|---|
| `<free text>` | Ask a question about your notes using RAG |
| `/write <filename> <description>` | Create a structured note from user-provided BJJ knowledge |
| `/update <filename> <new information>` | Merge new information into an existing note |
| `/reindex` | Rebuild the vector index after manual vault changes |
| `/exit` | Exit the Wiki and return to the launcher |

Example:

```text
>> /write Rear-Naked-Choke Classic choke from back control. Wrap the arm around the neck, secure the grip and bring the elbows together.
```

The generated note is shown as a preview before saving and must be confirmed by the user.

---

## How It Works

```text
                         User Input
                             │
              ┌──────────────┴──────────────┐
              │                             │
         /write /update                  Question
              │                             │
              ▼                             ▼
       Schema + Rules               Hybrid Retrieval
       + Canonical Notes            Chroma + Titles
              │                             │
              ▼                             ▼
          LLM Writer                  Grounded LLM
              │
              ▼
        Markdown Vault
              │
              ▼
           Obsidian
```

### Writing

`/write` turns user-provided BJJ knowledge into a structured Markdown note.

The application:

1. Classifies the input into a supported note type
2. Loads the corresponding schema and global writing rules
3. Provides existing note titles as canonical wiki entities
4. Structures the supplied knowledge
5. Shows the generated note before saving it

The writer currently supports:

```text
submission
escape
sweep
pass
position
takedown
throw
```

Each type has its own schema in `app/schemas/`.

The user's description is treated as the source of technical BJJ knowledge. The LLM may reorganize, clarify, and rephrase the supplied information, but it should not intentionally fill missing technical details using general BJJ knowledge.

Unsupported schema sections remain present as:

```markdown
* TBD
```

### Updating

`/update` works against an existing Markdown note.

Both the existing note and the new user input are treated as technical source material. Existing knowledge is preserved while new information is integrated into the appropriate sections.

Updates use the current schema for the note type. This also allows older notes using legacy structures or headings to be migrated to the current schema while preserving their technical content.

### Wiki Links

Concrete BJJ entities are connected through Obsidian Wiki-Links:

```markdown
[[Side-Control]]
[[Mount]]
[[Butterfly-Guard]]
[[Armbar]]
```

Existing note titles are supplied to the writer as canonical entities. Links to meaningful BJJ entities may also be created before the corresponding note exists, allowing the wiki to develop naturally over time.

Detailed linking and terminology behavior is defined in `app/schemas/global_rules.md`.

### Retrieval

Questions are answered using hybrid retrieval.

**Semantic search** uses ChromaDB embeddings to find notes related to the question.

**Title matching** directly matches normalized note titles against the query. Matching is case- and hyphen-insensitive, so:

```text
Side-Control.md
```

can be found from:

```text
side control
```

Combining both approaches helps retrieve conceptually related notes while preventing short or sparsely written notes from being missed due to weak embeddings.

---

## Architecture

The application uses a lightweight layered architecture:

```text
CLI
 │
 ▼
Services
 ├────► Repository ────► Markdown / Obsidian Vault
 ├────► LLM Layer ─────► LLM Provider
 └────► Vector Store ──► ChromaDB
```

The main application structure is:

```text
LLM-BJJ-Wiki/
│
├── app/
│   ├── cli/            # Terminal interface
│   ├── services/       # Application use cases
│   ├── repositories/   # Markdown vault access
│   ├── llm/            # Provider-neutral LLM access
│   │   ├── openai/     # OpenAI implementation
│   │   └── anthropic/  # Reserved for future provider support
│   ├── vectorstore/    # ChromaDB and retrieval
│   ├── schemas/        # Note schemas and global writing rules
│   ├── config.py
│   └── main.py
│
├── example-vault/      # Empty example vault structure
├── benchmarks/         # Writer regression benchmarks
├── assets/
├── .env.example
├── requirements.txt
├── start.py
├── todo.md
└── README.md
```

Services contain the application use cases while infrastructure-specific access is kept behind dedicated repository, LLM, and vector-store layers.

The LLM layer is provider-neutral from the perspective of the application services. OpenAI is currently the implemented provider, while the structure allows additional providers to be added later.

---

## Obsidian

Obsidian acts as the visual frontend for the knowledge base.

The application handles LLM-assisted writing, updating, retrieval, and question answering, while Obsidian provides:

- browsing and manually editing notes
- following `[[Wiki-Links]]`
- navigating related techniques
- exploring relationships through Graph View

Obsidian must be installed separately.

The Markdown files remain the source of truth, so the vault can still be viewed, edited, moved, or used directly without running the application.

---

## Configuration

Configuration is stored locally in `.env`.

Example:

```text
LLM_PROVIDER=openai
OPENAI_API_KEY=your_api_key_here
VAULT_PATH=C:\Users\YourName\Documents\Obsidian\BJJ
LANGUAGE=English
WRITER_MODEL=gpt-5.6-luna
CLASSIFIER_MODEL=gpt-4.1-mini
```

Normally, configuration can be managed through the launcher instead of editing `.env` manually.

`.env` is excluded through `.gitignore`, while `.env.example` is included as a template.

Note folders are mapped by technique type through `TYPE_TO_FOLDER` in `app/config.py`. Adding a new note type requires a folder mapping and a corresponding schema.

---

## Run Without the Launcher

For normal use:

```bash
python start.py
```

For development, the application can also be started directly:

```bash
python -m app.main
```

Direct startup bypasses the launcher's setup, configuration validation, and dependency checks.

---

## Writer Benchmark

The repository contains a benchmark suite for testing note generation against real BJJ input cases.

```text
benchmarks/
└── writer/
    ├── cases/
    ├── model_pricing.py
    └── run_writer_benchmark.py
```

Benchmarks can compare writer models using identical inputs and deterministic expectations such as required or forbidden Wiki-Links.

Runs also record token usage, execution time, and estimated API cost.

Run the complete benchmark with:

```bash
python -m benchmarks.writer.run_writer_benchmark
```

Or run a specific case:

```bash
python -m benchmarks.writer.run_writer_benchmark butterfly_sweep_test
```

The benchmark is intended to catch repeatable structural and Wiki-Linking errors rather than replace manual evaluation of BJJ content quality.

---

## Roadmap

Planned improvements include smarter command routing, fuzzy note matching, duplicate detection, undo support, additional LLM providers, wiki linting, a BJJ terminology glossary, and deriving a knowledge graph from Markdown relationships.

See [`todo.md`](todo.md) for the full roadmap.

---

## Notes

- OpenAI API usage may incur costs.
- The API key is stored locally in `.env`.
- User-created Markdown notes remain in the configured vault and are not committed to this repository by the application.
- Do not store sensitive information in notes that will be sent to an external LLM provider.
- This is currently a personal and learning project rather than a production system.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.