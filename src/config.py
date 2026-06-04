"""Paths and default settings for the HR RAG pipeline."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA_SAMPLE = ROOT / "data" / "sample"
DATA_RAW = ROOT / "data" / "raw"
CHROMA_DIR = ROOT / "outputs" / "chroma_db"
OUTPUTS_DIR = ROOT / "outputs"

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
LLM_MODEL = "google/flan-t5-base"  # lighter default; swap to Qwen in notebook for GPU runs
