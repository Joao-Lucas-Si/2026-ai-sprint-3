import os

from langchain_ollama.embeddings import OllamaEmbeddings


def embed():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text",
    )
    return embeddings