"""Chunk documents, embed, and store in ChromaDB."""

from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from src.config import (
    CHROMA_DIR,
    CHUNK_OVERLAP,
    CHUNK_SIZE,
    EMBEDDING_MODEL,
)


def split_documents(documents: list[Document]) -> list[Document]:
    """Split loaded documents into overlapping chunks."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    return splitter.split_documents(documents)


def build_vector_store(
    documents: list[Document],
    persist_directory: Path | None = None,
) -> Chroma:
    """Embed chunks and persist to ChromaDB."""
    persist_directory = persist_directory or CHROMA_DIR
    persist_directory.mkdir(parents=True, exist_ok=True)

    chunks = split_documents(documents)
    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=str(persist_directory),
    )


def get_retriever(
    documents: list[Document] | None = None,
    persist_directory: Path | None = None,
):
    """
    Build or load retriever.

    If documents is provided, rebuilds the vector store.
    Otherwise loads from persist_directory (must exist).
    """
    persist_directory = persist_directory or CHROMA_DIR

    if documents is not None:
        db = build_vector_store(documents, persist_directory)
        return db.as_retriever()

    if not persist_directory.exists() or not any(persist_directory.iterdir()):
        raise FileNotFoundError(
            f"No vector index at {persist_directory}. "
            "Run: python scripts/build_index.py"
        )

    embeddings = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
    db = Chroma(
        persist_directory=str(persist_directory),
        embedding_function=embeddings,
    )
    return db.as_retriever()
