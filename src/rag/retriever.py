from src.rag.chucking import split
from src.rag.embeddings import embed
from src.rag.loader import rag_load
from src.rag.vector_store import store


def rag_indexar():
    paginas = rag_load()
    chunks = split(paginas)
    embedding = embed()
    
    db = store(chunks, embedding)
    

    retriever = db.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 2},  # recuperar os 3 chunks mais similares
    )
    
    return retriever