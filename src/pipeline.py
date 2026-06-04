"""End-to-end HR policy RAG pipeline."""

from pathlib import Path

from src.embed import build_vector_store, get_retriever
from src.generate import answer_question
from src.ingest import load_default_sample, load_documents


def build_index(document_path: Path | None = None):
    """
    Ingest documents and build the vector index.

    Uses sample handbook if document_path is None.
    """
    if document_path is None:
        documents = load_default_sample()
    else:
        documents = load_documents(document_path)

    build_vector_store(documents)
    return len(documents)


def ask(
    question: str,
    document_path: Path | None = None,
    *,
    generate: bool = True,
    top_k: int = 2,
) -> dict:
    """
    Full RAG query. Rebuilds index if document_path given; else uses persisted store.

    Set generate=False for retrieval-only (no LLM download) — useful for eval and CI.
    """
    if document_path is not None:
        documents = load_documents(document_path)
        retriever = get_retriever(documents=documents)
    else:
        retriever = get_retriever()

    if generate:
        return answer_question(question, retriever, top_k=top_k)

    from src.query import format_context, retrieve

    docs = retrieve(question, retriever, k=top_k)
    context = format_context(docs)
    return {
        "answer": "[Retrieval only] Top matching policy excerpts are shown in sources.",
        "context": context,
        "chunks_used": len(docs),
        "mode": "retrieval_only",
    }
