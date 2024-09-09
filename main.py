from google import generativeai as genai
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import argparse
import uvicorn

parser = argparse.ArgumentParser()
parser.add_argument("--google_genai_api_key", help="openai api key to be used")
args = parser.parse_args()

app = FastAPI()

class Query(BaseModel):
    question: str

genai.configure(api_key=args.google_genai_api_key)

@app.post("/ask")
async def ask_question(query: Query):
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = await model.generate_content_async(query.question)
        answer = response.text.strip()
        return {"answer": answer}
    except Exception as e:
        raise HTTPException(status_code=500, detail=(e))
    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)