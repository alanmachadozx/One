"""

This file is responsible for testing the parser in isolation from the main code,
with the aim of verifying whether a specific new function is functional.

to execute: python -m unittest tests/test_parser.py

"""

import unittest
from src.parser.parser import *
from src.lexer.scanner import *


class TestParser(unittest.TestCase):
    
    def parser_result(self, text: str):
        scanner = Scanner(text)
        scanner.scan()
        parser = Parser(scanner.tokens)
        return parser.parse_command()

    def ast_example(self, node: CommandExpr):
        
        if isinstance(node, SequenceAction):
            self.ast_example(node.left)
            self.ast_example(node.right)

        if isinstance(node, SingleAction):
            print(f"action: {node.action}, target: {node.target}")
         
    # Tests the AND connector, which executes two or more separate commands.
    def test_and(self):
        #There are three separate commands that will be executed.
        text = "open firefox and open kitty and open spotify"   
        parser = self.parser_result(text)
        
        print("\n########### AND connector test ###########")
        self.ast_example(parser)

    # Tests composite actions that consist of more than one action token.
    def test_compound_action(self):
        # create and task are two separate actions in TokenType class
        text = "I am going to create task make a coffee" 
        parser = self.parser_result(text)
        
        print("\n########### Compound action test ###########")
        self.ast_example(parser)

    # Tests cases where, instead of two commands connected by an AND,
    # there is a single command with a target containing the `and` token.
    # Note: If the next token is an action, the parser will treat it as two separate commands.
    def test_and_in_context(self):
        text = "play heaven and hell by Black Sabbath "
        parser = self.parser_result(text)
        
        print("\n########### AND in context test ###########")
        self.ast_example(parser)

    def test_clear_target(self):
        text = "open a firefox"
        parser = self.parser_result(text)

        print("\n########### Clear target test ###########")
        self.ast_example(parser)

if __name__ == '__main__':
    unittest.main()
        