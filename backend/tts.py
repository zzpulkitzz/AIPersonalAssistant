import base64
from dotenv import load_dotenv
from openai import OpenAI
import os
from pathlib import Path
import sounddevice as sd
load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


speech_file_path = Path(__file__).parent / "speech.mp3"
def speak(text):
    with client.audio.speech.with_streaming_response.create(
        model="gpt-4o-mini-tts",
        voice="coral",
        input=text,
        instructions="Speak in a cheerful and positive tone.",
    ) as response:
        response.stream_to_file(speech_file_path)