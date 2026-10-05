
"""
This is where the link between identifying the command and executing the action occurs.
"""

import subprocess
import webbrowser
from src.commands.apis import *
import urllib.parse
from src.audio.speech import *
from database.db import * 


class Actions:
    def __init__(self):
        self.router = {
            "VIEW_TASKS": self.view_task,
            "ADD_TASK": self.add_task,
            "VIEW_HISTORY": self.view_history,
            "OPEN_APP": self.open_app,
            "CLOSE_APP": self.close_app,
            "SEARCH": self.search,
            "ASK_GEMINI": self.ask_gemini,
            "PLAY_MUSIC": self.play_music,
            "UPDATE": self.update,
            "NEXT_MUSIC": self.next_music,
            "UP_VOL": self.up_vol,
            "DOWN_VOL": self.down_vol,
            "STOP_MUSIC": self.stop_music,
            "RESUME_MUSIC": self.resume_music,
        }

        
    def process(self, intent:str, target:str):
        if intent in self.router:
            action = self.router[intent]
            action(intent, target)

    def view_task(self, intent: str, target: str):
        view_tasks()
        _ = history_insert(intent, target)

    def add_task(self, intent: str, target: str):
        time_remaining = ask_user(" Enter the time remaining")
        if time_remaining == "skip":
            time_remaining = None
            
        description = ask_user(" Enter the description")
        if description == "skip":
            description = None
            
        create_task(target, time_remaining, description)
        speech(f"Task {target} created.")
        _ = history_insert(intent, target)

    def view_history(self, intent: str, target: str):
        db_query()
        _ = history_insert(intent, target)

    def search(self, intent: str, target: str):
        formatted_content = urllib.parse.quote(target)
        url = f"https://www.google.com/search?q={formatted_content}"
        
        speech(f"Searching for {target}.")
        webbrowser.open(url)
        _ = history_insert(intent, target)

    def open_app(self, intent: str, target: str):
        try:      
           subprocess.Popen([target])
           _ = history_insert(intent, target)
           
        except Exception:
            speech(f"{target} not found.")
            
        else:
            speech(f"Opened {target}.")

    def close_app(self, intent: str, target: str):
        try:
            subprocess.Popen(["kill", target])
            _ = history_insert(intent, target)
            
        except Exception:
            speech(f"{target} not found!")
        else:
            speech(f"Closed {target}.")

    def ask_gemini(self, intent: str, target: str):
        speech("Thinking")

        response = ask_gemini(target)
        print(response)
        _ = history_insert(intent, target)

    def play_music(self, intent: str, target: str):
        subprocess.Popen(["spotify-launcher"])

        #Captures the "play music-name" command and searches for the specific song on Spotify
        #You need Spotify for Developers and spotify-launcher.
        try:
            if target:
                result = sp.search(q=target, limit= 1, type="track")

                if result:
                    tracks = result.get("tracks", {}).get("items", [])
    
                    if tracks:
                        music_uri = tracks[0]["uri"] #select the first track and your uri
                        sp.start_playback(uris = [music_uri])
                        speech(f"Playing {target}.")
                        _ = history_insert(intent, target)

                    else:
                        speech("Music not found!")
        except Exception:
            speech("Failed to communicate with Spotify")

    def update(self, intent: str, target: str):
        subprocess.Popen(["sudo", "pacman", "-Syu"])
        _ = history_insert(intent, target)
        speech("Update started.")

    def next_music(self, intent: str, target: str):
        subprocess.Popen(["playerctl", "next"])
        _ = history_insert(intent, target)

    def up_vol(self, intent: str, target: str):
        subprocess.Popen(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%+"])
        _ = history_insert(intent, target)

    def down_vol(self, intent: str, target: str):
        subprocess.Popen(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%-"])
        _ = history_insert(intent, target)

    def stop_music(self, intent: str, target: str):
        subprocess.Popen(["playerctl", "stop"])
        _ = history_insert(intent, target)

    def resume_music(self, intent: str, target: str):
        subprocess.Popen(["playerctl", "play"])
        _ = history_insert(intent, target)

    