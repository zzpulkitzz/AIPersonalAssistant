import sounddevice as sd
import numpy as np
from pydub import AudioSegment
from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
# Record audio from mic
def record_to_mp3(filename="output.mp3", duration=5, samplerate=44100):
    print("Recording...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype="int16")
    sd.wait()  # wait until recording is finished
    print("Recording finished.")

    # Convert numpy array -> AudioSegment
    audio_segment = AudioSegment(
        audio_data.tobytes(),
        frame_rate=samplerate,
        sample_width=audio_data.dtype.itemsize,
        channels=1
    )

    # Export as MP3 (requires ffmpeg installed)
    audio_segment.export(filename, format="mp3")
    print(f"Saved recording as {filename}")


def transcribe(filename="mic_recording.mp3"):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    audio_file= open(filename, "rb")

    transcription = client.audio.transcriptions.create(
        model="gpt-4o-transcribe", 
        file=audio_file
    )
    print(transcription.text)
    return transcription.text



