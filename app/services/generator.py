from openai import OpenAI
import os

print("OPENAI_API_KEY =", os.getenv("OPENAI_API_KEY"))

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
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

    response = client.chat.completions.create(
        model="google/gemini-2.0-flash-exp:free",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful AI assistant."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2
    )

    return response.choices[0].message.content