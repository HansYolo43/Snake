""" Grid for the game will be represented as Graphs containing """
from __future__ import annotations

from typing import Optional


class Grid:
    """ Grid
    """
    size: int
    grid: list[list[Node]]

    def __init__(self, size: Optional[int] = 9) -> None:
        """
        Initialize the grid with the given size.
        """
        self.size = size
        self.grid = [[Node(x, y) for y in range(size)] for x in range(size)]

        for column in self.grid:
            for stone in column:
                if stone.x + 1 < size:
                    stone.add_neighbour(self.get_node(stone.x + 1, stone.y))
                if stone.x - 1 >= 0:
                    stone.add_neighbour(self.get_node(stone.x - 1, stone.y))
                if stone.y + 1 < size:
                    stone.add_neighbour(self.get_node(stone.x, stone.y + 1))
                if stone.y - 1 >= 0:
                    stone.add_neighbour(self.get_node(stone.x, stone.y - 1))

    def get_node(self, x: int, y: int) -> Node:
        """Return the node at the given coordinates."""
        return self.grid[x][y]

    def print_grid(self, snake, food):
        """Print the grid"""
        for y in range(self.size):
            for x in range(self.size):
                if (x, y) == snake.snake_head:
                    print("H", end=" ")
                elif (x, y) in snake.snake:
                    print("S", end=" ")
                elif (x, y) == food:
                    print("F", end=" ")
                else:
                    print(".", end=" ")
            print()
        print()


class Node:
    """ A point on the grid.
    Attributes:
        neighbours (dict[tuple[int, int], Node]): A dictionary of the neighbouring points.
        occupied (bool): Whether the point is occupied by snake.
        x (int): The x coordinate of the point.
        y (int): The y coordinate of the point.
    """
    x: int
    y: int
    neighbours: dict[tuple[int, int], Node]
    occupied: bool

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.neighbours = {}
        self.occupied = False

    def add_neighbour(self, neighbour: Node) -> None:
        """
        Adds a neighbour to the stone if it is adjacent to the stone.

        Args:
            neighbour (Stone): The neighbouring stone to add.
        """
        # Check if the neighbor is adjacent to the current stone
        if abs(self.x - neighbour.x) + abs(self.y - neighbour.y) == 1:
            self.neighbours[neighbour.x, neighbour.y] = neighbour
            neighbour.neighbours[self.x, self.y] = self
        else:
            raise Exception

    def get_neighbours(self) -> list[tuple[int, int]]:
        """Return the neighbours of the stone"""
        cords = []
        for key in self.neighbours:
            cords.append(key)
        return cords
