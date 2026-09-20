import subprocess
import webbrowser
from src.commands.apis import *
import urllib.parse
from src.commands.speech import *
from database.db import * 


class Actions:
        
    def process(self, action:str, target:str):
        if action == "create task":
            time_remaining = ask_user(" Enter the time remaining")
            if time_remaining == "skip":
                time_remaining = None
                
            description = ask_user(" Enter the description")
            if description == "skip":
                description = None
                
            create_task(target, time_remaining, description)
            speech(f"Task {target} created.")
            
            
        if action == "view" and target == "history":
            db_query()
            _ = history_insert(action, target)
            
        if action == "open":
            
            try:      
               subprocess.Popen([target])
               _ = history_insert(action, target)
               
            except Exception:
                print(f"{target} not found!")
                speech(f"{target} not found.")
                
            else:
                speech(f"Opened {target}.")

        if action == "close":
            try:
                subprocess.Popen(["kill", target])
                _ = history_insert(action, target)
                
            except Exception:
                print(f"{target} not found!")
                speech(f"{target} not found!")
            else:
                speech(f"Closed {target}.")

        if action == "gemini":
            speech("Thinking")

            response = ask_gemini(target)
            print(response)
            _ = history_insert(action, target)
        
        if action == "search":
            formatted_content = urllib.parse.quote(target)
            url = f"https://www.google.com/search?q={formatted_content}"
            
            speech(f"Searching for {target}.")
            webbrowser.open(url)
            _ = history_insert(action, target)

        if action == "play":
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
                            _ = history_insert(action, target)

                        else:
                            print("Music not found!")
            except Exception:
                print("Failed to communicate with Spotify")

        if action == "update":
            subprocess.Popen(["sudo", "pacman", "-Syu"])
            _ = history_insert(action, target)
            speech("Update started.")
        
        if action == "next" and target == "music":
            subprocess.Popen(["playerctl", "next"])
            _ = history_insert(action, target)

        if action == "up" and target == "volume":
            subprocess.Popen(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%+"])
            _ = history_insert(action, target)

        if action == "down" and target == "volume":
            subprocess.Popen(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%-"])
            _ = history_insert(action, target)

        if action == "stop" and target == "music":
            subprocess.Popen(["playerctl", "stop"])
            _ = history_insert(action, target)

        if action == "start" and target == "music":
            subprocess.Popen(["playerctl", "play"])
            _ = history_insert(action, target)
