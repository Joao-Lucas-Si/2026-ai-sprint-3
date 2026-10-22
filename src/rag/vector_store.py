import os

from langchain.embeddings import Embeddings
from langchain_classic.schema import Document
from langchain_classic.vectorstores import Chroma


def store(chunks: list[Document], embeddings: Embeddings):
    db: Chroma
    persist_directory = "./content"
    collection_name = "assistente_escrita"
    if os.path.exists("./content/chroma.sqlite3"):
        db  = Chroma(persist_directory=persist_directory, collection_name=collection_name, embedding_function=embeddings)
    else:
        db = Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            persist_directory=persist_directory,
            collection_name=collection_name
        )
        db.persist()
    print(f"Chunks indexados: {db._collection.count()}")
    return db
