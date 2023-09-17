from game import Game
import random

from player import Human


def runner_1():
    """Runs the game"""
    game = Game(9)
    player = Human()
    while not game.game_over:
        move = player.make_move(game)
        game.print_game()

        print("Move:", move)

        game.record_move(move)


        input("Press enter to continue")
    


    





runner_1()
