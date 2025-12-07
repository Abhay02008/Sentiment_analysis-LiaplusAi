import os
from groq import Groq
from dotenv import load_dotenv
from .db import conversation_collection

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

async def generate_llm_summary(user_id: str):
    # Fetch user's chat history
    records = await conversation_collection.find(
        {"user_id": user_id}
    ).to_list(None)

    if not records:
        return "No conversations found."

    messages = [r.get("user_message") for r in records if r.get("user_message")]
    sentiments = [r.get("sentiment") for r in records if r.get("sentiment")]

    full_text = "\n".join(messages)

    prompt = f"""
You are an empathetic emotional analysis assistant.

Analyze the user's entire conversation for:
- mood shifts,
- tone changes,
- emotional highs/lows,
- key day events mentioned (like gym, exams, work, stress, family, etc.)
- how their mood evolved from start to end.

Write a natural human summary (NOT robotic, NOT rule-based).
The summary MUST be under 100 words.
Be warm, understanding, and insightful.

Conversation messages:
{full_text}

Sentiments detected per message:
{sentiments}

Write the summary now:
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "system", "content": "You summarize emotions empathetically."},
                  {"role": "user", "content": prompt}],
        max_tokens=150,
        temperature=0.7
    )

    return response.choices[0].message.content.strip()
