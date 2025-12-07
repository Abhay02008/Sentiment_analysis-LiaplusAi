from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .db import conversation_collection
from .chatbot import get_chatbot_response
from .sentiment import get_sentiment_label
from .trend import get_user_trend
from .trend_summary_llm import generate_llm_summary
#in python we use fast api format
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    user_id: str
    message: str
#for getting trend analysis
@app.get("/trend/{user_id}")
async def trend(user_id: str):
    trend_label = await get_user_trend(user_id)
    return {"trend": trend_label}
#for summary
@app.get("/llm-summary/{user_id}")
async def llm_summary(user_id: str):
    summary = await generate_llm_summary(user_id)
    return {"summary": summary}
#for chatting
@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        sentiment = get_sentiment_label(req.message)
        bot_reply = await get_chatbot_response(req.message)

        await conversation_collection.insert_one({
            "user_id": req.user_id,
            "user_message": req.message,
            "sentiment": sentiment,
            "bot_reply": bot_reply
        })

        return {
            "reply": bot_reply,
            "sentiment": sentiment
        }

    except Exception as e:
        return {"error": str(e)}
#for deleting all the history from bot's memory  about previous chat
@app.delete("/reset/{user_id}")
async def reset_chat(user_id: str):
    try:
        await conversation_collection.delete_many({"user_id": user_id})
        return {"status": "success", "message": "Chat history cleared."}
    except Exception as e:
        return {"error": str(e)}
