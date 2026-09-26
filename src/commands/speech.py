from gtts import gTTS
import os
import subprocess
from faster_whisper import WhisperModel
import queue
import contextlib
import src.state as state
import time

model = WhisperModel("small.en", device= "cpu", compute_type= "int8")

#Função para voz de resposta a comandos
def speech(text: str):
    tts = gTTS(text = text, lang ='en')
    tts.save("speech.mp3")

    _ = subprocess.run(
        ["ffplay", "-nodisp", "-autoexit", "speech.mp3"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        check = False
    )
        
    if os.path.exists("speech.mp3"):
        os.remove("speech.mp3")

    time.sleep(0.4)

def transcribe_audio(audio):
    segments, _ = model.transcribe(audio, condition_on_previous_text=False, 
    no_speech_threshold=0.5, vad_filter=False)
    text = None
    
    for segment in segments:
        clean_text = segment.text.strip().replace(".", "").replace(",", "").lower()
        print(clean_text)
        text = segment.text.strip()

    return text

@contextlib.contextmanager
def limited_hear():
    #clear the queue
    while not state.q.empty():
        try:    
            state.q.get_nowait()
        except queue.Empty:
            pass
            
    state.is_processing = False
    try:
        yield
    finally:
        state.is_processing = True

def ask_user(ask: str) -> str:
    speech(ask)

    with limited_hear():
        while True:
            try:
                audio_chunk = state.q.get(timeout=0.5)
            except queue.Empty:
                continue

            text = transcribe_audio(audio_chunk)
            if text:
                 return text.lower().strip().replace(".", "").replace(",", "")

