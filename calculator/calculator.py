"""
Assignment four in TDT4113: 'Calculator'
"""

import math
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

    def output_queue_generator(self, input_list):
        """
        Uses the shunting yard algorithm to tak a standard list of calculations
        and turn it intro a list of RPN, to be calculated
        :param input_list: a list of numbers, parentheses, operators and functions as its elements
        """
        self.output_queue = Queue()
        operator_stack = Stack()

        for elem in input_list:

            if isinstance(elem, numbers.Number):
                self.output_queue.push(elem)

            elif isinstance(elem, Function):
                operator_stack.push(elem)

            elif elem == '(':
                operator_stack.push(elem)

            elif elem == ')':
                stack_elem = operator_stack.pop()
                while stack_elem != '(':
                    self.output_queue.push(stack_elem)
                    stack_elem = operator_stack.pop()
                operator_stack.pop()    # Getting rid of the start parentheses

            elif isinstance(elem, Operator):
                if not operator_stack.is_empty():
                    top = operator_stack.peek()
                    precedence = self.precedence_calculator(top, elem)
                    while top is not None and precedence:
                        self.output_queue.push(operator_stack.pop())
                        if not operator_stack.is_empty():
                            top = operator_stack.peek()
                        else:
                            top = None
                operator_stack.push(elem)

        while not operator_stack.is_empty():
            self.output_queue.push(operator_stack.pop())




    @staticmethod
    def precedence_calculator(top, elem):
        """
        :param top: top element of stack, can be function, operator, number
        :param elem: is a operator with a strength
        :return: if top has precedence over elem
        """
        if isinstance(top, numbers.Number) or top == '(' or isinstance(top, Function):
            return False
        if isinstance(top, Operator):
            return top.strength >= elem.strength


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
        if p == 3:
            print("NORMAL --> RPN TEST")
            calc = Calculator()
            norm = [numpy.exp, '(', 1, numpy.add, 2, numpy.multiply, 3, ')']
            calc.output_queue_generator(norm)

            print("NORMAL: ", norm, "RPN: ", calc.output_queue)


unit_test()

