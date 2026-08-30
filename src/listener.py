import sounddevice as sd
from actions import *
import numpy as np
from faster_whisper import WhisperModel
import webrtcvad
import queue

comands_execute = Actions()
vad = webrtcvad.Vad(3) #set aggressiveness mode, where 3 is the most agressive
q = queue.Queue()

SAMPLERATE = 16000
FRAMEDURATION = 30 #ms
FRAME_SIZE = int(SAMPLERATE * FRAMEDURATION/ 1000)

model = WhisperModel("tiny.en", device= "cpu", compute_type= "int8")

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
              final_audio = np.concatenate(buffer)
              q.put(final_audio)
              
              buffer.clear()
              is_recording = False
              offtime = 0
              
def transcribe_audio(audio):
    segments, _ = model.transcribe(audio, language= "en")
    text = None
    
    for segment in segments:
        print(f"{segment.text.strip()}")
        text = segment.text.strip()

    return text

def start_listerning():
    print("Recordinng...")
    with sd.InputStream(samplerate= SAMPLERATE, channels= 1, dtype = "float32", callback= callback, blocksize= FRAME_SIZE):

        try:
            while True:
                audio_chunk = q.get()  
                text = transcribe_audio(audio_chunk)
    
                if text:
                    formatted_text = (text.lower().strip().replace(".", "").replace(",", ""))
                    comands_execute.process(formatted_text)
    
        except KeyboardInterrupt:
            print("program finished")