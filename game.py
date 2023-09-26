"""Snake game logic"""
from grid import Grid
from snake import Snake
from random import randint


class Game:
    """Snake game logic
    Attributes:
            grid_size (int): The size of the board (i.e. the number of rows and columns).
            grid (list): A 2D list representing the board, containing Stone objects.
            snake (class) Contains all the details abt snake.
            food (tuple): A tuple containing the coordinates of the food.
            game_over (bool): A boolean value indicating whether the game is over.
            possible_moves (list): A list containing all the possible moves that the snake can make.
            """

    grid_size: int
    grid: Grid
    snake: Snake
    food: tuple[int, int]
    game_over: bool
    possible_moves: list[tuple[int, int]]

    def __init__(self, grid_size):
        self.grid_size = grid_size
        self.grid = Grid(grid_size)

        self.game_over = False
        self.food = (grid_size // 2, grid_size // 2)
        self.snake = Snake()
        self.possible_moves = [(0, 1), (1, 0)]

    def spawn_food(self) -> tuple[int, int] | None:
        """gives next food on the board"""
        while len(self.snake.snake) < self.grid_size ** 2:
            x = randint(0, self.grid_size - 1)
            y = randint(0, self.grid_size - 1)
            if (x, y) not in self.snake.snake:
                return x, y
        return None

    def game_over_(self) -> bool:
        """checks if game is over"""
        return not self.snake.alive or len(self.snake.snake) == self.grid_size ** 2 or self.collision_food(self) or self.outof_boundary()

    def collision(self) -> bool:
        """checks if snake has collided with itself"""
        return self.snake.snake_head in self.snake.snake[:-1]

    def outof_boundary(self) -> bool:
        """checks if snake has gone out of boundary"""
        return self.snake.snake_head[0] < 0 or self.snake.snake_head[0] >= self.grid_size or self.snake.snake_head[
            1] < 0 or self.snake.snake_head[1] >= self.grid_size

    def game_end(self) -> bool:
        """checks if game is over"""
        return self.collision() or self.outof_boundary() or self.game_over_()

    def collision_food(self, move: tuple[int, int]) -> bool:
        """checks if snake has collided with food"""
        return move == self.food

    def record_move(self, move: tuple[int, int]) -> bool:
        """records move of snake"""
        if self.game_over_():
            
            return False
        elif self.collision_food(move):
            self.snake.make_move(self.food, True)
            self.food = self.spawn_food()

            self.update_possible_moves()


            return True
        else:
            self.snake.make_move(move, False)
            self.update_possible_moves()


            return True

    def valid_move(self, move: tuple[int, int]) -> bool:
        """checks if move is valid and also check if move is in the grid size

        TODO: FIX THIS SPAGHETTI CODE"""
        
        return move in self.possible_moves

    def update_possible_moves(self) -> None:
        """
        updates possible moves
        """
        self.possible_moves = self.grid.get_node(self.snake.snake_head[0], self.snake.snake_head[1]).get_neighbours()
    

    def print_board(self) -> None:
        """prints board"""
        self.grid.print_grid(self.snake, self.food)
        return None

    def get_game_state(self):
        """Returns the current game state."""
        return {
            'grid': self.grid.grid,
            'snake': self.snake.snake,
            'food': self.food,
            'game_over': self.game_over
        }

    def reset_game(self):
        """Resets the game to the initial state."""
        self.grid = Grid(self.grid_size)
        self.snake = Snake()
        self.game_over = False
        self.food = (self.grid_size // 2, self.grid_size // 2)

    
    def print_game(self):
        """Prints the current state of the game."""
        for y in range(self.grid_size):
            for x in range(self.grid_size):
                if (x, y) == self.snake.snake_head:
                    print("H", end=" ")
                elif (x, y) in self.snake.snake:
                    print("S", end=" ")
                elif (x, y) == self.food:
                    print("F", end=" ")
                else:
                    print(".", end=" ")
            print()
        print("Score:", self.score())
        if self.game_over:
            print("Game Over!")

    def score(self):
        return len(self.snake.snake)
