from game import Game
import random

from player import Human , Djaktra, A_star, DFS, BFS ,  Hamiltonin

from typing import Type, Dict, List
from test import simulate_games, plot_results


def main():
    # List of player types
    # player_types = [Human, Djaktra, A_star, DFS, BFS, FloodFill ,  AI_Hamiltonian_Dijkstra]
    player_types = [Hamiltonin]
    grid_size = 10  # Grid size for the game
    
    # Conduct Simulations
    results = simulate_games(grid_size, player_types)
    
    # Print Results
    for player, result in results.items():
        print(f"{player}: Time = {result['Time']} seconds, Score = {result['Score']}")
    
    # # Plot Results
    # plot_results(results)


    

main()

