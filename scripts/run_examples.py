#!/usr/bin/env python3
"""Build index and run example questions; save results for README/portfolio."""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from src.config import OUTPUTS_DIR  # noqa: E402
from src.pipeline import ask, build_index  # noqa: E402


def main():
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--generate",
        action="store_true",
        help="Use LLM generation (downloads flan-t5). Default: retrieval-only.",
    )
    args = parser.parse_args()

    examples_path = OUTPUTS_DIR / "example_queries.json"
    with open(examples_path) as f:
        examples = json.load(f)

    print("Building index from sample handbook...")
    build_index()

    results = []
    for item in examples:
        question = item["question"]
        print(f"\nQ: {question}")
        result = ask(question, generate=args.generate)
        print(f"chunks: {result['chunks_used']}, mode: {result.get('mode', 'rag')}")
        results.append(
            {
                "question": question,
                "expected_topics": item.get("expected_topics", []),
                "answer": result["answer"],
                "chunks_used": result["chunks_used"],
                "sources_preview": result["context"][:800],
                "mode": result.get("mode", "rag"),
            }
        )

    payload = {
        "_meta": {
            "status": "executed",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "generate_llm": args.generate,
            "regenerate_command": "python scripts/build_index.py && python scripts/run_examples.py",
        },
        "results": results,
    }

    out_path = OUTPUTS_DIR / "sample_results.json"
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nSaved {len(results)} results to {out_path}")


if __name__ == "__main__":
    main()
