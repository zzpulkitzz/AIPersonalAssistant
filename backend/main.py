from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from base import Base   
import os
import schemas
from dotenv import load_dotenv
from google import genai
import asyncio
from tts import speak
Base.metadata.create_all(bind=engine)
from stt import record_to_mp3, transcribe
app = FastAPI()

load_dotenv()

gemini_client = genai.Client(api_key=os.getenv("GOOGLE_API_KEY"))

def print_available_tools(tools):
    print("Available tools:", [t.name for t in tools.tools])

async def call_gemini(query: str):

    
        response = await gemini_client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=query,
                config=genai.types.GenerateContentConfig(
                    temperature=0
                )
            )
        speak(response.text)
        return response.text

async def handleQuery(query: str):
    await call_gemini(query)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



record_to_mp3("mic_recording.mp3", duration=5)
query=transcribe("mic_recording.mp3")
asyncio.run(handleQuery(query))
# Example endpoint
@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
