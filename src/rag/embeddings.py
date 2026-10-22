from langchain_classic.embeddings import OllamaEmbeddings


def embed():
    embeddings = OllamaEmbeddings(
        model="nomic-embed-text"
    )
    return embeddings
