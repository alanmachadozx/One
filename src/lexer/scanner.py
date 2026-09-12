class Scanner:
    def __init__(self, text):
        self.text = text
        self.current = 0
        self.start = 0
        self.line = 1
        self.tokens = []