"""
Wrappers of functions and operators used in the program
"""

import numbers
import numpy


class Function:
    """
    Function wrapper
    """
    def __init__(self, func):
        self.func = func

    def execute(self, element, debug=False):

        # Check type
        if not isinstance(element, numbers.Number):
            raise TypeError(f'Cannot execute function as "{element}" is not a number')

        result = self.func(element)

        # Report
        if debug is True:
            print("Function: " + self.func.__name__
                  + "({:f}) = {:f}".format(element, result))

        return result

    def __str__(self):
        return self.func.__name__


class Operator:
    """
    Wrapper for operator
    """

    def __init__(self, operation, strength=0):
        self.operation = operation
        self.strength = strength

    def execute(self, first_elem, second_elem, debug=False):

        # Check type
        if not isinstance(first_elem, numbers.Number):
            raise TypeError(f'Cannot execute {self.operation} as {first_elem} is not a number')

        if not isinstance(second_elem, numbers.Number):
            raise TypeError(f'Cannot execute {self.operation} as {second_elem} is not a number')

        result = self.operation(first_elem, second_elem)

        # Report
        if debug:
            print(f'Operation: {first_elem} ' + self.operation.__name__ + f' {second_elem} = {result}')

        return result

    def __str__(self):
        return self.operation.__name__


def unit_test():
    exp = Function(numpy.exp)
    sin = Function(numpy.sin)
    print(exp.execute(sin.execute(4)))
    print(exp.execute(sin.execute(0)))
    try:
        print(exp.execute(sin.execute("hei")))
    except TypeError as e:
        print("ERROR", e)

    add_op = Operator(numpy.add, 0)
    multiply_op = Operator(numpy.multiply, 1)
    print(add_op.execute(1, multiply_op.execute(2, 3)))

    try:
        print(add_op.execute("poop", "poop"))
    except TypeError as e:
        print("ERROR", e)

    print("ORDER TEST")
    div_op = Operator(numpy.divide, 1)
    print(div_op.execute(10, 2))
    sub_op = Operator(numpy.subtract, 0)
    print(sub_op.execute(2, 1))




# unit_test()

