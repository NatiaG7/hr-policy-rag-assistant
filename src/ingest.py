"""Load HR policy documents from PDF or plain text."""

from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document


def load_documents(path: Path) -> list[Document]:
    """
    Load a single file. Supports .pdf and .txt.

    Raises FileNotFoundError if path does not exist.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {path}")

    suffix = path.suffix.lower()
    if suffix == ".pdf":
        loader = PyPDFLoader(str(path))
        return loader.load()
    if suffix in {".txt", ".md"}:
        loader = TextLoader(str(path), encoding="utf-8")
        return loader.load()

    raise ValueError(f"Unsupported file type: {suffix}. Use .pdf, .txt, or .md.")


def load_default_sample() -> list[Document]:
    """Load the bundled sample employee handbook."""
    from src.config import DATA_SAMPLE

    sample = DATA_SAMPLE / "employee_handbook_sample.txt"
    return load_documents(sample)
