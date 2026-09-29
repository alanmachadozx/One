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
            print(node.action, node.target)
         

        return node
        
    def test_and(self):
        text = "open firefox and open kitty and open spotify"   
        parser = self.parser_result(text)
        print("### AND test ###")
        _ = self.ast_example(parser)
        

if __name__ == '__main__':
    unittest.main()
        