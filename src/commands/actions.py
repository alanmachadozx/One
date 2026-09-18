from cmath import e
from http.client import responses
import subprocess
import webbrowser
from src.commands.apis import *
import urllib.parse
import pyttsx3

#for the response voice
engine = pyttsx3.init()
engine.setProperty('rate', 150)

class Actions:
    def __init__(self):
       self.common_targets = [
           
       ]
        
    def process(self, action:str, target:str):

        if action == "open":
            try:
               subprocess.Popen([target])
            except Exception:
                print(f"{target} not found!")
                engine.say(f"{target} not found.")
                engine.runAndWait()
            else:
                engine.say(f"Opened {target}.")
                engine.runAndWait()
                
        if action == "close":
            try:
                subprocess.Popen(["kill", target])
                
            except Exception:
                print(f"{target} not found!")
                engine.say(f"{target} not found!")
                engine.runAndWait()
            else:
                engine.say(f"Closed {target}.")
                engine.runAndWait()

        if action == "gemini":
            engine.say("Thinking")
            engine.runAndWait()

            response = ask_gemini(target)
            print(response)
        
        if action == "search":
            formatted_content = urllib.parse.quote(target)
            url = f"https://www.google.com/search?q={formatted_content}"
            
            engine.say(f"Searching for {target}.")
            engine.runAndWait()
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
                            engine.say(f"Playing {target}.")
                            engine.runAndWait()
        
                        else:
                            print("Music not found!")
            except Exception:
                print("Failed to communicate with Spotify")

        if action == "update":
            subprocess.Popen(["sudo", "pacman", "-Syu"])
            
            engine.say("Update completed.")
            engine.runAndWait()
        
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
