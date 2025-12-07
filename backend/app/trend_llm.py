import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

TREND_SYSTEM_PROMPT = """
You are an advanced emotional trend analyzer.

Your job is to read the ENTIRE conversation (all user messages AND AI replies)
and determine the user's **final emotional state**, based on:
1. Emotional shifts (positive → negative, calm → stressed, happy → worried, etc.)
2. Severity of emotions (fear, panic, shock, sadness, grief, stress, anxiety, depression)
3. Emotional impact of events (e.g., danger, loss, failure, trauma, major success)
4. The meaning, context, and emotional weight behind the user's words.
5. DO NOT average sentiments — interpret emotions like a human.
6. Focus on the user's FINAL emotional state.

Your output MUST be ONLY ONE of these labels:

- Positive
- Mostly Positive
- Neutral
- Mostly Neutral
- Mostly Negative
- Negative

IMPORTANT:
- Do NOT include explanation.
- Do NOT include reasoning.
- Only output the single label exactly.
"""

def classify_mood_with_llm(full_chat: str):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": TREND_SYSTEM_PROMPT},
            {"role": "user", "content": full_chat}
        ],
        max_tokens=5,
        temperature=0
    )

    return response.choices[0].message.content.strip()
