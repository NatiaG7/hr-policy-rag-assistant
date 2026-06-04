"""Generate answers from retrieved context using a seq2seq LLM."""

from transformers import AutoModelForSeq2SeqLM, AutoTokenizer, pipeline

from src.config import LLM_MODEL
from src.query import format_context, retrieve

_tokenizer = None
_model = None
_pipe = None


def _load_pipeline(model_name: str = LLM_MODEL):
    global _tokenizer, _model, _pipe
    if _pipe is not None:
        return _pipe

    _tokenizer = AutoTokenizer.from_pretrained(model_name)
    _model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    _pipe = pipeline(
        "text2text-generation",
        model=_model,
        tokenizer=_tokenizer,
        max_new_tokens=150,
    )
    return _pipe


def build_prompt(question: str, context: str) -> str:
    """Build a grounded prompt for the HR assistant."""
    return f"""You are an HR policy assistant. Answer using ONLY the context below.

Context:
{context}

Question: {question}

Answer:"""


def answer_question(
    question: str,
    retriever,
    model_name: str = LLM_MODEL,
    top_k: int = 2,
) -> dict:
    """
    RAG: retrieve chunks, then generate an answer.

    Returns dict with answer, context, and retrieved chunk count.
    """
    docs = retrieve(question, retriever, k=top_k)
    context = format_context(docs)

    pipe = _load_pipeline(model_name)
    prompt = build_prompt(question, context)
    result = pipe(prompt, max_new_tokens=150, do_sample=False)
    text = result[0]["generated_text"]

    # flan-t5 may echo prompt; keep only new content after "Answer:"
    if "Answer:" in text:
        text = text.split("Answer:")[-1].strip()

    return {
        "answer": text,
        "context": context,
        "chunks_used": len(docs),
    }
