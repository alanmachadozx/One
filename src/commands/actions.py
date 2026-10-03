
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
        
    def process(self, intent:str, target:str):

        if intent == "VIEW_TASKS":
            view_tasks()
            _ = history_insert(intent, target)
            
        if intent == "ADD_TASK":
            time_remaining = ask_user(" Enter the time remaining")
            if time_remaining == "skip":
                time_remaining = None
                
            description = ask_user(" Enter the description")
            if description == "skip":
                description = None
                
            create_task(target, time_remaining, description)
            speech(f"Task {target} created.")
            _ = history_insert(intent, target)
            
        if intent == "view history":
            db_query()
            _ = history_insert(intent, target)
            
        if intent == "OPEN_APP":
            
            try:      
               subprocess.Popen([target])
               _ = history_insert(intent, target)
               
            except Exception:
                speech(f"{target} not found.")
                
            else:
                speech(f"Opened {target}.")

        if intent == "CLOSE_APP":
            try:
                subprocess.Popen(["kill", target])
                _ = history_insert(intent, target)
                
            except Exception:
                speech(f"{target} not found!")
            else:
                speech(f"Closed {target}.")

        if intent == "ASK_GEMINI":
            speech("Thinking")

            response = ask_gemini(target)
            print(response)
            _ = history_insert(intent, target)

        if intent == "SEARCH":
            formatted_content = urllib.parse.quote(target)
            url = f"https://www.google.com/search?q={formatted_content}"
            
            speech(f"Searching for {target}.")
            webbrowser.open(url)
            _ = history_insert(intent, target)

        if intent == "PLAY_MUSIC":
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
                            print("Music not found!")
            except Exception:
                print("Failed to communicate with Spotify")

        if intent == "UPDATE":
            subprocess.Popen(["sudo", "pacman", "-Syu"])
            _ = history_insert(intent, target)
            speech("Update started.")
        
        if intent == "NEXT_MUSIC":
            subprocess.Popen(["playerctl", "next"])
            _ = history_insert(intent, target)

        if intent == "UP_VOL":
            subprocess.Popen(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%+"])
            _ = history_insert(intent, target)

        if intent == "DOWN_VOL" and target == "volume":
            subprocess.Popen(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%-"])
            _ = history_insert(intent, target)

        if intent == "STOP_MUSIC":
            subprocess.Popen(["playerctl", "stop"])
            _ = history_insert(intent, target)

        if intent == "start music":
            subprocess.Popen(["playerctl", "play"])
            _ = history_insert(intent, target)
