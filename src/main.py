import queue
from  listener import *
import webrtcvad

q = queue.Queue()
SAMPLERATE = 16000
DURATION = 5
FRAMEDURATION = 30 #ms
FRAME_SIZE = int(SAMPLERATE * FRAMEDURATION/ 1000)

vad = webrtcvad.Vad(3) #set aggressiveness mode, where 3 is the most agressive
model = WhisperModel("tiny.en", device= "cpu", compute_type= "int8")

start_listerning(q, SAMPLERATE, DURATION, FRAME_SIZE, vad, model)