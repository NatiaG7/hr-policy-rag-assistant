# HR Policy RAG Assistant

Document intelligence pipeline that ingests HR policy text, stores semantic embeddings in ChromaDB, and answers employee questions with retrieval-augmented generation (RAG).

**Auditable answers:** the app shows **retrieved source chunks** alongside each response so HR teams can verify policy grounding.

## Business problem

HR teams maintain long policy PDFs. Employees struggle to find answers on benefits, leave, and workplace rules. This project automates **document ingestion → semantic search → grounded answers** so responses cite internal policy content instead of generic LLM guesses.

## Dataset

| Item | Detail |
|------|--------|
| **Demo document** | `data/sample/employee_handbook_sample.txt` — **synthetic** handbook (safe to publish) |
| **Your PDFs** | Place under `data/raw/` — not committed to git |
| **Cloud storage** | Optional S3/URL download via `scripts/download_data.py` ([data/README.md](data/README.md)) |

## Methodology

```
PDF/TXT → load & chunk → embeddings (MiniLM) → ChromaDB → retrieve top-k → LLM answer
```

1. **Ingest** — `PyPDFLoader` or `TextLoader` (`src/ingest.py`)
2. **Chunk** — 500 chars, 50 overlap (`src/config.py`, `src/embed.py`)
3. **Embed** — `sentence-transformers/all-MiniLM-L6-v2`
4. **Store** — ChromaDB (`outputs/chroma_db/`, gitignored)
5. **Retrieve** — similarity search (`src/query.py`)
6. **Generate** — `google/flan-t5-base` (`src/generate.py`); use `--retrieve-only` to skip the LLM

> **Notebook vs repo:** [notebooks/hr_policy_rag_pipeline.ipynb](notebooks/hr_policy_rag_pipeline.ipynb) is the original Colab workflow (Qwen on GPU). The **maintained code** is under `src/` and uses **flan-t5-base** by default for lighter local runs.

## Technologies

- Python, LangChain, ChromaDB, Hugging Face (embeddings + LLM)
- Gradio (`app.py`)
- Optional: AWS S3 via `boto3` + `scripts/download_data.py`

## Project structure

```
hr-policy-rag-assistant/
├── app.py                      # Gradio: answer + retrieved sources
├── src/
│   ├── config.py               # Paths, models, chunk settings
│   ├── ingest.py               # Load PDF/TXT
│   ├── embed.py                # Chunk + ChromaDB
│   ├── query.py                # Retrieval
│   ├── generate.py             # LLM answer
│   ├── formatting.py           # CLI/UI formatting
│   └── pipeline.py             # Orchestration
├── scripts/
│   ├── build_index.py          # Build vector index
│   ├── ask.py                  # CLI query
│   ├── run_examples.py         # Eval questions → sample_results.json
│   └── download_data.py        # Optional S3/URL fetch
├── notebooks/                  # Colab history (see disclaimer in notebook)
├── data/sample/                # Synthetic demo handbook
├── outputs/
│   ├── example_queries.json
│   └── sample_results.json     # Illustrative until you run run_examples.py
└── requirements.txt
```

## Quick start

```bash
cd hr-policy-rag-assistant
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 1) Build index from sample handbook
python scripts/build_index.py

# 2) Ask (CLI) — prints answer + retrieved sources
python scripts/ask.py "What are employee benefits?" --save

# Retrieval only (no LLM download)
python scripts/ask.py "How many vacation days do employees receive?" --retrieve-only

# 3) Regenerate verified results (replaces illustrative sample_results.json)
python scripts/run_examples.py

# 4) Gradio UI
python app.py
```

### Use your own PDF

```bash
cp /path/to/policy.pdf data/raw/
python scripts/build_index.py --document data/raw/policy.pdf
python scripts/ask.py "What is the parental leave policy?"
```

## Results

The bundled [outputs/sample_results.json](outputs/sample_results.json) is **illustrative** until you run the pipeline locally. After `build_index.py` and `run_examples.py`, `_meta.status` becomes `"executed"` and `chunks_used` will be populated.

Expected topics on the **synthetic** handbook:

| Question | Policy content (from sample doc) |
|----------|----------------------------------|
| What are employee benefits? | Health/dental/vision, 15 vacation days, 401(k) match up to 4% |
| How many vacation days? | 15 vacation days per year (+ sick days, holidays) |
| Is remote work allowed? | Up to two days per week remote, manager approval |

```bash
python scripts/build_index.py
python scripts/run_examples.py              # retrieval-only
python scripts/run_examples.py --generate   # full RAG with flan-t5
```

## Future improvements

- FastAPI `/query` endpoint + Docker
- LangGraph multi-step retrieval agent
- Retrieval hit-rate evaluation on `example_queries.json`
- Qwen2.5 config flag in `src/config.py` for GPU runs

## Author

Natia Gogitidze — AI/ML Data Engineer portfolio project
