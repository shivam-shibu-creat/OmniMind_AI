import os
from google import genai

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

def generate_answer(question, context):

    prompt = f"""
You are OmniMind AI.

Answer the question using the provided context.

Context:
{context}

Question:
{question}

Give a clear and detailed answer.
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text