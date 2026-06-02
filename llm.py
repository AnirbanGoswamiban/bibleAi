import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel("gemini-2.5-flash")


def build_prompt(question: str, context: str) -> str:
    return f"""
You are a Bible assistant.

Use the supplied Bible passages as evidence.

When answering:

- Explain the meaning in natural language.
- Cite relevant references.
- Do not simply repeat verses.
- If the passages do not answer the question, say so.
- If the question is emotional or personal, provide a compassionate answer grounded in the retrieved passages.

Bible Passages:

{context}

Question:
{question}
"""


def answer_question(question: str, context: str):
    try:
        response = model.generate_content(
            build_prompt(question, context)
        )

        return response.text if response and response.text else (
            "Sorry, I couldn't generate an answer."
        )

    except Exception:
        return "Sorry, I couldn't generate an answer right now."


def stream_answer(question: str, context: str):
    try:
        response = model.generate_content(
            build_prompt(question, context),
            stream=True
        )

        has_content = False

        for chunk in response:
            try:
                if chunk.text:
                    has_content = True
                    yield chunk.text
            except Exception:
                continue

        if not has_content:
            yield "Sorry, I couldn't generate an answer."

    except Exception:
        yield "Sorry, I couldn't generate an answer right now."