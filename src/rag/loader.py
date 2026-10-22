from langchain_classic.document_loaders import PyMuPDFLoader


def rag_load():
    # loader = PyMuPDFLoader("documento.pdf")
    # paginas = loader.load()
    # print(f"Páginas carregadas: {len(paginas)}")
    # print(f"Metadados da pág. 1: {paginas[0].metadata}")
    # → {'source': 'manual.pdf', 'page': 0, 'total_pages': 24, ...}
    # print(f"Trecho da pág. 1:\n{paginas[0].page_content[:300]}")
    # return paginas
    # Carregar múltiplos PDFs de uma vez
    pdfs = [
        "protocolos.pdf",
    ]
    paginas = []
    for pdf in pdfs:
        paginas.extend(PyMuPDFLoader(f"data/knowledge_base/{pdf}").load())
    return paginas