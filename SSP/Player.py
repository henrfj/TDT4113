import random
# from helper_classes import *
import matplotlib.pyplot

# --------------Different Players--------------


class Player:
    """Parent class for the players"""

    def __init__(self, name):
        """initialize a general player"""
        self.name = name
        self.playerMoves = {self: []}

    def choose_action(self, opponent):
        """Return the action of the player"""
        pass

    def receive_result(self, opponent, action):
        """Receive results from match"""
        try:
            self.playerMoves[opponent].append(action.action)
        except KeyError:
            self.playerMoves[opponent] = [action.action]

    def __str__(self):
        """Easier access to name of class through printing"""
        return self.name

    def get_results(self):
        """Currently only used for debugging purposes"""
        return self.playerMoves


class RandomPlayer(Player):
    """A player who will always have a 50% chance to win"""

    def __int__(self, name):
        """initialize new random_player"""
        super().__init__(name)

    def choose_action(self, opponent):
        """Returns a random action"""
        action = Action(random.randint(0, 2))
        self.playerMoves[self].append(action.action)
        return action


class SequentialPlayer(Player):
    """A stupid player scrolling through all possible actions"""

    def __init__(self, name):
        self.counter = 2
        super().__init__(name)

    def choose_action(self, opponent):
        """returns the next move in its sequence"""
        self.counter = (self.counter + 1) % 3
        action = Action(self.counter)
        self.playerMoves[self].append(action.action)
        return action


class MostUsualPlayer(Player):
    """This player counters the most used move of the opponent"""
    def __init__(self, name):
        """initializes a new most usual player, not being a very smart player"""
        super().__init__(name)

    def choose_action(self, opponent):
        """Chooses the counter for opponents most usual move"""
        move_counter = [0, 0, 0]
        try:    # It will fail when the opponents key is missing (before first match)
            for move in self.playerMoves[opponent]:
                move_counter[move] += 1
        except KeyError:
            pass

        if sum(move_counter) != 0:
            action = Action(find_counter(move_counter.index(max(move_counter))))
            self.playerMoves[self].append(action.action)
            return action

        action = Action(random.randint(0, 2))
        self.playerMoves[self].append(action.action)
        return action


class HistorianPlayer(Player):
    """This player looks for patterns in the opponents history"""
    def __init__(self, name, depth):
        """initialize a new historian player, using the superclass to set name"""
        self.depth = depth
        super().__init__(name)

    def choose_action(self, opponent):
        """Chooses action based on pattern recognition, using 'depth' to decide depth of inspection"""


# --------------HELP-CLASSES--------------

def find_counter(move):
    """receives an integer representing a move, returns the counter"""
    counters = {0: 2, 1: 0, 2: 1}
    return counters[move]


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

        print("player moves for " + str(self.player1) + ": " + str(self.player1.get_results()[self.player1]))
        print("player moves for " + str(self.player2) + ": " + str(self.player2.get_results()[self.player2]))


def main():
    """main function, obviously"""
    p1 = RandomPlayer("RandomDude")
    p2 = SequentialPlayer("SequentialDude")
    p3 = MostUsualPlayer("MostUsualDude")
    p4 = HistorianPlayer("HistorianDude", 2)

    tourney = ManyMatches(p1, p3, 1000)
    tourney.tournament()


main()
