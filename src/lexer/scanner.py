
"""
The scanner is responsible for identifying which words in the received text are tokens and 
which are not—treating ordinary words (non-tokens) as identifiers. Afterward, it stores the tokens in an array.
"""

from src.lexer.token import *
import jellyfish
import importlib.resources
from symspellpy import SymSpell, Verbosity

_SYM_SPELL_INSTANCE = SymSpell(max_dictionary_edit_distance=2, prefix_length=7)
_dict_ref = importlib.resources.files("symspellpy") / "frequency_dictionary_en_82_765.txt"

with importlib.resources.as_file(_dict_ref) as path:
    _SYM_SPELL_INSTANCE.load_dictionary(str(path), term_index=0, count_index=1)
#translate a string into a list of tokens
class Scanner:
    def __init__(self, text: str):
        self.text: str = text
        self.current: int = 0
        self.tokens: list[Token] = []
        self.sym_spell = _SYM_SPELL_INSTANCE

    def finished(self):
        return self.current >= len(self.text)

    def advance(self):
        self.current += 1
        return self.text[self.current - 1]

    # Checks if the received word is similar to an existing token
    def similar_sound(self, text: str):
        text_phonetic = jellyfish.nysiis(text)
        for tokens in TokenType:
            if jellyfish.nysiis(tokens.value) == text_phonetic:
                return tokens.value
        return text
    
    def text_correction(self, text: str):
        suggestion = self.sym_spell.lookup(text, Verbosity.TOP, max_edit_distance=2)
        return suggestion[0].term if suggestion else text
    
    def scan(self):
        while not self.finished():
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

            buffer = self.similar_sound(buffer)
        
            try:
                token_type = TokenType(self.text_correction(buffer))

            except ValueError:
                token_type = TokenType.IDENTIFIER

            self.tokens.append(Token(type=token_type, lexeme= self.text_correction(buffer)))