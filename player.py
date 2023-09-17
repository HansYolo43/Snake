from game import Game
import random

game = Game(9)


class Player():

    def make_move():
        """Makes a move"""
        raise NotImplementedError
    


class Human(Player):
    """Human player"""

    def make_move(self, game:Game) -> tuple[int, int] :
        chosen = random.choice(game.possible_moves)

        print(chosen)
        return chosen
        
        
        
