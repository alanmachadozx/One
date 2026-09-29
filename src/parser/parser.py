
"""
The parser is where the distinction is made between elements conveying an intended action and those that merely complement the sentence 
(such as *and*, *in*, *to*, *on*). Furthermore, the command is separated into a target and an action.
"""

from src.lexer.token import Token, TokenType
from src.commands.registry import registry_commands, trash_tokens

class CommandExpr:
        pass

class SingleAction(CommandExpr):
    def __init__(self, action: str | None, target: str):
        self.target: str = target
        self.action: str | None = action

class SequenceAction(CommandExpr):
    def __init__(self, left: CommandExpr, operator: str, right: CommandExpr):
        self.left: CommandExpr = left
        self.operator: str = operator
        self.right: CommandExpr = right

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens: list[Token] = tokens
        self.current_token: int = 0
        self.actions: set[TokenType] = { #picks all token types except AND and IDENTIFIER
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

    def valid_action(self):
        action = None
        target: list[str] = []

        if self.is_action():
            #splits the structure into {"action", "target"},
            #transforms two action tokens into a single action if it is a compound command, like "create task"
            if self.next_is_action():
                action = self.peek().lexeme + " " + self.peek_next().lexeme
                self.advance()
            else:
                action = self.peek().lexeme
                
            self.advance()
            target = self.parse().copy()
            
        else:
            target = self.parse().copy()
        #It deals with cases where, instead of two commands connected by an AND operator,
        #there is a single command with a target containing the `and` token. 
        #If the next token is an action, the parser treats it as two separate commands.
        if self.check("and") and not self.next_is_action():
            target.append(self.peek().lexeme)
            self.advance()
            target = target + self.parse()

        return action, target

    def clear_target(self, buffer: list[str]):
        clear_target: list[str] = []
        for i in buffer:
            if i not in trash_tokens:
                clear_target.append(i)
        return clear_target

    def parse(self):
        buffer: list[str] = []

        while self.current_token < len(self.tokens) and not self.check("and"):
            buffer.append(self.peek().lexeme)
            self.advance()
            
        return buffer

    def parse_command(self) -> CommandExpr:
        action, target = self.valid_action()
        
        if action and registry_commands.get(action):
            raw_text = registry_commands[action]["raw_text"]

            if not raw_text:
                target = self.clear_target(target)

        target = " ".join(target)
        
        left = SingleAction(action, target)

        if self.match("and"):
            operator = self.previous().lexeme
            right = self.parse_command()
            
            return SequenceAction(left, operator, right)
        
        return left