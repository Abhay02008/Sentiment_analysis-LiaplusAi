from .db import conversation_collection
from .trend_llm import classify_mood_with_llm

async def get_user_trend(user_id: str):
    # Fetch all conversation records for this user
    records = await conversation_collection.find(
        {"user_id": user_id}
    ).to_list(None)

    if not records:
        return "No messages yet"

    # Build full conversational transcript
    conversation_text = ""
    for rec in records:
        user_msg = rec.get("user_message", "")
        bot_msg = rec.get("bot_reply", "")
        conversation_text += f"User: {user_msg}\nAI: {bot_msg}\n"

    # Final LLM classification of emotional trend
    trend_label = classify_mood_with_llm(conversation_text)

    return trend_label
