#!/usr/bin/env python3
"""Ask a question against the HR policy RAG index."""

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import OUTPUTS_DIR  # noqa: E402
from src.formatting import format_full_response  # noqa: E402
from src.pipeline import ask  # noqa: E402


def main():
    parser = argparse.ArgumentParser(description="Query HR policy RAG")
    parser.add_argument("question", type=str, help="Question to ask")
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save result to outputs/last_query.json",
    )
    parser.add_argument(
        "--retrieve-only",
        action="store_true",
        help="Skip LLM; show retrieved chunks only (faster, no model download)",
    )
    args = parser.parse_args()

    result = ask(args.question, generate=not args.retrieve_only)
    answer, sources = format_full_response(result)

    print("\n--- Answer ---\n")
    print(answer)
    print("\n")
    print(sources)

    if args.save:
        OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
        out = OUTPUTS_DIR / "last_query.json"
        with open(out, "w") as f:
            json.dump(result, f, indent=2)
        print(f"\nSaved to {out}")


if __name__ == "__main__":
    main()
