def is_valid_move(x, y, n, path):
    """ Check if the next move (x, y) is valid. """
    return (0 <= x < n) and (0 <= y < n) and ((x, y) not in path)

def find_hamiltonian_cycle(n, path, x, y, dx, dy):
    """ Try to find a Hamiltonian cycle in an n x n grid. """
    if len(path) == n*n:
        # Check if the last vertex is adjacent to the first vertex to form a cycle.
        if (path[0][0] - x, path[0][1] - y) in zip(dx, dy):
            return path
        else:
            return None
    
    # Try all possible movements
    for i in range(4):
        next_x, next_y = x + dx[i], y + dy[i]
        if is_valid_move(next_x, next_y, n, path):
            path.append((next_x, next_y))  # Make move
            result = find_hamiltonian_cycle(n, path, next_x, next_y, dx, dy)
            if result is not None:
                return result  # If cycle is found
            path.pop()  # Backtrack if no cycle is found from this move
    
    return None

def hamiltonian_cycle(n):
    """ Wrapper function to setup and start the backtracking algorithm for finding a Hamiltonian cycle. """
    # Possible movements: right, down, left, up
    dx = [1, 0, -1, 0]
    dy = [0, 1, 0, -1]

    # Start from the top-left corner of the grid (0,0)
    path = [(0, 0)]
    return find_hamiltonian_cycle(n, path, 0, 0, dx, dy)

# Start with a 3x3 grid
n = 12
cycle = hamiltonian_cycle(n)
print(cycle)
