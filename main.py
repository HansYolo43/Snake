from game import Game
import random

from player import Random , Djaktra, A_star, DFS, BFS ,  Hamiltonin

from typing import Type, Dict, List
from test import simulate_games, plot_results


def graph():
    """Run the game simulation and plot the results."""
    # List of player types
    player_type = [Random, Djaktra, A_star]
    player_types = [DFS, BFS, Hamiltonin]
    
    
    grid_size = 10  # Grid size
    
    # Conduct Simulations
    result = simulate_games(grid_size, player_type)
    results = simulate_games(grid_size, player_types)

    for player, result in result.items():
        print(f"{player}: Time = {result['Time']} seconds, Score = {result['Score']}")
    

    for player, result in results.items():
        print(f"{player}: Time = {result['Time']} seconds, Score = {result['Score']}")
    
    # # Plot Results
    plot_results(result)
    plot_results(results)

    
import arcade

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Snake Game"

class StartView(arcade.View):
    def on_show(self):
        arcade.set_background_color(arcade.color.WHITE)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        arcade.draw_text("Snake Game", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50,
                         arcade.color.BLACK, font_size=50, anchor_x="center")
        arcade.draw_text("Click to play", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        arcade.draw_text("Press S to simulate", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 50,
                         arcade.color.GRAY, font_size=20, anchor_x="center")
        
        #

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = GameView()
        self.window.show_view(game_view)

    def on_key_press(self, symbol, modifiers):
        """ If the user presses 'S', start the simulation. """
        if symbol == arcade.key.S:
            simulate_view = SimulateView()
            self.window.show_view(simulate_view)


# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Snake Game"
CELL_WIDTH = 20
CELL_HEIGHT = 20
GRID_WIDTH = SCREEN_WIDTH // CELL_WIDTH
GRID_HEIGHT = SCREEN_HEIGHT // CELL_HEIGHT
INITIAL_SPEED = 10  

class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.snake_body = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.snake_direction = (0, 1)  # Start 
        self.food_x = random.randint(0, GRID_WIDTH - 1)
        self.food_y = random.randint(0, GRID_HEIGHT - 1)
        self.score = 0
        self.frames_since_last_move = 0
        self.frames_between_moves = INITIAL_SPEED
        self.total_time = 0.0  # Initial frames 

        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        # Draw the snake
        for x, y in self.snake_body:
            arcade.draw_rectangle_filled(x * CELL_WIDTH + CELL_WIDTH // 2,
                                         y * CELL_HEIGHT + CELL_HEIGHT // 2,
                                         CELL_WIDTH, CELL_HEIGHT,
                                         arcade.color.GREEN)
        # Draw the food
        arcade.draw_rectangle_filled(self.food_x * CELL_WIDTH + CELL_WIDTH // 2,
                                     self.food_y * CELL_HEIGHT + CELL_HEIGHT // 2,
                                     CELL_WIDTH, CELL_HEIGHT,
                                     arcade.color.RED)
        # Draw the score
        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, SCREEN_HEIGHT - 40, arcade.color.WHITE, 20)

        # Draw the timer
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(time_text, 10, SCREEN_HEIGHT - 80, arcade.color.WHITE, 20)

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        if key == arcade.key.UP and self.snake_direction != (0, -1):
            self.snake_direction = (0, 1)
        elif key == arcade.key.DOWN and self.snake_direction != (0, 1):
            self.snake_direction = (0, -1)
        elif key == arcade.key.LEFT and self.snake_direction != (1, 0):
            self.snake_direction = (-1, 0)
        elif key == arcade.key.RIGHT and self.snake_direction != (-1, 0):
            self.snake_direction = (1, 0)
        elif key == arcade.key.ESCAPE:
            start_view = StartView()
            self.window.show_view(start_view)

    def update(self, delta_time):
        """ Movement and game logic """
        self.total_time += delta_time
        self.frames_since_last_move += 1

        if self.frames_since_last_move >= self.frames_between_moves:
            # Reset the frame counter
            self.frames_since_last_move = 0

            
            head_x, head_y = self.snake_body[0]
            new_x = head_x + self.snake_direction[0]
            new_y = head_y + self.snake_direction[1]

            # Check for collisions
            if new_x < 0 or new_y < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT:
                self.game_over()
                return

            if (new_x, new_y) in self.snake_body:
                self.game_over()
                return

            if (new_x, new_y) == (self.food_x, self.food_y):
                self.snake_body.insert(0, (new_x, new_y))
                self.spawn_food()
                self.score += 1
                self.increase_speed()
            else:
                self.snake_body.pop()
                self.snake_body.insert(0, (new_x, new_y))

    def spawn_food(self):
        
        while True:
            self.food_x = random.randint(0, GRID_WIDTH - 1)
            self.food_y = random.randint(0, GRID_HEIGHT - 1)
            if (self.food_x, self.food_y) not in self.snake_body:
                break

    def increase_speed(self):
        # Decrease the number of frames between moves, speeding up the snake
        self.frames_between_moves = max(5, self.frames_between_moves - 1)

    def game_over(self):
        print("Game over!")
        
        end_view = EndView(self.score, self.total_time)
        self.window.show_view(end_view)

