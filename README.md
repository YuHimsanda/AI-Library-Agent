# AI Library Agent

An AI-powered library assistant that helps users discover books, check inventory, and reserve available copies through a conversational interface.

The project combines a LangGraph ReAct agent with semantic book search, a Chroma vector database, and a SQLite inventory database. A Streamlit application provides the user interface.

## Features

- Search the catalogue using natural-language questions.
- Retrieve book details from the semantic index.
- Check whether a book is currently available.
- Reserve an available book for a Student ID.
- Maintain conversation context during a chat session.
- Use a local SQLite database for inventory and reservations.

## Requirements

- Python 3.14 or newer
- [uv](https://docs.astral.sh/uv/)
- A Groq API key

## Quick Start

### 1. Install dependencies

From the project root, run:

```powershell
uv sync
```

### 2. Configure the API key

Create `.venv/.env` and add your Groq API key:

```dotenv
GROQ_API_KEY=your_groq_api_key
```

The application loads this file when it starts. Keep it out of source control.

### 3. Create the library database

Run this once to create `library.db` and add the sample inventory:

```powershell
uv run python setup_db.py
```

### 4. Build the semantic book index

Create the Chroma index from `data/books.csv`:

```powershell
uv run python digest.py
```

The first run downloads the `all-MiniLM-L6-v2` embedding model and may take several minutes. The generated index is stored in `chroma_db/`.

### 5. Start the Streamlit application

```powershell
uv run streamlit run Streamlit/ui.py
```

Open the local URL printed by Streamlit, typically `http://localhost:8501`.

## How It Works

1. A user sends a question through the Streamlit chat interface.
2. The LangGraph agent decides whether to search books, check availability, or reserve a book.
3. Semantic search retrieves relevant catalogue records from Chroma.
4. Inventory and reservation operations are handled by SQLite.
5. Conversation state is retained for the current chat session.

Before a reservation, the agent checks availability and requires a Student ID. Users should confirm reservation details when prompted.

## Project Structure

```text
.
├── agent.py              # LangGraph agent and conversation configuration
├── tools.py              # Semantic search, availability, and reservation tools
├── digest.py             # Imports books.csv into Chroma
├── setup_db.py           # Creates and seeds the SQLite library database
├── data/books.csv        # Source catalogue data
├── chroma_db/            # Generated semantic-search storage
├── Streamlit/ui.py       # Streamlit chat interface
└── pyproject.toml        # Project metadata and dependencies
```

## Data and Configuration

The application uses these runtime resources:

- `data/books.csv` supplies searchable book metadata.
- `chroma_db/` stores generated embeddings and must exist before semantic search is used.
- `library.db` stores inventory and reservations and is created by `setup_db.py`.
- `.venv/.env` stores the `GROQ_API_KEY` used by the language model.

If catalogue data changes, rerun `digest.py` to rebuild the semantic index. Run `setup_db.py` only when initializing a new database, because it inserts the sample inventory.

## Development

Compile-check the Streamlit interface with:

```powershell
uv run python -m py_compile Streamlit/ui.py
```

Run the command-line agent directly with:

```powershell
uv run python agent.py
```

Type `exit` or `quit` to end the command-line session.

## License

No license has been specified for this project yet.
