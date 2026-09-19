import subprocess
import webbrowser
from src.commands.apis import *
import urllib.parse
from src.commands.speech import speech

class Actions:
        
    def process(self, action:str, target:str):

        if action == "open":
            try:
                
               subprocess.Popen([target])
            except Exception:
                print(f"{target} not found!")
                speech(f"{target} not found.")
            else:
                speech(f"Opened {target}.")

        if action == "close":
            try:
                subprocess.Popen(["kill", target])
                
            except Exception:
                print(f"{target} not found!")
                speech(f"{target} not found!")
            else:
                speech(f"Closed {target}.")

        if action == "gemini":
            speech("Thinking")

            response = ask_gemini(target)
            print(response)
        
        if action == "search":
            formatted_content = urllib.parse.quote(target)
            url = f"https://www.google.com/search?q={formatted_content}"
            
            speech(f"Searching for {target}.")
            webbrowser.open(url)

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

                        else:
                            print("Music not found!")
            except Exception:
                print("Failed to communicate with Spotify")

        if action == "update":
            subprocess.Popen(["sudo", "pacman", "-Syu"])
            
            speech("Update completed.")
        
        if action == "next music":
            subprocess.Popen(["playerctl", "next"])

        if action == "up volume":
            subprocess.Popen(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%+"])

        if action == "down volume":
            subprocess.Popen(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%-"])

        if action == "stop music":
            subprocess.Popen(["playerctl", "stop"])

        if action == "start music":
            subprocess.Popen(["playerctl", "play"])
