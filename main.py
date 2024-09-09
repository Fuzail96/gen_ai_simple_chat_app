from google import generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
import argparse
import uvicorn

parser = argparse.ArgumentParser()
parser.add_argument("--google_genai_api_key", help="openai api key to be used")
args = parser.parse_args()

app = FastAPI()

class ChatHistory(BaseModel):
    role: str
    parts: str

class Query(BaseModel):
    question: str
    history: list[ChatHistory]
    
genai.configure(api_key=args.google_genai_api_key)

@app.post("/ask")
async def ask_question(query: Query):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        chat = model.start_chat(
            history=[history.dict() for history in query.history]
        )
        response = await chat.send_message_async(query.question)
        answer = response.text.strip()
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=(e))
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)