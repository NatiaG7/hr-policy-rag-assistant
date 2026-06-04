"""Retrieve relevant policy chunks for a user question."""

from langchain_core.documents import Document


def retrieve(query: str, retriever, k: int = 3) -> list[Document]:
    """Return top-k document chunks for the query."""
    return retriever.invoke(query)[:k]


def format_context(docs: list[Document]) -> str:
    """Join retrieved chunks into a single context string."""
    return "\n\n".join(doc.page_content for doc in docs)
