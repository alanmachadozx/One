import json
import sys
import sounddevice as sd
from actions import *
from thefuzz import fuzz

def start_listening( rec, samplerate, q):
        def callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))
            
        try:
            with sd.RawInputStream(samplerate= samplerate, blocksize= 8000, dtype= "int16", channels= 1, callback= callback):
                while True:
                    data = q.get()
            
                    if rec.AcceptWaveform(data): #return true if your voice stop
                        result = json.loads(rec.Result())
                        text = result.get("text", "") #return the key value or a empty string

                        if text:
                            print(text)
        
        except KeyboardInterrupt:
            print("The program is over")