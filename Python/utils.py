import random


def get_input_matrix(length):
    """Take 2D list as input and return list."""
    matrix = []

    for _ in range(length):
        row = input().split()
        matrix.append(row)

    return matrix


def get_random_config(size):
    """Create a random configuration of the given size with 2 blank positions and return random configuration."""
    arr = list(map(str, range(1, size * size - 1))) + ['-', '-']
    random.shuffle(arr)
    config = []
    for i in range(size):
        config.append(arr[i * size: (i + 1) * size])
    return config


def get_possible_directions(blank, size):
    """Get possible move directions for a given blank position."""
    dirs = []
    r, c = blank
    if r != 0:
        dirs.append((-1, 0))
    if r < size - 1:
        dirs.append((1, 0))
    if c != 0:
        dirs.append((0, -1))
    if c < size - 1:
        dirs.append((0, 1))
    return dirs


def get_random_goal_using_start(start):
    """Generate a random goal matrix by making a random number of moves on the start matrix in random directions."""
    size = len(start)
    blanks = get_blanks(start)
    goal = get_2d_array_copy(start)
    blank_dirs = [get_possible_directions(blanks[0], size), get_possible_directions(blanks[1], size)]
    for i in range(random.randint(15, 20)):
        blank_no = random.randint(0, 1)
        blank = blanks[blank_no]
        direction = random.choice(blank_dirs[blank_no])
        swap(goal, blank, (blank[0] + direction[0], blank[1] + direction[1]))

    return goal


def get_heuristic_cost_misplaced(current, goal):
    """Get the cost based on the heuristic => Cost = number of tiles in wrong positions."""
    n = len(current)
    cost = 0

    for r in range(n):
        for c in range(n):
            if current[r][c] != goal[r][c]:
                cost += 1
    return cost


def get_heuristic_cost_manhattan(current, goal):
    """Get the cost based on the heuristic => Cost = Manhattan distance of each tile position to its respective
    position of the goal configuration """
    n = len(current)
    cost = 0

    goal_coordinates = {}

    for r in range(n):
        for c in range(n):
            num = goal[r][c]
            if num != '-':
                goal_coordinates[num] = (r, c)

    for r in range(n):
        for c in range(n):
            num = current[r][c]
            if num != '-':
                dst = goal_coordinates[num]
                cost += abs(r - dst[0]) + abs(c - dst[1])

    return cost


def swap(mat, pos1, pos2):
    """Swap the positions of 2 elements in the given matrix."""
    r1, c1 = pos1
    r2, c2 = pos2
    mat[r1][c1], mat[r2][c2] = mat[r2][c2], mat[r1][c1]


def get_2d_array_copy(array):
    """Return a copy of the given 2D array."""
    return [row[:] for row in array]


def get_blanks(matrix):
    """Get a list of blank tiles (of length 2) from the given matrix."""
    length = len(matrix)
    blank = []
    for i in range(length):
        row = matrix[i]
        for j in range(length):
            if row[j] == '-':
                blank.append([i, j])
    return blank


def print_matrix(matrix):
    """Print the matrix in a tabular format"""
    n = len(matrix)
    print("-" * 7 * n + "-")
    for r in range(n):
        print("|" + ("  {:<4}|" * n).format(*matrix[r]))
        print("-" * 7 * n + "-")

