import json
import sys
import sounddevice as sd
from actions import *

comands_execute = Actions()
def start_listerning(q):
        def callback(indata, frames, time, status):
            if status:
                print(status, file=sys.stderr)
            q.put(bytes(indata))
                    
        try:
            with sd.RawInputStream(samplerate= 16000, blocksize= 8000, dtype= "int16", channels= 1, callback= callback):
                while True:
                    data = q.get()
        
                        
        
        except KeyboardInterrupt:
            print("The program is over")