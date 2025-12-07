# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from .db import conversation_collection
# from .chatbot import get_chatbot_response
# from .sentiment import get_sentiment_label   # <-- NEW
# from .trend_summary_llm import generate_llm_summary
# from .trend_llm import classify_mood_with_llm
# from .trend import get_user_trend



# app = FastAPI()
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # allow all frontend origins
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )
# class ChatRequest(BaseModel):
#     user_id: str
#     message: str
# @app.get("/trend/{user_id}")
# async def trend(user_id: str):
#     records = await conversation_collection.find({"user_id": user_id}).to_list(None)

#     if not records:
#         return {"trend": "No messages yet", "summary": ""}

#     # FIX: run the correct function
#     mood = await get_user_trend(user_id)

#     # LLM summary
#     summary = await generate_llm_summary(user_id)

#     return {
#         "trend": mood,
#         "summary": summary
#     }

# @app.get("/llm-summary/{user_id}")
# async def llm_summary(user_id: str):
#     summary = await generate_llm_summary(user_id)
#     return {"summary": summary}

# @app.post("/chat")
# async def chat(req: ChatRequest):
#     try:
#         # 1. Analyze sentiment of user message
#         sentiment = get_sentiment_label(req.message)

#         # 2. Get chatbot reply
#         bot_reply = await get_chatbot_response(req.message)

#         # 3. Save to MongoDB
#         await conversation_collection.insert_one({
#             "user_id": req.user_id,
#             "user_message": req.message,
#             "sentiment": sentiment,        # <-- NEW
#             "bot_reply": bot_reply
#         })

#         # 4. Return response to frontend
#         return {
#             "reply": bot_reply,
#             "sentiment": sentiment      # <-- NEW
#         }

#     except Exception as e:
#         return {"error": str(e)}

# @app.delete("/reset/{user_id}")
# async def reset_chat(user_id: str):
#     try:
#         # delete all conversation records for this user
#         await conversation_collection.delete_many({"user_id": user_id})
#         return {"status": "success", "message": "Chat history cleared."}
#     except Exception as e:
#         return {"error": str(e)}
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .db import conversation_collection
from .chatbot import get_chatbot_response
from .sentiment import get_sentiment_label
from .trend import get_user_trend
from .trend_summary_llm import generate_llm_summary

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

@app.get("/trend/{user_id}")
async def trend(user_id: str):
    trend_label = await get_user_trend(user_id)
    return {"trend": trend_label}

@app.get("/llm-summary/{user_id}")
async def llm_summary(user_id: str):
    summary = await generate_llm_summary(user_id)
    return {"summary": summary}

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

@app.delete("/reset/{user_id}")
async def reset_chat(user_id: str):
    try:
        await conversation_collection.delete_many({"user_id": user_id})
        return {"status": "success", "message": "Chat history cleared."}
    except Exception as e:
        return {"error": str(e)}
