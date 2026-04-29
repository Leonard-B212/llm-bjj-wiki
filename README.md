# 🥋 BJJ LLM Wiki

A small project to query your BJJ techniques stored in Obsidian notes using an LLM.

## 🎯 Goal

* Use your own Markdown notes (Obsidian) as a knowledge base
* Ask questions via terminal
* Get answers based on your own training notes

---

## 🧠 Concept

The system follows a simple RAG (Retrieval-Augmented Generation) approach:

Question → find relevant notes → send to LLM → generate answer

### Components:

* Markdown Notes (Obsidian Vault)
* Vector Database (semantic search)
* LLM (OpenAI API)

---

## 📁 Project Structure (current)

```text id="h2f91c"
llm-bjj/
│
├── app/
│   └── main.py
│
├── .env
├── .gitignore
├── requirements.txt
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash id="0ytc7d"
git clone <https://github.com/Leonard-B212/llm-bjj-wiki.git>
cd llm-bjj
```

---

### 2. Install dependencies

```bash id="juy4c8"
pip install -r requirements.txt
```

or manually:

```bash id="m9y0fp"
pip install chromadb openai python-dotenv
```

---

### 3. Set your API key

Create a `.env` file:

```text id="cys6tx"
OPENAI_API_KEY=your_api_key
```

Important:

* `.env` is listed in `.gitignore`
* your key will not be committed

---

### 4. Configure your Vault path

In your code, set your Obsidian vault path, e.g.:

```python id="l7m0kc"
VAULT_PATH = r"C:\Users\leona\Documents\Obsidian\BJJ"
```

---

## ▶️ Run the project

```bash id="cl8m1g"
python -m app.main
```

You can now ask questions in the terminal:

```text id="sxh0g7"
Question: What can I do from Closed Guard?
```

---

## 🧩 How it works (simplified)

1. Markdown files are loaded
2. Content is stored in a vector database
3. You ask a question
4. Relevant notes are retrieved
5. The LLM generates an answer based on those notes

---

## 🧭 Current Status

* Terminal-based interaction
* Simple structure
* Focus on understanding over complexity

Planned:

* better retrieval (chunking)
* automatic note generation
* optional web interface

---

## ❗ Notes

* Do not store sensitive data in your notes
* OpenAI API usage may incur costs
* This is currently a learning project

---

## 🥋 Vision

A personal BJJ knowledge system that:

* reflects your own game
* understands connections between techniques
* supports your learning process
