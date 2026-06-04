#!/usr/bin/env python3
"""Build the Chroma vector index from a document or the default sample."""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.pipeline import build_index  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Build HR policy vector index")
    parser.add_argument(
        "--document",
        type=Path,
        default=None,
        help="Path to .pdf or .txt (default: bundled sample handbook)",
    )
    args = parser.parse_args()

    print("Building index...")
    n = build_index(args.document)
    print(f"Done. Loaded {n} document(s). Index saved to outputs/chroma_db/")


if __name__ == "__main__":
    main()
