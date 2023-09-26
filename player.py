from game import Game
import random
import heapq
from collections import deque


game = Game(9)


class Player():

    def make_move():
        """Makes a move"""
        raise NotImplementedError
    


class Human(Player):
    """Human player"""

    def make_move(self, game:Game) -> tuple[int, int] :
        chosen = random.choice(game.possible_moves)

        print(chosen)
        return chosen
    

class Djaktra(Player):
    """Uses Djaktra algo to make a move"""

    def make_move(self, game:Game) -> tuple[int, int] :
        start = game.snake.snake_head
        goal = game.food

        distance = {start: 0} 
        came = {}

        open_list = [(distance[start], start)]
        closed_list = set()

        while  open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came, current)
            

            closed_list.add(current)

            node = game.grid.get_node(current[0], current[1])
            neighbours = [neigh for neigh in node.get_neighbours() if neigh not in game.snake.snake[:-1] or neigh == game.snake.snake_tail]

            
            for neighbor in neighbours:

                if neighbor in closed_list:
                    continue

                tentative_distance = distance[current] + 1

                if neighbor not in distance or tentative_distance < distance[neighbor]:
                    came[neighbor] = current
                    distance[neighbor] = tentative_distance
                    heapq.heappush(open_list, (distance[neighbor] , neighbor))

        immediate_neighbours = game.grid.get_node(start[0], start[1]).get_neighbours()
        safe_moves = [move for move in immediate_neighbours if move not in game.snake.snake[:-1] or move == game.snake.snake_tail]

        return random.choice(safe_moves) if safe_moves else random.choice(immediate_neighbours)


    def reconstruct_path(self, came_from: dict[tuple[int, int], tuple[int, int]], start: tuple[int, int]) -> tuple[int, int]:
        # Return the next step to take from the start node to the goal
        current = start
        while current in came_from:
            next_move = current
            current = came_from[current]
        return next_move
        


class  A_star(Player):
    """ Uses A_star algo to make a move """


    def make_move(self, game: Game) -> tuple[int, int]:
        start = game.snake.snake_head
        goal = game.food

        # Initialize both the actual distance and estimated distance to the goal
        g_score = {start: 0}
        f_score = {start: self.heuristic(start, goal)}

        open_list = [(f_score[start], start)]
        came_from = {}
        closed_list = set()

        while open_list:
            _, current = heapq.heappop(open_list)

            if current == goal:
                return self.reconstruct_path(came_from, start)

            closed_list.add(current)

            node = game.grid.get_node(current[0], current[1])
            neighbours = [neigh for neigh in node.get_neighbours() if neigh not in game.snake.snake[:-1] or neigh == game.snake.snake_tail]

            for neighbour in neighbours:
                if neighbour in closed_list:
                    continue

                tentative_g_score = g_score[current] + 1

                if neighbour not in g_score or tentative_g_score < g_score[neighbour]:
                    came_from[neighbour] = current
                    g_score[neighbour] = tentative_g_score
                    f_score[neighbour] = g_score[neighbour] + self.heuristic(neighbour, goal)
                    heapq.heappush(open_list, (f_score[neighbour], neighbour))

        immediate_neighbours = game.grid.get_node(start[0], start[1]).get_neighbours()
        safe_moves = [move for move in immediate_neighbours if move not in game.snake.snake[:-1] or move == game.snake.snake_tail]

        return random.choice(safe_moves) if safe_moves else random.choice(immediate_neighbours)
    

    def heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])


class DFS(Player):
    """Uses Depth First Search to make a move"""

    def make_move(self, game: Game) -> tuple[int, int]:
        start = game.snake.snake_head
        goal = game.food
        visited = set()
        path = []

        if self.dfs(game, start, goal, visited, path):
            return path[1]
        else:
            immediate_neighbours = game.grid.get_node(start[0], start[1]).get_neighbours()
            safe_moves = [move for move in immediate_neighbours if move not in game.snake.snake[:-1] or move == game.snake.snake_tail]
            return random.choice(safe_moves) if safe_moves else random.choice(immediate_neighbours)

    def dfs(self, game: Game, current: tuple[int, int], goal: tuple[int, int], visited: set, path: list) -> bool:
        if current == goal:
            return True

        if current in visited:
            return False

        visited.add(current)

        node = game.grid.get_node(current[0], current[1])
        neighbours = [neigh for neigh in node.get_neighbours() if neigh not in game.snake.snake[:-1] or neigh == game.snake.snake_tail]

        for neighbour in neighbours:
            if neighbour not in visited:
                path.append(neighbour)
                if self.dfs(game, neighbour, goal, visited, path):
                    return True
                path.pop()

        return False


