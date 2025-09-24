import base64
from dotenv import load_dotenv
from openai import OpenAI
import os
from pathlib import Path
import sounddevice as sd
load_dotenv()
print(os.environ.get("OPENAI_API_KEY"))
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


speech_file_path = Path(__file__).parent / "speech.mp3"

with client.audio.speech.with_streaming_response.create(
    model="gpt-4o-mini-tts",
    voice="coral",
    input="Today is a wonderful day to build something people love!",
    instructions="Speak in a cheerful and positive tone.",
) as response:
    with sd.OutputStream(samplerate=24000, channels=1, dtype="int16") as stream:
        for chunk in response.iter_bytes(chunk_size=4096):
            stream.write(chunk)