"""Gradio UI for HR policy RAG (optional demo)."""

import gradio as gr

from src.formatting import format_full_response
from src.pipeline import ask, build_index


def chat(user_input: str) -> tuple[str, str]:
    if not user_input.strip():
        return "Please enter a question.", ""
    try:
        result = ask(user_input)
        return format_full_response(result)
    except FileNotFoundError:
        return (
            "Vector index not found.",
            "Click **Rebuild index** first, then ask again.",
        )
    except Exception as e:
        return (
            f"Error: {e}",
            "Run `python scripts/build_index.py` from the project root.",
        )


def rebuild_index() -> str:
    try:
        build_index()
        return "Index rebuilt from sample handbook. You can ask questions now."
    except Exception as e:
        return f"Build failed: {e}"


with gr.Blocks(title="HR Policy Assistant") as demo:
    gr.Markdown(
        """
        # HR Policy RAG Assistant
        Answers are grounded in **retrieved policy chunks** from your indexed documents.
        """
    )
    with gr.Row():
        rebuild_btn = gr.Button("Rebuild index (sample doc)")
        rebuild_out = gr.Textbox(label="Index status", interactive=False)

    user_input = gr.Textbox(
        label="Your question",
        placeholder="What are employee benefits?",
        lines=2,
    )
    with gr.Row():
        answer_out = gr.Textbox(label="Answer", lines=6, scale=1)
        sources_out = gr.Textbox(label="Retrieved sources", lines=10, scale=1)

    ask_btn = gr.Button("Ask", variant="primary")

    rebuild_btn.click(rebuild_index, outputs=rebuild_out)
    ask_btn.click(chat, inputs=user_input, outputs=[answer_out, sources_out])
    user_input.submit(chat, inputs=user_input, outputs=[answer_out, sources_out])

if __name__ == "__main__":
    demo.launch()
