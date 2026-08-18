import subprocess


class Actions:
    def __init__(self):
        self.commands ={
            "open firefox": self.open_browser,
            "stop music": self.pause_music,
            "start music": self.start_music,
            "turn up the volume": self.up_volume,
            "turn down the volume": self.down_volume,
            "next music": self.next_music
        }

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

    def process(self, text):
        if text in self.commands:
            action = self.commands[text]
            action()