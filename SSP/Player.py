from random import *


class Player:
    """Parent class for the players"""

    def __init__(self, name):
        self.name = name
        self.playerResults = {}

    def choose_action(self):
        """Return the action of the player"""

    def receive_result(self):
        """Receive results from match"""

    def __str__(self):
        """Provides GUI with name of class"""


class RandomPlayer(Player):
    """Will always win with a 50% chance"""
    def __int__(self, name):
        super().__init__(name)



