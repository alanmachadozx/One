from numpy.core.numeric import nextafter

from src.lexer.token import Token, TokenType

class CommandExpr:
        pass

class SingleAction(CommandExpr):
    def __init__(self, action: str | None, target: str):
        self.target = target
        self.action = action

class SequenceAction(CommandExpr):
    def __init__(self, left: CommandExpr, operator: str, right: CommandExpr):
        self.left = left
        self.operator = operator
        self.right = right

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token = 0
        self.actions = { #picks all token types except AND and IDENTIFIER
            t for t in TokenType if t not in (TokenType.AND, TokenType.IDENTIFIER)
        }

    def peek(self) -> Token:
        return self.tokens[self.current_token]
    
    def advance(self):
        self.current_token += 1

    def peek_next(self) -> Token:
        return self.tokens[self.current_token + 1]

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

    def is_action(self):
        if self.current_token >= len(self.tokens):
            return False
        return self.peek().type in self.actions

    def next_is_action(self):
        if self.current_token + 1 >= len(self.tokens):
            return False
        return self.peek_next().type in self.actions

    def parse(self):
        buffer = []

        while self.current_token < len(self.tokens) and not self.check("and"):
            buffer.append(self.peek().lexeme)
            self.advance()
            
        return buffer

    def parse_command(self) -> CommandExpr:
        action = None
        target = " "
        
        if self.is_action():
            action = self.peek().lexeme #splits the structure into {"action", "target"}
            self.advance()
            target = " ".join(self.parse())
        else:
            target = " ".join(self.parse())

        if self.check("and") and not self.next_is_action():
            target = target + " " + " ".join(self.peek().lexeme)
            self.advance()
            target = target + " " + " ".join(self.parse())
            
        left = SingleAction(action, target)

        if self.match("and"):
            operator = self.previous().lexeme
            right = self.parse_command()
            
            return SequenceAction(left, operator, right)
        
        return left