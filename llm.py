import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(
    api_key=os.getenv("GEMINI_API_KEY")
)

model = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def answer_question(question: str, context: str):
    prompt = f"""
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
    response = model.generate_content(prompt)

    return response.text

def stream_answer(question: str, context: str):

    prompt = f"""
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
    response = model.generate_content(prompt,stream=True)


    for chunk in response:
        if chunk.text:
            yield chunk.text