from fastapi import FastAPI, Depends,Request
from fastapi.responses import Response
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models
from twilio.rest import Client
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

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_NUMBER = os.getenv("TWILIO_NUMBER")
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

async def call_gemini(query: str):

    
        response = await gemini_client.aio.models.generate_content(
                model="gemini-2.5-flash",
                contents=query,
                config=genai.types.GenerateContentConfig(
                    temperature=0
                )
            )
        print(response.text)
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



""" @app.on_event("startup")
async def startup_event():
    record_to_mp3("mic_recording.mp3", duration=5)
    query = transcribe("mic_recording.mp3")
    print(query)
    await handleQuery(query) """
# Example endpoint
@app.post("/call-user")
def call_user():
    call = client.calls.create(
        to="+918126293202",
        from_=TWILIO_NUMBER,
        twiml="<Response><Say>What is your task status?</Say><Record action='/twilio/process' maxLength='10' transcribe='true'/></Response>"
        
    )
    return {"status": "initiated", "call_sid": call.sid}


@app.post("/twilio/voice")
async def twilio_voice():
    # Play prompt and ask for speech input
    twiml = """
    <Response>
      <Say>What is your task status?</Say>
      <Record action="/twilio/process" maxLength="10" transcribe="true"/>
    </Response>
    """
    return Response(content=twiml, media_type="application/xml")

@app.post("/twilio/process")
async def process_recording(request: Request):
    # Handle recording, call your LLM/logic, return another <Say> or redirect
    recording_url = (await request.form())["RecordingUrl"]
    # Download/Transcribe/Process recording here
    answer = "Thanks, your response is saved."
    twiml = f"""
    <Response>
      <Say>{answer}</Say>
      <Hangup/>
    </Response>
    """
    return Response(content=twiml, media_type="application/xml")

@app.post("/users/")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
