"""
Where it is defined which words will be tokens.
"""

from enum import StrEnum
from dataclasses import dataclass

#the actions tokens
class TokenType(StrEnum):
    OPEN = "open"
    CLOSE = "close"
    AND = "and"
    ONE = "one"
    PLAY = "play"
    SEARCH = "search"
    GEMINI = "gemini"
    STOP = "stop"
    START = "start"
    NEXT = "next"
    UPDATE = "update"
    UP = "up"
    DOWN = "down"
    VIEW = "view"
    CREATE = "create"
    IDENTIFIER = "identifier"
    TASK = "task"
    MUSIC = "music"

@dataclass
class Token:
    type: TokenType
    lexeme: str
    
