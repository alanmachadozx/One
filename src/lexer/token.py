from enum import StrEnum
from dataclasses import dataclass

#the actions tokens
class TokenType(StrEnum):
    OPEN = "open"
    CLOSE = "close"
    AND = "and"
    ONE = "one"
    THE = "the"
    PLAY = "play"
    SEARCH = "search"
    FOR = "for"
    GEMINI = "gemini"
    STOP = "stop music"
    START = "start music"
    NEXT = "next music"
    UPDATE = "update"
    UP = "up volume"
    DOWN = "down volume"
    IDENTIFIER = "identifier"

@dataclass
class Token:
    type: TokenType
    lexeme: str
    
