from game import Game
import random
import heapq
from collections import deque


class Player():
    

    def make_move(self, game: Game):
        """Makes a move"""
        raise NotImplementedError


class Random(Player):
    """Human player"""

    def make_move(self, game: Game) -> tuple[int, int]:
        chosen = random.choice(game.possible_moves)

        
        return chosen


class Djaktra(Player):
    """Uses Djaktra algo to make a move"""

    def make_move(self, game: Game) -> tuple[int, int]:
        start = game.snake.snake_head
        goal = game.food

        distance = {start: 0}
        came = {}

        open_list = [(distance[start], start)]
        closed_list = set()

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came, current)

            closed_list.add(current)

            node = game.grid.get_node(current[0], current[1])
            neighbours = [neigh for neigh in node.get_neighbours() if
                          neigh not in game.snake.snake[:-1] or neigh == game.snake.snake_tail]

            for neighbor in neighbours:

                if neighbor in closed_list:
                    continue

                tentative_distance = distance[current] + 1

                if neighbor not in distance or tentative_distance < distance[neighbor]:
                    came[neighbor] = current
                    distance[neighbor] = tentative_distance
                    heapq.heappush(open_list, (distance[neighbor], neighbor))

        immediate_neighbours = game.grid.get_node(start[0], start[1]).get_neighbours()
        safe_moves = [move for move in immediate_neighbours if
                      move not in game.snake.snake[:-1] or move == game.snake.snake_tail]

        return random.choice(safe_moves) if safe_moves else random.choice(immediate_neighbours)

    def reconstruct_path(self, came_from: dict[tuple[int, int], tuple[int, int]], start: tuple[int, int]) -> tuple[
        int, int]:
        # Return the next step to take from the start node to the goal
        current = start
        while current in came_from:
            next_move = current
            current = came_from[current]
        return next_move


class A_star(Player):
    """ Uses A_star algo to make a move """

    def make_move(self, game: Game) -> tuple[int, int]:
        start = game.snake.snake_head
        goal = game.food

        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        open_list = [(f_score[start], start)]
        came_from = {}
        closed_list = set()

        if self.heuristic(start, goal) == 1:
            return goal

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came_from, current)

            closed_list.add(current)

            node = game.grid.get_node(current[0], current[1])
            neighbours = [neigh for neigh in node.get_neighbours()
                          if neigh not in game.snake.snake]

            for neighbour in neighbours:
                if neighbour in closed_list:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = g_score[neighbour] + self.heuristic(neighbour, goal)
                    heapq.heappush(open_list, (f_score[neighbour], neighbour))

        safe_moves = game.possible_moves
        return random.choice(safe_moves)

    def heuristic(self, a: tuple[int, int], b: tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.insert(0, current)
        return path[1]  # return the next step towards the goal

class DFS(Player):
    """Uses Depth First Search to make a move"""

    def make_move(self, game: Game) -> list[tuple[int, int]]:
        start = game.snake.snake_head
        goal = game.food
        visited = set()
        path = []

        # Perform DFS and find a path
        if self.dfs(game, start, goal, visited, path):
            return path[1:]  # Skip the first element.
        else:
            return []  # Return an empty path

    def dfs(self, game: Game, current: tuple[int, int], goal: tuple[int, int], visited: set, path: list) -> bool:
        # Add the current position to the path and visited nodes
        path.append(current)
        visited.add(current)

        # If the current position is the goal, we found path
        if current == goal:
            return True

        # Get valid neighbors, considering the game rules.
        node = game.grid.get_node(current[0], current[1])
        neighbors = [neighbor for neighbor in node.get_neighbours() if neighbor not in visited and neighbor not in game.snake.snake]

        # Explore each neighbor for a valid path
        for neighbor in neighbors:
            if self.dfs(game, neighbor, goal, visited, path):
                return True

        # If none of the neighbors lead to a solution, backtrack
        path.pop()
        return False


class BFS(Player):
    """Uses Breadth First Search to make a move
    Returns the path from the snake's head to the food, not including the start position."""

    def make_move(self, game: Game) -> list[tuple[int, int]]:
        start = game.snake.snake_head
        goal = game.food

        visited = set()
        queue = deque([(start, [])])  # Queue holds the node and the path

        while queue:
            current, path = queue.popleft()

            # If the goal is found, 
            if current == goal:
                return path  

            if current in visited:
                continue

            visited.add(current)

            node = game.grid.get_node(current[0], current[1])
            neighbours = [neigh for neigh in node.get_neighbours() if neigh not in game.snake.snake]

            for neighbour in neighbours:
                if neighbour not in visited:
                    
                    queue.append((neighbour, path + [neighbour])) 



class Hamiltonin(Player):
    """Uses Hamiltonian cycle generated by grid to give a path"""

    def make_move(self, game: Game) -> list[tuple[int, int]]:

        cycle = game.grid.cycle

        index1 = 0
        index2 = len(cycle) - 1

        for node in cycle:
            if cycle[index1] == game.snake.snake_head and cycle[index2] == game.food:
                break
            if cycle[index2] != game.food:
                index2 -= 1
            if cycle[index1] != game.snake.snake_head:
                index1 += 1

        index1 += 1
        index2 += 1


        if index1 < index2:
            path = cycle[index1:index2 + 1]
        else:
            path = cycle[index1:] + cycle[:index2 + 1]


        return path

