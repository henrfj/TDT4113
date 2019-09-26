"""Helper classes used in 'calculator'"""

__author__ = "Henrik Fjellheim"


class Container:
    """Superclass for the different containers"""

    def __init__(self):
        self.items = []

    def size(self):
        """Return number of elements in self.items"""
        return len(self.items)

    def is_empty(self):
        """Check if self.items is empty"""
        return len(self.items) == 0

    def push(self, item):
        """Pushes item to the end of the list"""
        self.items.append(item)

    def pop(self):
        """Removes and returns top element of container.
        Is different for different subclasses; thus this is a dummy"""
        raise NotImplementedError

    def peek(self):
        """Returns top element of container without removing it.
        Is different for different subclasses; thus this is a dummy"""
        raise NotImplementedError


class Queue(Container):
    """A standard queue container. FIFO"""

    def peek(self):
        """:return top element of queue without removing it"""
        return self.items[0]

    def pop(self):
        """:return top element of queue after removing it"""
        return self.items.pop(0)


class Stack(Container):
    """A standard stack container. LIFO"""

    def peek(self):
        """:return top element of stack without removing it"""
        return self.items[-1]

    def pop(self):
        """:return top element of stack after removing it"""
        return self.items(-1)
