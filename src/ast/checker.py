from src.parser.parser import *
from src.commands.actions import *

command_execute = Actions()

#if it is a SequenceAction, check the left and right nodes
def ast_checker(node: CommandExpr):
    
    if isinstance(node, SequenceAction):
        ast_checker(node.left)
        ast_checker(node.right)

    if isinstance(node, SingleAction) and node.action:
        true_command = node.action + " " + node.target
        command_execute.process(true_command)