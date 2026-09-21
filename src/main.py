
from src.listener import *
import slint
import sys
import os

path = os.path.dirname(os.path.abspath(__file__))
slint_path = os.path.join(path, '..', 'front-end', 'app-window.slint')

#load the ui
ui = slint.load_file(slint_path)

app = ui.MainWindow()
app.run()

start_listerning()