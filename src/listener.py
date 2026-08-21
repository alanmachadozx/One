import json
import sys
import sounddevice as sd
from actions import *

comands_execute = Actions()
def start_listerning(q, samplerate, duration):

    def audio_record():
        print("Recordinng...")
        with sd.InputStream(samplerate= samplerate, channels= 1, dtype = "float32") as stream:
            # return a tuple with 2 elements, read(data, overflowed), the [0] is used for select just data
            audio = stream.read(int(samplerate * duration))[0]
         
        sd.wait()
        #converts the two-dimensional(2D) audio matrix into a one-dimensional (1D) vector
        # the faster-whisper library requires this format
        return audio.flatten()