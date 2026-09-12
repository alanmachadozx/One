from cmath import e
from http.client import responses
import subprocess
import webbrowser
from apis import *
import urllib.parse
import pyttsx3

#for the response voice
engine = pyttsx3.init()
engine.setProperty('rate', 150)

class Actions:
    def __init__(self):
        self.commands ={
            "stop music": self.pause_music,
            "start music": self.start_music,
            "up the volume": self.up_volume,
            "down the volume": self.down_volume,
            "next music": self.next_music,
            "update system": self.system_update
        }
        
        
    def process(self, text):
        self.open_program(text)
        self.close_program(text)
        self.play_music(text)
        self.web_search(text)
        self.gemini_search(text)
        if text in self.commands:
            action = self.commands[text]
            action()

    def gemini_search(self, text:str):
        if "gemini" in text:
            engine.say("Thinking")
            engine.runAndWait()
            
            content = text.replace("gemini", "").strip()
            responses = ask_gemini(content)
            print(responses)
            
    def web_search(self, text:str):
        if "search for" in text:
            content = text.replace("search for", "").strip()
            formatted_content = urllib.parse.quote(content)
            url = f"https://www.google.com/search?q={formatted_content}"

            engine.say(f"Searching for {content}.")
            engine.runAndWait()
            webbrowser.open(url)

    #captures the "play music-name" command and searches for the specific song on Spotify
    # You need Spotify for Developers and spotify-launcher.
    def play_music(self, text:str):
        if "play" in text:
            subprocess.Popen(["spotify-launcher"])
            music_name = text.replace("play", "", 1).strip()
            try:
                if music_name:
                    result = sp.search(q= music_name, limit= 1, type="track")
    
                    if result:
                        tracks = result.get("tracks", {}).get("items", [])
        
                        if tracks:
                            music_uri = tracks[0]["uri"] #select the first track and your uri
                            sp.start_playback(uris =[music_uri])
                            engine.say(f"Playing {music_name}.")
                            engine.runAndWait()
        
                        else:
                            print("Music not found!")
            except Exception:
                print("Failed to communicate with Spotify")

    def open_program(self, text:str):
        if "open" in text:
            program = text.replace("open", "").strip()

            try:
               subprocess.Popen([program])
            except Exception:
                print(f"Failed to open {program}")
                engine.say(f"Failed to open {program}.")
                engine.runAndWait()
            else:
                engine.say(f"Opened {program}.")
                engine.runAndWait()

    def close_program(self, text: str):
        if "close" in text:
            program = text.replace("close", "").strip()
            subprocess.Popen(["kill", program])
            
            engine.say(f"Closed {program}.")
            engine.runAndWait()

    def system_update(self):
        subprocess.Popen(["sudo", "pacman", "-Syu"])
        engine.say("Update completed.")
        engine.runAndWait()
        
        
    def next_music(self):
        subprocess.Popen(["playerctl", "next"])
        
    def up_volume(self):
        subprocess.Popen(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%+"])
        
    def down_volume(self):
        subprocess.Popen(["wpctl", "set-volume", "@DEFAULT_AUDIO_SINK@", "5%-"])

    def start_music(self):
        subprocess.Popen(["playerctl", "play"])
        
    def pause_music(self):
        subprocess.Popen(["playerctl", "play-pause"])
