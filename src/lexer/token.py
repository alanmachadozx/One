"""
Where it is defined which words will be tokens.
"""

from enum import StrEnum
from dataclasses import dataclass

#the actions tokens
class TokenType(StrEnum):
    AND = "and"
    IDENTIFIER = "identifier"

@dataclass
class Token:
    type: TokenType
    lexeme: str
    
