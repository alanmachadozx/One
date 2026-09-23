
from src.listener import *
import slint
import sys
import os
import threading

path = os.path.dirname(os.path.abspath(__file__))
slint_path = os.path.join(path, '..', 'front-end', 'app-window.slint')

#load the ui
ui = slint.load_file(slint_path)
app = ui.MainWindow()

def background_thread():
    linstener = threading.Thread(target=start_listerning)
    linstener.daemon = True
    linstener.start()

app.start_program = background_thread
app.run()

