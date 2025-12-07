import os
from groq import Groq
import asyncio
from concurrent.futures import ThreadPoolExecutor
from dotenv import load_dotenv

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

executor = ThreadPoolExecutor()

def _groq_call(user_message: str):
    """
    Blocking Groq call executed in a background thread
    """
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant", 
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an empathetic AI assistant."
                    "You are user's friend and try to ask about user's day and whats going on in his life."
                     "Always reply in under 70 words unless the user requests a long explanation. "
                     "Keep responses supportive, warm, and concise."

                )
            },
            {"role": "user", "content": user_message}
        ],
        max_tokens=200,
        temperature=0.7
    )

    # IMPORTANT: Correct extraction
    return response.choices[0].message.content


async def get_chatbot_response(user_message: str):
    """
    Async wrapper for thread execution
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, _groq_call, user_message)
