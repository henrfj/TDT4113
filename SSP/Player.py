from random import *
from helper_classes import *


class Player:
    """Parent class for the players"""

    def __init__(self, name):
        """initialize a general player"""
        self.name = name
        self.playerResults = {self: []}

    def choose_action(self):
        """Return the action of the player"""
        pass

    def receive_result(self, opponent, action):
        """Receive results from match"""
        try:
            self.playerResults[opponent].append(action)
        except:
            self.playerResults[opponent] = [action]

    def __str__(self):
        """Easier access to name of class through printing"""
        return self.name


class RandomPlayer(Player):
    """A player who will always have a 50% chance to win"""

    def __int__(self, name):
        """initialize new random_player"""
        super().__init__(name)

    def choose_action(self):
        """Returns a random action"""
        return Action(random.randint(0, 2))


class SequentialPlayer(Player):
    """A stupid player scrolling through all possible actions"""

    def __init__(self, name):
        self.counter = 0
        super().__init__(name)

    def choose_action(self):
        """returns the next move in its sequence"""
        self.counter = (self.counter + 1) % 3
        return Action(self.counter)


class MostUsualPlayer(Player):
    """This player counters the most used move of the opponent"""
    pass
