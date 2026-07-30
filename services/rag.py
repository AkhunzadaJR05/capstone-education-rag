import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))

SYSTEM_PROMPT = """You are a helpful assistant answering questions based ONLY on the provided context from uploaded documents.

Rules:
- Only use information from the context below to answer.
- If the context does not contain enough information to answer, respond exactly with: I don't know.
- Do not use any outside knowledge, even if you know the answer.
- Be concise and direct."""


def build_context(chunks: list[dict]) -> str:
    parts = []
    for chunk in chunks:
        parts.append(f"[Source: {chunk['filename']}, chunk {chunk['chunk_index']}]\n{chunk['text']}")
    return "\n\n".join(parts)


def generate_answer(query: str, retrieved_chunks: list[dict], history: list[dict]) -> str:
    context = build_context(retrieved_chunks)

    messages = [{"role": "system", "content": SYSTEM_PROMPT}]

    for turn in history:
        messages.append({"role": turn["role"], "content": turn["content"]})

    user_message = f"Context:\n{context}\n\nQuestion: {query}"
    messages.append({"role": "user", "content": user_message})

    response = groq_client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=messages,
        temperature=0.2,
    )

    return response.choices[0].message.content