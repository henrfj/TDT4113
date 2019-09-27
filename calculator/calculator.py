"""
Assignment four in TDT4113: 'Calculator'
"""

import math
import numbers
import re
import sys
from containers import *
from wrappers import *


__author__ = "Henrik Fjellheim"


class Calculator:
    """
    Takes a string input in correct format and returns an answer.
    Parsing included.
    """

    def __init__(self):
        self.functions = {
            'EXP': Function(numpy.exp),
            'LOG': Function(numpy.log),
            'SIN': Function(numpy.sin),
            'COS': Function(numpy.cos),
            'SQRT': Function(numpy.sqrt),
            'ABS': Function(numpy.abs)
        }

        self.operators = {
            'PLUSS': Operator(numpy.add, strength=0),
            'MINUS': Operator(numpy.subtract, strength=0),
            'DELE': Operator(numpy.divide, strength=1),
            'GANGE': Operator(numpy.multiply, strength=1),
        }

        self.constants = {
            'PI': math.pi,
            'TAU': math.tau,
            'E': math.e
        }

        # Parse_text fills this queue with RPN,
        # the evaluate_output_queue evaluates it to find answer
        self.output_queue = Queue()

        # To turn on/off debug for functions and operators.execute
        # self.debug = debug

    def evaluate_output_queue(self):
        """Evaluates the RPN in the queue"""
        stack = Stack()
        while not self.output_queue.is_empty():
            elem = self.output_queue.pop()
            if isinstance(elem, numbers.Number):
                stack.push(elem)
            elif isinstance(elem, Function):
                _input = stack.pop()
                stack.push(elem.execute(_input))
            elif isinstance(elem, Operator):
                # TODO Test if these are popped in the right order
                _input_1 = stack.pop()
                _input_2 = stack.pop()
                stack.push(elem.execute(_input_1, _input_2))

        return stack.pop()


def unit_test():
    p = 1
    while p != 0:
        p = int(input("CHOOSE TESTING: "))
        if p == 1:
            print("BASIC CALCULATOR OPERATION")
            calc = Calculator()
            print(calc.functions["EXP"].execute(calc.operators["PLUSS"].execute(1, calc.operators["GANGE"].execute(2, 3))))
            print("---------------------------")
        if p == 2:
            print("RPN READER TEST")
            calc = Calculator()
            calc.output_queue.push(1)
            calc.output_queue.push(2)
            calc.output_queue.push(3)
            calc.output_queue.push(calc.operators["GANGE"])
            calc.output_queue.push(calc.operators["PLUSS"])
            calc.output_queue.push(calc.functions["EXP"])
            print("ANSWER IS: ", calc.evaluate_output_queue())


unit_test()

