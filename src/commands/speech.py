from gtts import gTTS
import os
import subprocess

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