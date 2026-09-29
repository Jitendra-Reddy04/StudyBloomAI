import os

from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()


NOT_FOUND = "I couldn't find this in your documents."


SYSTEM = (
    "You answer questions using ONLY the numbered context passages provided. "
    "Do not use outside knowledge. "
    "Cite the passages you used like [1] or [2]. "
    "Be concise and clear. "
    f"If the context does not contain the answer, reply exactly: {NOT_FOUND}"
)


def complete(system, user):
    """Call the Groq LLM through its OpenAI-compatible API."""

    model = os.getenv(
        "LLM_MODEL",
        "openai/gpt-oss-20b"
    )

    client = OpenAI(
        base_url=os.getenv(
            "OPENAI_BASE_URL",
            "https://api.groq.com/openai/v1"
        ),
        api_key=os.getenv("OPENAI_API_KEY")
    )

    response = client.chat.completions.create(
        model=model,
        max_tokens=700,
        messages=[
            {
                "role": "system",
                "content": system
            },
            {
                "role": "user",
                "content": user
            }
        ]
    )

    return response.choices[0].message.content


def answer(question, hits, min_score=0.25):
    """
    Generate an answer using only retrieved document chunks.
    """

   
    if not hits:
        return NOT_FOUND

    
    ctx = "\n\n".join(
        f"[{i + 1}] "
        f"({h['source']}, p.{h['page']})\n"
        f"{h['text']}"
        for i, h in enumerate(hits)
    )

   
    return complete(
        SYSTEM,
        f"Context:\n{ctx}\n\nQuestion: {question}"
    )
