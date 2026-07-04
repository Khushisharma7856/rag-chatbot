import ollama


def generate_answer(question, context):

    prompt = f"""

You are an AI research assistant.

Answer the question only using the context below.

Context:
{context}


Question:
{question}


Answer:
"""


    response = ollama.chat(
        model="llama3.2",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )


    return response["message"]["content"]