import queue
from vosk import Model, KaldiRecognizer
import sounddevice as sd
from  listener import *

q = queue.Queue()

try:
    model = Model("src/model")
except Exception: 
    print("Model folder not found!")
    sys.exit(1)

#looks for the default linux microphone settings
device_info = sd.query_devices(None, "input") 
rec = KaldiRecognizer(model, 16000)

start_listening(rec, 16000, q)