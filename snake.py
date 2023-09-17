class Snake:
    """Snake"""
    snake: list[tuple[int, int]]
    direction: str
    alive: bool
    snake_head: tuple[int, int]
    snake_tail: tuple[int, int]

    def __init__(self):
        self.snake = [(0, 0)]
        self.direction = 'Right'
        self.alive = True
        self.snake_head = self.snake[0]
        self.snake_tail = self.snake[0]

    def make_move(self, tup: tuple[int, int], food: bool) -> None:
        """Make a move"""
        if food:
            self.snake.append(tup)
            self.snake_head = tup
        
        else:
            self.snake.append(tup)
            self.snake_head = tup
            self.snake.pop(0)
            self.snake_tail = self.snake[0]


    def update_direction(self, move: tuple[int, int]) -> bool:
        """Updates direction
        Potentiallu useless"""
        if self.snake_head[0] - move[0] == 1:
            self.direction = 'Left'
        elif self.snake_head[0] - move[0] == -1:
            self.direction = 'Right'
        elif self.snake_head[1] - move[1] == 1:
            self.direction = 'Up'
        elif self.snake_head[1] - move[1] == -1:
            self.direction = 'Down'
        else:
            raise ValueError("Invalid move")

        return True
