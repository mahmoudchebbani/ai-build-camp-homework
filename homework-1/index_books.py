from gitsource import chunk_documents
from minsearch import Index

from chunk_books import load_documents


def prepare_documents(chunks):
    return [{**chunk, "content": "\n".join(chunk["content"])} for chunk in chunks]


def build_index():
    chunks = chunk_documents(load_documents(), size=100, step=50)
    documents = prepare_documents(chunks)
    index = Index(text_fields=["content"], keyword_fields=["source"])
    index.fit(documents)
    return index, documents


if __name__ == "__main__":
    index, documents = build_index()
    print("indexed:", len(documents), "| index.docs:", len(index.docs))
