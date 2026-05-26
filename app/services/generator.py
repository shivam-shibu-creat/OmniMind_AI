import os

from dotenv import load_dotenv

from openai import OpenAI

from langsmith import traceable



load_dotenv()



client = OpenAI(

    base_url="https://openrouter.ai/api/v1",

    api_key=os.getenv(
        "OPENROUTER_API_KEY"
    )
)

@traceable
def generate_answer(

    question,

    context
):

    prompt = f"""

You are an advanced AI assistant.

Answer ONLY from the provided context.

If the answer is not present in the context,
say:

"I could not find the answer in the document."

Context:
{context}

Question:
{question}

"""

    response = client.chat.completions.create(

        model="openai/gpt-4o-mini",

        messages=[

            {

                "role": "system",

                "content": (
                    "You are a helpful AI assistant."
                )
            },

            {

                "role": "user",

                "content": prompt
            }
        ],

        temperature=0.2
    )

    answer = (

        response
        .choices[0]
        .message
        .content
    )

    return answer