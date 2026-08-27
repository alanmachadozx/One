import subprocess
from spotify_cliente import *

class Actions:
    def __init__(self):
        self.commands ={
            "open firefox": self.open_browser,
            "stop music": self.pause_music,
            "start music": self.start_music,
            "turn up the volume": self.up_volume,
            "turn down the volume": self.down_volume,
            "next music": self.next_music,
        }
        
        
    def process(self, text):
        if text in self.commands:
            action = self.commands[text]
            action()

    def play_music(self, text:str):
        if "play" in text:
            music_name = text.replace("play", "").strip
            result = sp.search(q= music_name, limit= 1, type="track")
        
            if result:
                tracks = result["tracks"]["items"]

                if tracks:
                    music_uri = tracks[0]["uri"] #select the first track and your uri
                    sp.start_playback(uris =[music_uri])

                else:
                    print("Music not found!")
             
         
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

    def open_browser(self):
        subprocess.Popen(["firefox"])