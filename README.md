# ⭐ Sentiment Analysis Friend  

**Your AI-powered emotional companion chatbot**  

Sentiment Analysis Friend is an AI emotional companion that chats with users, detects their mood, analyzes emotional shifts across the entire conversation, and generates a supportive summary of their day.  

---

## 🧠 Overview  

It uses:  
- **Groq LLM (Llama 3.1 8B)** for empathetic conversation & mood interpretation  
- **VADER Sentiment Analyzer** for message-level sentiment detection  
- **MongoDB** to store chat history  
- **FastAPI** for the backend  
- **Custom Frontend UI** with expandable input box, mood trend modal, reset chat, and smooth chat experience  

---

## 🚀 Features  

### ✅ AI Chatbot (Groq LLM)  
- Replies empathetically like a supportive friend  
- Understands context and emotional tone  
- Always answers within **70 words**  

### ✅ Sentiment Detection  
Uses **VADER** to classify each user message as:  
- Positive  
- Neutral  
- Negative  

### ✅ Emotional Trend Analysis (LLM-powered)  
- Reads the entire chat history  
- Understands emotional shifts → *happy → stressed → relaxed*  
- Determines the final mood with labels like:  
  - Positive  
  - Mostly Positive  
  - Neutral  
  - Mostly Negative  
  - Negative  

### ✅ Summary of Mood  
- LLM generates a short, warm, 100-word emotional summary  
- Explains how your mood changed throughout the conversation  

### ✅ Chat Reset  
- Clears chat history *(from UI + MongoDB + chatbot memory)*  
- After reset → new conversation = fresh mood analysis  

### ✅ Frontend Enhancements  
- Wide chatbox  
- Growing message input *(like WhatsApp/ChatGPT)*  
- Rounded UI  
- Modal popup for mood trend  
- “Sentiment Analysis Friend” title in the header UI  
- Send button icon instead of text  

---

## 🛠️ Tech Stack  

| Component          | Technology                  |
|--------------------|-----------------------------|
| **Language**       | Python, HTML, CSS, JS        |
| **Backend**        | FastAPI                      |
| **Frontend**       | Custom HTML/CSS, JS Fetch    |
| **LLM Provider**   | Groq API (Llama 3.1)         |
| **Database**       | MongoDB Atlas                |
| **Sentiment Analysis** | VADER                   |
| **Deployment-ready** | Yes                       |

---

## 📁 Project Structure

- chatbot-sentiment/
  - backend/
    - app/
      - chatbot.py
      - sentiment.py
      - trend_llm.py
      - trend_summary_llm.py
      - main.py
      - db.py
      - ...
    - requirements.txt
  - frontend/
    - index.html


---
## 📘 Files Explanations (Technical Overview)

### 1️⃣ `chatbot.py` — LLM-Powered Chat Response Generator

#### What it does
- Loads the Groq API client.
- Sends user messages to the LLaMA‑3.1 model from a background thread.
- Uses a system prompt so the AI behaves as a friendly, empathetic, concise assistant.
- Returns a short, supportive reply (kept under 70 words).

#### Why it exists
- Direct LLM calls would block FastAPI’s async event loop.
- Uses `ThreadPoolExecutor` with `asyncio.run_in_executor()` to keep chat responses efficient and non‑blocking.

---

### 2️⃣ `sentiment.py` — VADER Sentiment Classifier

#### What it does
- Uses the VADER sentiment model tailored for chat and social-style text.
- Calculates sentiment scores (positive, negative, neutral).
- Converts the compound score into one of three labels: **Positive**, **Neutral**, or **Negative**.

#### Why it exists
- Every stored message is annotated with a sentiment label.
- These labels enable mood‑trend analysis, summary generation, and visualization of emotional shifts over time.

---

### 3️⃣ `trend_llm.py` — Emotional Trend Analyzer (LLM Classification)

#### What it does
- Builds a strict system prompt for the LLM to:
  - Read the full conversation (user and AI messages).
  - Understand emotional weight and transitions.
  - Output a single overall mood label (for example: *Mostly Positive*, *Neutral*, *Negative*).
- Sends the full conversation text to Groq LLaMA‑3.1.
- Returns only the final label with no explanation.

#### Why it exists
- VADER works at the per‑message level only.
- This LLM module interprets the overall emotional arc of the conversation, similar to how a human therapist would.

---

### 4️⃣ `trend_summary_llm.py` — Empathetic Mood Summary Generator

#### What it does
- Fetches all past messages and their sentiment labels.
- Prepares a summarization prompt that asks the LLM to:
  - Detect mood shifts.
  - Identify stress or tension points.
  - Highlight emotional highs and lows.
  - Produce a warm, human‑like summary under 100 words.
- Uses Groq LLaMA‑3.1 to generate the final emotional summary.

#### Why it exists
- `trend_llm.py` only outputs a label.
- This module provides a therapist‑style written recap of the user’s overall mood during the day or session.

---

### 5️⃣ `main.py` — FastAPI Backend (Core API Layer)

#### Endpoints

| Endpoint                | Purpose                                                                 |
|-------------------------|-------------------------------------------------------------------------|
| `POST /chat`            | Process user messages, generate replies, compute sentiment, save to DB |
| `GET /trend/{user_id}`  | Return the emotional trend label using the LLM                         |
| `GET /llm-summary/{user_id}` | Generate an empathetic emotional summary for the user             |
| `DELETE /reset/{user_id}`    | Clear chat history for that user from MongoDB                     |

#### What it does
- Initializes the FastAPI application.
- Enables CORS so the custom frontend can communicate with the backend.
- Defines request/response models using Pydantic.
- Stores all conversation messages in MongoDB.
- Wires together all components: chatbot, sentiment analyzer, trend LLM, and summary LLM.

#### Why it exists
- Acts as the central controller for:
  - Chatbot responses.
  - Sentiment analysis.
  - Mood classification.
  - Emotional summary generation.
  - MongoDB persistence.
- Effectively ties the entire application into a single cohesive backend.

## ▶️ How to Run  

### 1️⃣ Install dependencies  
pip install -r backend/requirements.txt


### 2️⃣ Start backend  
uvicorn app.main:app --reload

### 3️⃣ Open frontend  
Simply open the following file in your browser:  
frontend/index.html

✅ That’s it — your AI emotional companion is ready! ❤️  


---

## 📜 License  
This project is for **educational and personal use**.  

