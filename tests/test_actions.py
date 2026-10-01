
"""

This file is responsible for testing the actions commands in isolation from the main code,
with the aim of verifying whether a specific new function is functional.

to execute: python -m unittest tests/test_actions.py
"""

import unittest
from src.commands.actions import *

class TestActions(unittest.TestCase):

    def test_actions(self):
        action = "search for" 
        target = "Led Zeppelin is the best band of all time?"

        print(f'actions: {action}, target: {target}')
        actions = Actions()
        actions.process(action, target)

if __name__ == '__main__':
    unittest.main()
        