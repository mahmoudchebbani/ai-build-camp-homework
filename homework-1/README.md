# Homework 1: Document Processing with AI

Extract text from Allen Downey's free [Green Tea Press](https://greenteapress.com) books, chunk it, index it and build a RAG system on top.

Verified with `markitdown 0.1.7`, `minsearch 0.2.0` and `gitsource 0.0.5`.

## Setup

```bash
cd homework-1
uv sync
cp .env.example .env   # then add your OpenAI key
```

## Pipeline

Run the scripts from inside `homework-1/`, in this order:

| Step | Script | What it does |
| --- | --- | --- |
| 1 | `download_books.py` | Downloads every PDF in `books.csv` into `books/` |
| 2 | `convert_books.py` | Converts the PDFs to markdown in `books_text/` with markitdown |
| 3 | `chunk_books.py` | Drops empty lines and chunks each book (`size=100`, `step=50`) |
| 4 | `index_books.py` | Joins chunk lines and indexes them with minsearch |
| 5 | `rag.py` | RAG over the index with `gpt-4o-mini`, returns token usage |
| 6 | `rag_structured.py` | Same RAG with a Pydantic `RAGResponse` structured output |

```bash
uv run python download_books.py
uv run python convert_books.py
uv run python chunk_books.py
uv run python index_books.py
uv run python rag.py
uv run python rag_structured.py
```

## Answers

| # | Question | Result | Answer |
| --- | --- | --- | --- |
| 1 | Lines in Think Python 2e markdown | 9,702 (`wc -l`, no trailing newline) | 9,703 |
| 2 | Chunks for Think Python 2e | 189 | 189 |
| 3 | Chunks indexed | 988 | 988 |
| 4 | Book of top result for "python function definition" | `PhysicalModelingInMatlab4.md` | Physical Modeling in MATLAB |
| 5 | Input tokens for one RAG query | 7,926 | 7944 |
| 6 | Extra input tokens with structured output | 8,112 − 7,926 = 186 | 186 |
