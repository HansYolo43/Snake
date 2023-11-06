import time
from typing import Type, Dict, List
from player import Player
from game import Game
from plotly import graph_objects as go


def simulate_games(grid_size: int, player_types: List[Type[Player]]) -> Dict[str, Dict[str, float]]:
    results = {}

    for player_type in player_types:
        player = player_type()  # Initialize player

        # Initialize Game with Player
        game = Game(grid_size=grid_size)

        # Record Start Time
        start_time = time.time()

        # Run the Game
        simulate_game_g(game, player)
        # This method should run the game until it ends and should be part of your Game class

        # Record End Time
        end_time = time.time()

        # Record Results
        results[player_type.__name__] = {
            "Time": end_time - start_time,
            "Score": game.score()
            # This method should return the score of the game and should be part of your Game class
        }

    return results


def simulate_game(game: Game, player: Player):
    while not game.game_end():
        move = player.make_move(game)

        print(f"Move: {move}")

        game.print_game()

        val = game.record_move(move)

        print(val)

        if not val:
            print("Game Over")
            break


def simulate_game_g(game: Game, player: Player):
    while not game.game_end():
        # Get the path from the player's make_move method.
        path = player.make_move(game)

        print("Path", path)

        # Process each move along the path.
        for move in path:
            print(f"Move: {move}")
            game.print_game()  # This should visually represent the game state.

            # Record the move and update the game state.
            move_success = game.record_move(move)

            # If move was not successful, it's game over.
            if not move_success:
                print("Move was unsuccessful. Game Over.")
                return  # End the simulation.

            # Check if the game has ended after the move (snake ate itself or hit a wall).
            if game.game_end():
                print("Game Over.")
                return  # End the simulation.d



def plot_results(results: Dict[str, Dict[str, float]]):
    player_names = list(results.keys())
    times = [results[name]["Time"] for name in player_names]
    scores = [results[name]["Score"] for name in player_names]

    # Create a bar chart for scores and times
    fig = go.Figure(data=[
        go.Bar(name='Scores', x=player_names, y=scores),
        go.Bar(name='Time (s)', x=player_names, y=times)
    ])

    # Change the bar mode
    fig.update_layout(barmode='group', title="Performance of Different Players")
    fig.show()
