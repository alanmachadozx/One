
"""
The parser is where the distinction is made between elements conveying an intended action and those that merely complement the sentence 
(such as *and*, *in*, *to*, *on*). Furthermore, the command is separated into a target and an action.
"""

from src.lexer.token import Token, TokenType
from src.commands.registry import registry_commands
from src.classifier.model import *

class CommandExpr:
        pass

class SingleAction(CommandExpr):
    def __init__(self, intent: str | None, target: str):
        self.target: str = target
        self.intent: str | None = intent

class SequenceAction(CommandExpr):
    def __init__(self, left: CommandExpr, operator: str, right: CommandExpr):
        self.left: CommandExpr = left
        self.operator: str = operator
        self.right: CommandExpr = right

class Parser:
    def __init__(self, tokens: list[Token], intent: str | None):
        self.tokens: list[Token] = tokens
        self.current_token: int = 0
        self.intent: str | None = intent

    def peek(self) -> Token:
        return self.tokens[self.current_token]
    
    def advance(self):
        self.current_token += 1

    def previous(self) -> Token:
        return self.tokens[self.current_token - 1]
        
    #Is similar to match, but does not advance the token if it does not match
    def check(self, token_type: str) -> bool:
        if self.current_token >= len(self.tokens):
            return False
        return self.peek().type == token_type

    # if the current token matches the given type, advance and return True, otherwise return False
    def match(self, token_type: str) -> bool:
        if self.check(token_type):
            self.advance()
            return True
        return False

    # Clears the buffer, removing any words that should be ignored
    # based on the current intent
    def clear(self, buffer: list[str]):
        clear_target: list[str] = []

        if not self.intent:
            return buffer
            
        ignore_words: list[str] = registry_commands[self.intent].get("ignore_words", [])
        for i in buffer:
            if i not in ignore_words:
                clear_target.append(i)
        return clear_target

    def parse(self):
        buffer: list[str] = []

        while self.current_token < len(self.tokens) and not self.check("and"):
            buffer.append(self.peek().lexeme)
            self.advance()
            
        return buffer

    def parse_command(self) -> CommandExpr:
        target = self.parse()

        
        if self.intent and registry_commands.get(self.intent):
            raw_text = registry_commands[self.intent]["raw_text"]
            
        # If the raw_text is true in a intent, clear the target of any ignored words
            if raw_text:
                target = self.clear(target)

        target = " ".join(target)

        left = SingleAction(self.intent, target)

        if self.match("and"):
            operator = self.previous().lexeme
            right = self.parse_command()
            
            return SequenceAction(left, operator, right)
        
        return left