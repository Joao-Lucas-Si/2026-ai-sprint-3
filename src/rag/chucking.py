from langchain_classic.schema import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter


def split(paginas: list[Document]):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1024,
        chunk_overlap=15,
        separators=["\n\n", "\n", ". ", " ", ""],
    )
    # Dividir as páginas em chunks menores
    chunks = splitter.split_documents(paginas)
    tamanhos = [len(c.page_content) for c in chunks]


    return chunks