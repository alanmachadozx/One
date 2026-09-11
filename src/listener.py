import sounddevice as sd
from actions import *
import numpy as np
from faster_whisper import WhisperModel
import webrtcvad
import queue
import time

comands_execute = Actions()
vad = webrtcvad.Vad(3) #set aggressiveness mode, where 3 is the most agressive
q = queue.Queue()

SAMPLERATE = 16000
FRAMEDURATION = 30 #ms
FRAME_SIZE = int(SAMPLERATE * FRAMEDURATION/ 1000)

model = WhisperModel("small", device= "cpu", compute_type= "int8")

buffer = []
is_recording = False
offtime = 0

#the callback function, called by the inputStream
def callback(indata, frames, time, status):
    global buffer, is_recording, offtime
    
    if status:
        print(status)

    clear_indata = indata[:, 0]
    clear_bytes = (clear_indata * 32768).astype(np.int16).tobytes()

    if vad.is_speech(clear_bytes,SAMPLERATE):
        is_recording = True
        offtime = 0
        buffer.append(clear_indata.copy())
        
    else:
        if is_recording:
            buffer.append(clear_indata.copy())
            offtime += 1
            
            if offtime > 15:
              if len(buffer) > 30: 
                final_audio = np.concatenate(buffer)
                q.put(final_audio)
                    
              buffer.clear()
              is_recording = False
              offtime = 0
              
def transcribe_audio(audio):
    segments, _ = model.transcribe(audio, condition_on_previous_text=False, 
    no_speech_threshold=0.5, vad_filter=True, initial_prompt="search")
    text = None
    
    for segment in segments:
        print(f"{segment.text.strip().replace(".", "").replace(",", "").lower()}")
        text = segment.text.strip()

    return text

def start_listerning():
    engine.say("Hello! One has started.")
    engine.runAndWait()
    time.sleep(2)
    
    with sd.InputStream(samplerate= SAMPLERATE, channels= 1, dtype = "float32", callback= callback, blocksize= FRAME_SIZE):

        try:
            while True:
                audio_chunk = q.get()  
                text = transcribe_audio(audio_chunk)
    
                if text:
                    formatted_text = text.lower().strip().replace(".", "").replace(",", "")
                    comands_execute.process(formatted_text)
    
        except KeyboardInterrupt:
            engine.say("Program finished.")
            engine.runAndWait()