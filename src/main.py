import queue
import sounddevice as sd
from  listener import *
from faster_whisper import WhisperModel

q = queue.Queue()

model = WhisperModel("tiny.en", device= "cpu", compute_type= "int8")
segments = model.transcribe("test.wav", language= "en")

start_listerning(q)