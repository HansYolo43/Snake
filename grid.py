""" Grid for the game will be represented as Graphs containing """
from __future__ import annotations

from typing import Optional, List, Tuple


class Grid:
    """ Grid
    """
    size: int
    grid: list[list[Node]]
    cycle: list[tuple]

    def __init__(self, size: Optional[int] = 9) -> None:
        """
        Initialize the grid with the given size.
        """
        self.size = size
        self.grid = [[Node(x, y) for y in range(size)] for x in range(size)]
        self.cycle = self.hamiltonian_cycle(size)

        for column in self.grid:
            for point in column:
                if point.x + 1 < size:
                    point.add_neighbour(self.get_node(point.x + 1, point.y))
                if point.x - 1 >= 0:
                    point.add_neighbour(self.get_node(point.x - 1, point.y))
                if point.y + 1 < size:
                    point.add_neighbour(self.get_node(point.x, point.y + 1))
                if point.y - 1 >= 0:
                    point.add_neighbour(self.get_node(point.x, point.y - 1))

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

    def is_valid_move(self, x, y, n, path):
        """ Check if the next move (x, y) is valid. """
        return (0 <= x < n) and (0 <= y < n) and ((x, y) not in path)

    def find_hamiltonian_cycle(self, n, path, x, y, dx, dy):
        """ Try to find a Hamiltonian cycle in an n x n grid. """
        if len(path) == n*n:
        
            if (path[0][0] - x, path[0][1] - y) in zip(dx, dy):
                return path
            else:
                return None
        

        for i in range(4):
            next_x, next_y = x + dx[i], y + dy[i]
            if self.is_valid_move(next_x, next_y, n, path):
                path.append((next_x, next_y))  # Make move
                result = self.find_hamiltonian_cycle(n, path, next_x, next_y, dx, dy)
                if result is not None:
                    return result  # If cycle is found
                path.pop()  # Backtrack if no cycle is found from this move
        
        return None

    def hamiltonian_cycle(self, n):
        """ Wrapper function to setup and start the backtracking algorithm for finding a Hamiltonian cycle. """
        
        dx = [1, 0, -1, 0]
        dy = [0, 1, 0, -1]

        path = [(0, 0)]
        return self.find_hamiltonian_cycle(n, path, 0, 0, dx, dy)


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
        Adds a neighbour to the point if it is adjacent to the point.

        Args:
            neighbour (point): The neighbouring point to add.
        """
        # Check if the neighbor is adjacent to the current point
        if abs(self.x - neighbour.x) + abs(self.y - neighbour.y) == 1:
            self.neighbours[neighbour.x, neighbour.y] = neighbour
            neighbour.neighbours[self.x, self.y] = self
        else:
            raise Exception

    def get_neighbours(self) -> list[tuple[int, int]]:
        """Return the neighbours of the point"""
        cords = []
        for key in self.neighbours:
            cords.append(key)
        return cords


