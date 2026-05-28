from backend.analyzer import analyze_email_content
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class EmailRequest(BaseModel):
    email: str

@app.get("/")
def home():
    return {
        "message": "AI Phishing Detection API Running"
    }

@app.post("/analyze")
def analyze_email(request: EmailRequest):

    return analyze_email_content(request.email)