class BFS(Player):
    """Uses Breadth First Search to make a move"""

    def make_move(self, game: Game) -> tuple[int, int]:
        start = game.snake.snake_head
        goal = game.food

        visited = set()
        queue = deque([(start, [])])

        while queue:
            current, path = queue.popleft()

            if current == goal:
                if path:
                    return path[0]  # Return the first move in the path
                else:
                    break  # No path found

            if current in visited:
                continue

            visited.add(current)

            node = game.grid.get_node(current[0], current[1])
            neighbours = [neigh for neigh in node.get_neighbours() if neigh not in game.snake.snake[:-1] or neigh == game.snake.snake_tail]

            for neighbour in neighbours:
                if neighbour not in visited:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append((neighbour, new_path))

        # If no path is found, try to make a safe move
        immediate_neighbours = game.grid.get_node(start[0], start[1]).get_neighbours()
        safe_moves = [move for move in immediate_neighbours if move not in game.snake.snake[:-1] or move == game.snake.snake_tail]
        return random.choice(safe_moves) if safe_moves else random.choice(immediate_neighbours)
    


class FloodFill(Player):
    """Uses Flood Fill to determine the amount of open space"""

    def flood_fill(self, game: Game, start: tuple[int, int]) -> int:
        """Return the number of open cells connected to the start cell"""

        visited = set()
        queue = deque([start])
        count = 0

        while queue:
            current = queue.popleft()
            count += 1

            node = game.grid.get_node(current[0], current[1])
            neighbours = [neigh for neigh in node.get_neighbours() if neigh not in game.snake.snake[:-1] or neigh == game.snake.snake_tail]

            for neighbour in neighbours:
                if neighbour not in visited:
                    visited.add(neighbour)
                    queue.append(neighbour)

        return count

    def make_move(self, game: Game) -> tuple[int, int]:
        # For demonstration purposes, let's just print the open space size and then choose a random move
        open_space = self.flood_fill(game, game.snake.snake_head)
        print(f"Open space size: {open_space}")

        # Make a move (here, for simplicity, we'll make a random move)
        immediate_neighbours = game.grid.get_node(game.snake.snake_head[0], game.snake.snake_head[1]).get_neighbours()
        safe_moves = [move for move in immediate_neighbours if move not in game.snake.snake[:-1] or move == game.snake.snake_tail]
        return random.choice(safe_moves) if safe_moves else random.choice(immediate_neighbours)
    

class AI_Hamiltonian_Dijkstra(Player):
    """Uses Dijkstra's algorithm with a Hamiltonian cycle backup"""

    def __init__(self):
        self.cycle = self.generate_hamiltonian_cycle(self.game.grid.size)
        self.path = []  # To store the current path
        self.target = None  # To store the current target (either food or a point on the cycle)

    def shortest_path(self, game, start, end):
        """Compute the shortest path using Dijkstra's algorithm"""
        grid = game.grid
        visited = set()
        distances = {point: float('infinity') for point in self.cycle}
        distances[start] = 0
        queue = [(0, start)]

        while queue:
            current_dist, current_point = heapq.heappop(queue)
            if current_point in visited:
                continue
            if current_point == end:
                break

            visited.add(current_point)
            for neighbour in grid.get_node(current_point[0], current_point[1]).get_neighbours():
                if neighbour not in visited and neighbour not in game.snake.snake[:-1]:  # Exclude snake body
                    new_dist = current_dist + 1
                    if new_dist < distances[neighbour]:
                        distances[neighbour] = new_dist
                        heapq.heappush(queue, (new_dist, neighbour))

        # Reconstruct the path from the end to the start
        path = []
        while end:
            path.append(end)
            end = min(grid.get_node(end[0], end[1]).get_neighbours(), key=lambda p: distances.get(p, float('infinity')))
        path.reverse()
        return path

    def nearest_cycle_point(self, game):
        """Find the nearest point on the cycle to the snake's head"""
        head = game.snake.snake_head
        return min(self.cycle, key=lambda point: abs(point[0] - head[0]) + abs(point[1] - head[1]))

    def make_move(self, game: Game) -> tuple[int, int]:
        head = game.snake.snake_head
        food = game.food

        # If we're not currently following a path or if we've reached the target
        if not self.path or head == self.target:
            if head != food and self.shortest_path(game, head, food):
                # If there's a path to the food, set the food as the target and compute the path
                self.target = food
                self.path = self.shortest_path(game, head, food)
            else:
                # Otherwise, compute the path back to the nearest point on the Hamiltonian cycle
                self.target = self.nearest_cycle_point(game)
                self.path = self.shortest_path(game, head, self.target)

        # Follow the path
        next_move = self.path.pop(0)
        return next_move
    

    def generate_hamiltonian_cycle(grid_size):
        cycle = []
        for i in range(grid_size):
            if i % 2 == 0:  # Even rows
                for j in range(grid_size):
                    cycle.append((i, j))
            else:  # Odd rows
                for j in range(grid_size - 1, -1, -1):
                    cycle.append((i, j))
        return cycle