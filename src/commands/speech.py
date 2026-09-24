from gtts import gTTS
import os
import subprocess
from faster_whisper import WhisperModel
import queue

q = queue.Queue()
model = WhisperModel("small", device= "cpu", compute_type= "int8")

#Função para voz de resposta a comandos
def speech(text: str):
    tts = gTTS(text = text, lang ='en')
    tts.save("speech.mp3")

    subprocess.run(
        ["ffplay", "-nodisp", "-autoexit", "speech.mp3"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
        
    if os.path.exists("speech.mp3"):
        os.remove("speech.mp3")

def transcribe_audio(audio):
    segments, _ = model.transcribe(audio, condition_on_previous_text=False, 
    no_speech_threshold=0.5, vad_filter=False, initial_prompt="search")
    text = None
    
    for segment in segments:
        clean_text = segment.text.strip().replace(".", "").replace(",", "").lower()
        print(clean_text)
        text = segment.text.strip()

    return text


def ask_user(ask: str) -> str:
    speech(ask)

    #Your code's thread "locks" the queue. If the microphone tries to send a new audio block (q.put()) at that exact millisecond, it ends up waiting outside.
    with q.mutex:   
        q.queue.clear()  #clear the queue

    while True:
        audio_chunk = q.get()
        text = transcribe_audio(audio_chunk)
        if text:
            return text.lower().strip().replace(".", "").replace(",", "")
        