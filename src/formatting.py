"""Format RAG results for CLI and UI display."""


def format_sources(context: str, chunks_used: int) -> str:
    """Format retrieved chunks for display."""
    header = f"--- Retrieved sources ({chunks_used} chunk(s)) ---\n"
    return header + context


def format_full_response(result: dict) -> tuple[str, str]:
    """Return (answer, sources) for Gradio or terminal."""
    answer = result.get("answer", "").strip()
    sources = format_sources(
        result.get("context", ""),
        result.get("chunks_used", 0),
    )
    return answer, sources
