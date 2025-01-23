import os
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY")  
)


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5003", "http://13.38.245.166"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class CommitRequest(BaseModel):
    prompt: str

@app.post("/generate-commit")
async def generate_commit(request: CommitRequest):
    try:
      
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a helpful assistant that generates concise git commit messages."},
                {"role": "user", "content": f"Generate a git commit message for: {request.prompt}"},
            ],
            model="gpt-4",
        )
       
        commit_message = response.choices[0].message.content.strip()
        return {"commit_message": commit_message}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating commit: {str(e)}")
