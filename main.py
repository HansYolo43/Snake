from game import Game
import random

from player import Human, AI


def runner_1():
    """Runs the game"""
    game = Game(9)
    player = AI()
    while not game.game_end():
        move = player.make_move(game)

        game.print_game()

        print("Move:", move)

        val = game.record_move(move)

        if not val:
            print("Game Over")
            break


        # input("Press enter to continue")


    print("Score:", game.score())
    print("Game Over")


    print("Final Board")

    game.print_game()
    


    





runner_1()
