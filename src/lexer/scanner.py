class Scanner:
    def __init__(self, text):
        self.text = text
        self.current = 0
        self.start = 0
        self.line = 1
        self.tokens = []

        def finished(self):
            return self.current >= len(self.text)

        def advance(self):
            self.current += 1
            return self.text[self.current - 1]

        def previous(self):
            return self.text[self.current - 1]

        def peek(self):
            if self.finished():
                return '\0'
            return self.text[self.current]

        def peek_next(self):
            if self.current + 1 >= len(self.text):
                return '\0'
            return self.text[self.current + 1]

        def scan(self):
            while not self.finished():
                self.start = self.current
                

                