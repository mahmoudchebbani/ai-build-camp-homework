from collections import Counter
from pathlib import Path

from gitsource import chunk_documents


def load_documents(text_dir="books_text"):
    documents = []
    for path in sorted(Path(text_dir).glob("*.md")):
        lines = path.read_text(encoding="utf-8").split("\n")
        content = [line for line in lines if line.strip()]
        documents.append({"source": path.name, "content": content})
    return documents


if __name__ == "__main__":
    documents = load_documents()
    chunks = chunk_documents(documents, size=100, step=50)
    for source, n in sorted(Counter(c["source"] for c in chunks).items()):
        print(f"{source}: {n}")
    print("total:", len(chunks))
