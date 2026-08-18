import subprocess


class Actions:
    def __init__(self):
        self.commands ={
            "open firefox": self.open_browser
        }

    def open_browser(self):
        subprocess.Popen(["firefox"])

    def process(self, text):
        if text in self.commands:
            action = self.commands[text]
            action()