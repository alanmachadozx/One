import unittest
from src.lexer.scanner import *
from src.lexer.token import *

class TestLexer(unittest.TestCase):
    
    def test_similarity(self):                                                    #An indentifier exemple
        similar_texts = ["opening", "closing", "starting", "playing", "isthat"]
        for text in similar_texts:
            scanner = Scanner(text)
            scanner.scan()
            tokens = scanner.tokens[0]

            if tokens.type == TokenType.IDENTIFIER:
                print(f"Token is not an action:\n Type: {tokens.type} \n Lexeme: {tokens.lexeme}")
            else:
                print(f"token is a action:\n Type: {tokens.type} \n Lexeme: {tokens.lexeme}")
        

if __name__ == '__main__':
    unittest.main()
        