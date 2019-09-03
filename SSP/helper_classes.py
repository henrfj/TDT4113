from Player import *
import matplotlib.pyplot


class Action:
    """Helper class to sort out interaction between moves"""

    def __init__(self, action):
        """initialize a new action"""
        self.action = action

    def get_action(self):
        """returns the action played"""
        return self.action

    def __eq__(self, other):
        """Checks if two actions are the same, resulting in draw"""
        return self.action == other.action

    def __gt__(self, other):
        """Checks if an action beats another"""
        cmp = {0: 2, 1: 0, 2: 1}
        return cmp[self.action] != other.action

    def __str__(self):
        """for printing the move"""
        moves = ["rock", "scissors", "paper"]
        return moves[self.action]


class SingleMatch:
    """A class for a single match"""

    def __init__(self, player1, player2):
        """initializes a single match"""
        self.player1 = player1
        self.player2 = player2
        self.actionP1 = None
        self.actionP2 = None
        self.score = [0, 0]

    def execute_game(self):
        """Receives moves from both players, chooses winner and rapports results to both"""
        self.actionP1 = self.player1.choose_action(self.player2)
        self.actionP2 = self.player2.choose_action(self.player1)

        if self.actionP1 == self.actionP2:
            self.score = [0.5, 0.5]

        elif self.actionP1 > self.actionP2:
            self.score = [1, 0]

        else:
            self.score = [0, 1]

        self.player1.receive_result(self.player2, self.actionP2)
        self.player2.receive_result(self.player1, self.actionP1)

    def __str__(self):
        return str(self.player1) \
            + ": " + str(self.actionP1) \
            + ".\n" + str(self.player2) \
            + ": " + str(self.actionP2) + "."


class ManyMatches:
    """Contains methods for executing many matches = a tournament"""

    def __init__(self, player1, player2, number_of_matches):
        self.player1 = player1
        self.player2 = player2
        self.number_of_matches = number_of_matches
        self.scores = [0, 0]
        self.percentage = 0.0

    def single_match(self):
        """arranges a single match and returns score after printing some results to console"""
        match = SingleMatch(self.player1, self.player2)
        match.execute_game()
        print(match)
        return match.score

    def tournament(self):
        """arranges a whole tournament between player 1 and 2 with correct number of matches. Also plots"""

        x_axis = []
        y_axis = []

        for i in range(self.number_of_matches):
            score = self.single_match()

            self.scores[0] += score[0]
            self.scores[1] += score[1]

            self.percentage = self.scores[0] / (i + 1)

            x_axis.append(i + 1)
            y_axis.append(self.percentage)

        print("The tournament completed:\n" +
              str(self.player1) +
              ": " +
              str(self.scores[0]) +
              " points.\n" +
              str(self.player2) +
              ": " +
              str(self.scores[1]) +
              " points.")

        matplotlib.pyplot.plot(x_axis, y_axis)
        matplotlib.pyplot.axis([0, self.number_of_matches, 0, 1])
        matplotlib.pyplot.grid(True)
        matplotlib.pyplot.axhline(y=0.5, linewidth=0.5, color="m")
        matplotlib.pyplot.xlabel("Number of games")
        matplotlib.pyplot.ylabel("Winning percentage for " + str(self.player1))
        matplotlib.pyplot.show()


def main():
    """main function, obviously"""
    p1 = RandomPlayer("RandomDude")
    p2 = SequentialPlayer("SequentialDude")

    tourney = ManyMatches(p1, p2, 1000)
    tourney.tournament()

main()
