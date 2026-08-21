import json
import sys
import sounddevice as sd
from actions import *
import numpy as np
from faster_whisper import WhisperModel

comands_execute = Actions()
def start_listerning(q, samplerate, duration, frame_size, vad, model):

    def audio_record():
        print("Recordinng...")
        with sd.InputStream(samplerate= samplerate, channels= 1, dtype = "float32") as stream:
            # return a tuple with 2 elements, read(data, overflowed), the [0] is used for select just data
            audio = stream.read(int(samplerate * duration))[0]
         
        sd.wait()
        #converts the two-dimensional(2D) audio matrix into a one-dimensional (1D) vector
        # the faster-whisper library requires this format
        return audio.flatten()

    def contains_speech(audio):
        pcm = (audio * 32768).astype(np.int16).tobytes()

        for i in range(0, len(pcm), frame_size * 2):
            frame = pcm[i: i + frame_size * 2]

            if len(frame) < frame_size * 2:
                break

            if vad.is_speech(frame, samplerate):
                return True

        return False

    def transcribe_audio(audio):
        segments, _ = model.transcribe(audio, language= "en")
        text = None
        
        for segment in segments:
            print(f"{segment.text.strip()}")
            text = segment.text.strip()

        return text

    try:
        while True:
            if contains_speech(audio_record()):
                text = transcribe_audio(audio_record())
                comands_execute.process(text)

    except KeyboardInterrupt:
        print("program finished")