#ENd view
class EndView(arcade.View):
    def __init__(self, score, total_time):
        super().__init__()
        self.score = score
        self.total_time = total_time

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        """ Draw this view """
        arcade.start_render()
        # Draw the final score and time
        score_text = f"Final Score: {self.score}"
        arcade.draw_text(score_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        time_text = f"Total Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(time_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

        # Draw the retry and main menu options
        retry_text = "Retry"
        arcade.draw_text(retry_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 50,
                         arcade.color.WHITE, font_size=20, anchor_x="center")
        main_menu_text = "Main Menu"
        arcade.draw_text(main_menu_text, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        if key == arcade.key.R:
            game_view = GameView()
            self.window.show_view(game_view)
        elif key == arcade.key.M:
            start_view = StartView()
            self.window.show_view(start_view)
        elif key == arcade.key.ESCAPE:
            start_view = StartView()
            self.window.show_view(start_view)


#SIMULATE VIEW
# Constants for the screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "Snake Game Simulation"

# Constants for simulation options
SIMULATION_OPTIONS = ['Random', 'Dijkstra', 'A*', 'DFS', 'BFS', 'Hamiltonian']
SIMULATION_FUNCTIONS = {
    'Random': Random,  
    'Dijkstra': Djaktra,
    'A*': A_star,
    'DFS': DFS,
    'BFS': BFS,
    'Hamiltonian': Hamiltonin
}


class SimulateView(arcade.View):
    def __init__(self):
        super().__init__()
        self.selected_option_index = 0
        self.grid_size = 20  
        self.input_mode = False 
        self.input_value = ""  

    def on_draw(self):
        """ Draw the simulation selection menu. """
        arcade.start_render()

        arcade.set_background_color(arcade.color.BLACK)

        # Draw title
        arcade.draw_text("Snake Game Simulation", SCREEN_WIDTH / 2, SCREEN_HEIGHT - 60,
                         arcade.color.WHITE, font_size=30, anchor_x="center", anchor_y="center")

        # Draw grid size input
        grid_size_text = f"Grid Size: {self.grid_size if not self.input_mode else self.input_value}"
        arcade.draw_text(grid_size_text, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 60,
                         arcade.color.WHITE if not self.input_mode else arcade.color.YELLOW,
                         font_size=20, anchor_x="center", anchor_y="center")

        # Draw options
        for index, option in enumerate(SIMULATION_OPTIONS):
            y_position = SCREEN_HEIGHT / 2 - 30 * index
            color = arcade.color.RED if index == self.selected_option_index else arcade.color.WHITE
            arcade.draw_text(option, SCREEN_WIDTH / 2, y_position, color, font_size=20, anchor_x="center")

        # Draw instructions
        instructions = "Use UP/DOWN to change selection, ENTER to start, and type G to set grid size."
        arcade.draw_text(instructions, SCREEN_WIDTH / 2, 40, arcade.color.LIGHT_GRAY, font_size=16, anchor_x="center")

        

    def on_key_press(self, key, modifiers):
        """ Handle user input for simulation selection. """
        
        if self.input_mode:
            if key >= arcade.key.KEY_0 and key <= arcade.key.KEY_9:
                self.input_value += chr(key)
            elif key == arcade.key.BACKSPACE:
                self.input_value = self.input_value[:-1]
            elif key == arcade.key.ENTER and self.input_value:
                # Exit input mode and set grid size
                self.grid_size = int(self.input_value)
                self.input_mode = False
                self.input_value = ""
            elif key == arcade.key.ESCAPE:
                start_view = StartView()
                self.window.show_view(start_view)
            return

        
        if key == arcade.key.UP:
            self.selected_option_index = max(0, self.selected_option_index - 1)
        elif key == arcade.key.DOWN:
            self.selected_option_index = min(len(SIMULATION_OPTIONS) - 1, self.selected_option_index + 1)
        elif key == arcade.key.ENTER:
            selected_simulation = SIMULATION_OPTIONS[self.selected_option_index]
            simulation_function = SIMULATION_FUNCTIONS[selected_simulation]
            self.window.show_view(SimulationView(self.grid_size, simulation_function))
        elif key == arcade.key.G:
            # Enter input mode to change grid size
            self.input_mode = True
        elif key == arcade.key.ESCAPE:
            start_view = StartView()
            self.window.show_view(start_view)

        

import time

# Constants for the simulation
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600


SCREEN_TITLE = "Snake Game Simulation"
INITIAL_SPEEDS = 0.0001 # Initial frames between each update

class SimulationView(arcade.View):
    
    def __init__(self, grid_size, player_class):
        super().__init__()
        self.game = Game(grid_size)
        self.player = player_class()
        self.total_time = 0.0
        self.frames_since_last_move = 0
        self.frames_between_moves = INITIAL_SPEEDS
        self.grid  = grid_size




        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        arcade.start_render()

        CELL_WIDTH = SCREEN_WIDTH // self.grid
        CELL_HEIGHT = SCREEN_HEIGHT // self.grid
        # Draw the snake body
        for x, y in self.game.snake.snake:


            arcade.draw_rectangle_filled(x * CELL_WIDTH + CELL_WIDTH // 2,
                                         y * CELL_HEIGHT + CELL_HEIGHT // 2,
                                         CELL_WIDTH, CELL_HEIGHT,
                                         arcade.color.GREEN)
        # Draw the food
        arcade.draw_rectangle_filled(self.game.food[0] * CELL_WIDTH + CELL_WIDTH // 2,
                                     self.game.food[1] * CELL_HEIGHT + CELL_HEIGHT // 2,
                                     CELL_WIDTH, CELL_HEIGHT,
                                     arcade.color.RED)
        # Draw the score
        score_text = f"Score: {self.game.score()}"
        arcade.draw_text(score_text, 10, SCREEN_HEIGHT - 40, arcade.color.WHITE, 20)

        # Draw the timer
        minutes = int(self.total_time) // 60
        seconds = int(self.total_time) % 60
        time_text = f"Time: {minutes:02d}:{seconds:02d}"
        arcade.draw_text(time_text, 10, SCREEN_HEIGHT - 80, arcade.color.WHITE, 20)

    def update(self, delta_time):
        self.total_time += delta_time
        self.frames_since_last_move += 1

        if self.frames_since_last_move >= self.frames_between_moves:
            self.frames_since_last_move = 0

            # Ask the player for the next move
            next_move = self.player.make_move(self.game)

            if isinstance(next_move, list):  # Path-based player
                if next_move:
                    
                    self.game.record_move(next_move.pop(0))
            else:  # Move-based player
                self.game.record_move(next_move)

            # Check if the game has ended
            if self.game.game_end():
                
                print(f"Game Over. Total time: {self.total_time:.2f} seconds, Score: {self.game.score()}")
                self.game_over()

    def game_over(self):
        print(f"Game Over. Total time: {self.total_time:.2f} seconds, Score: {self.game.score()}")
        # Switch to the end view
        end_view = EndView(self.game.score(), self.total_time)
        self.window.show_view(end_view)

    def on_key_press(self, key, modifiers):
        """ Called whenever a key is pressed. """
        if key == arcade.key.ESCAPE:
            start_view = StartView()
            self.window.show_view(start_view)


def main():
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
    start_view = StartView()
    window.show_view(start_view)
    arcade.run()

if __name__ == "__main__":
    main()



