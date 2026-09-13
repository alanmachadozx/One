from lexer.token import Token

class CommandExpr:
        pass

class SingleAction(CommandExpr):
    def __init__(self, text):
        self.text = text

class SequenceAction(CommandExpr):
    def __init__(self, left: CommandExpr, operator: str, right: CommandExpr):
        self.left = left
        self.operator = operator
        self.right = right

class Parser:
    def __init__(self, tokens: list[Token]):
        self.tokens = tokens
        self.current_token = 0

    def peek(self) -> Token:
        return self.tokens[self.current_token]

    def advance(self):
        self.current_token += 1

    # if the current token matches the given type, advance and return True, otherwise return False
    def match(self, token_type: str):
        if self.peek().type == token_type:
            self.advance()
            return True
        return False

    