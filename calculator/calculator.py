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

        # Parse text to fills this queue with RPN,
        # the evaluate_output_queue evaluates it to find answer
        self.output_queue = Queue()

    def calculate(self):
        """The running of the calculator"""

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
                # print("Number:", elem)
                self.output_queue.push(elem)

            elif isinstance(elem, Function):
                # print("Function:", elem)
                operator_stack.push(elem)

            elif elem == '(':
                # print("Start parentheses: ", elem)
                operator_stack.push(elem)

            elif elem == ')':
                # print("End parentheses: ", elem)
                stack_elem = operator_stack.pop()
                while stack_elem != '(':
                    self.output_queue.push(stack_elem)
                    stack_elem = operator_stack.pop()

            elif isinstance(elem, Operator):
                # print("Operator: ", elem)
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
            item = operator_stack.pop()
            self.output_queue.push(item)

    def parse_string_to_list(self, input_string):
        """
        Parses string to be used in 'output_queue_generator'
        :param input_string: a user-written string to be calculated; assumed correct format
        :return: a string of numbers, functions and operators in a 'normal' syntax
        """

        # Make the string uppercase with no spaces,
        # ready for regex; re methods
        input_string = input_string.replace(" ", "").upper()

        regex_list = (
            '|'.join(
                self.functions.keys()),
            '|'.join(
                self.operators.keys()),
            r'\(',
            r'\)',
            r'\d+\.\d+',        # Positive float
            r'-\d+\.\d+',       # Negative float
            r'\d+',             # Positive integer
            r'-\d+')            # Negative integer

        regex = '|'.join(regex_list)


        # re.findall returns a list containing all matches
        matches = re.findall(regex, input_string)
        result = []
        for match in matches:
            # print(match)
            if match in self.functions.keys():
                result.append(self.functions[match])

            elif match in self.operators.keys():
                result.append(self.operators[match])

            elif match == ')' or match == '(':
                result.append(match)

            else:   # It's a number or trash
                try:
                    result.append(float(match))
                except ValueError:
                    pass

        return result



    @staticmethod
    def precedence_calculator(top, elem):
        """
        :param top: top element of stack, can be function, operator, number
        :param elem: is a operator with a strength
        :return: if top has precedence over elem
        """
        if isinstance(
            top,
            numbers.Number) or top == '(' or isinstance(
                top,
                Function):
            return False
        if isinstance(top, Operator):
            return top.strength >= elem.strength



def unit_test():
    p = 1
    while p != 0:
        print("--------------------------------------")
        print(
            "0:EXIT\n1:BASICS\n2:RPN READER\n3:RPN GENERATOR\n4:Combined 2 and 3\n5:REGEX\n6:CALCULATE")
        p = int(input("--------------------------------------\nCHOOSE FROM THE LIST ABOVE: "))
        if p == 1:
            print("BASIC CALCULATOR OPERATION")
            calc = Calculator()
            print(
                calc.functions["EXP"].execute(
                    calc.operators["PLUSS"].execute(
                        1, calc.operators["GANGE"].execute(
                            2, 3))))

        if p == 2:
            print("RPN READER TEST")
            calc = Calculator()
            calc.output_queue.push(1)
            calc.output_queue.push(2)
            calc.output_queue.push(3)
            calc.output_queue.push(calc.operators["GANGE"])
            calc.output_queue.push(calc.operators["PLUSS"])
            calc.output_queue.push(calc.functions["EXP"])
            rpn_printer(calc.output_queue)
            print("ANSWER IS: ", calc.evaluate_output_queue())
        if p == 3:
            print("NORMAL --> RPN TEST")
            calc = Calculator()
            norm = [
                calc.functions["EXP"],
                '(',
                1,
                calc.operators["PLUSS"],
                2,
                calc.operators["GANGE"],
                3,
                ')']
            norm_printer(norm)
            calc.output_queue_generator(norm)
            rpn_printer(calc.output_queue)
            print()
            norm2 = [2, calc.operators["GANGE"], 3, calc.operators["PLUSS"], 1]
            norm_printer(norm2)
            calc.output_queue_generator(norm2)
            rpn_printer(calc.output_queue)

        if p == 4:
            print("NORMAL --> RPN --> EVALUATED")
            calc = Calculator()
            norm = [
                calc.functions["EXP"],
                '(',
                1,
                calc.operators["PLUSS"],
                2,
                calc.operators["GANGE"],
                3,
                ')']
            norm_printer(norm)
            calc.output_queue_generator(norm)
            rpn_printer(calc.output_queue)
            print("ANSWER IS: ", calc.evaluate_output_queue())

        if p == 5:
            print("REGEX")
            calc = Calculator()
            s1 = "EXP(3.14 pluss -22 gange -3.33)"
            norm1 = calc.parse_string_to_list(s1)
            print(s1, "==> ")
            norm_printer(norm1)

            s2 = "((15 DELE (7 MINUS (1 PLUSS 1))) GANGE 3) MINUS (2 PLUSS (1 PLUSS 1))"
            norm2 = calc.parse_string_to_list(s2)
            print(s2, "==> ")
            norm_printer(norm2)

        if p == 6:
            print("Combined functionality")


def rpn_printer(rpn):
    """For debugging"""
    print("RPN: [ ", end='')
    s = rpn.size()
    l = rpn.items
    for i in range(s):
        if i != s - 1:
            print(l[i], ", ", end='')
        else:
            print(l[i], "]")


def norm_printer(norm):
    """For debugging"""
    print("Normal: [ ", end='')
    for i in range(len(norm)):
        if i != len(norm) - 1:
            print(norm[i], ", ", end='')
        else:
            print(norm[i], "]")


unit_test()
