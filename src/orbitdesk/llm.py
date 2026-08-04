import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def generate_answer(question, evidence):

    context = "\n\n".join(
        f"Source: {item['document_id']}\n{item['passage']}"
        for item in evidence
    )

    prompt = f"""
You are OrbitDesk's support assistant.

Answer the user's question using ONLY the provided knowledge-base evidence.
If the evidence does not identify one specific cause, explain the documented
possible causes and tell the user what they should check.

Do not invent facts.
Do not claim that you performed an action.

User question:
{question}

Knowledge-base evidence:
{context}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content