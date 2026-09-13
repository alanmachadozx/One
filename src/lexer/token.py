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
    STOP = "stop"
    START = "start"
    UPDATE = "update"
    UP = "up"
    DOWN = "down"
    VOLUME = "volume"
    IDENTIFIER = "identifier"

@dataclass
class Token:
    type: TokenType
    lexeme: str
    
