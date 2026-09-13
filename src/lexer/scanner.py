from lexer.token import *

class Scanner:
    def __init__(self, text: str):
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
            
        def peek_next(self):
            if self.current + 1 >= len(self.text):
                return '\0'
            return self.text[self.current + 1]

        def scan(self):
            while not self.finished():
                self.start = self.current
                self.scan_single_token()
                
        def scan_single_token(self):
            c = self.advance() 

            if not c.isspace():
                buffer = ""

                while not c.isspace():
                    buffer += c

                    if self.finished():
                        break
                    c = self.advance()

                try:
                    token_type = TokenType(buffer)

                except ValueError:
                    token_type = TokenType.IDENTIFIER

                self.tokens.append(Token(type= token_type, lexeme= buffer))