from enum import Enum
from queue import PriorityQueue
from time import time
from utils import get_blanks, get_heuristic_cost_manhattan, get_heuristic_cost_misplaced, get_2d_array_copy, swap

BLANK_COUNT = 2
DIRECTION_COUNT = 4

dirs = [(-1, 0), (1, 0), (0, -1), (0, 1)]
opposite_dirs = ('down', 'up', 'right', 'left')


class HeuristicType(Enum):
    MISPLACED = 1
    MANHATTAN = 2


# A node in the search tree
class State:
    def __init__(self, config, blanks, cost, path):
        self.config = config
        self.blanks = blanks
        self.cost = cost
        self.path = path

    def __lt__(self, other):
        return self.cost <= other.cost


class AStarSearch:
    def __init__(self, start, goal, cost_type=HeuristicType.MISPLACED):
        self.goal = goal
        self.n = len(start)
        self.cost_type = cost_type
        state = State(start, get_blanks(start), self.get_cost(start), ())
        self.open_set = PriorityQueue()
        self.open_set.put(state)
        self.closed_set = set()
        self.iter_count = 0
        self.time = 0

    def search(self) -> str:
        """
        Perform A* search over possibilities of steps.
        :return: Path as a string. Format: (1st number to move, move direction (as word)), (2nd number, direction),...
        """
        start_time = time()
        while not self.open_set.empty():
            self.iter_count += 1
            state = self.open_set.get()
            config = state.config

            if str(config) not in self.closed_set:
                self.closed_set.add(str(config))
            else:
                continue

            path = state.path

            # if cost from heuristic is 0 (goal achieved)
            if state.cost == len(path):
                self.time = time() - start_time
                return ",".join(path)

            for i in range(BLANK_COUNT):
                blank = state.blanks[i]
                for j in range(DIRECTION_COUNT):
                    r, c = blank[0] + dirs[j][0], blank[1] + dirs[j][1]
                    if 0 <= r < self.n and 0 <= c < self.n and config[r][c] != '-':
                        mat = get_2d_array_copy(config)
                        swap(mat, blank, (r, c))
                        cost = self.get_cost(mat)
                        path_new = path + (f"({mat[blank[0]][blank[1]]},{opposite_dirs[j]})",)
                        self.open_set.put(State(mat, [state.blanks[i - 1]] + [[r, c]], cost + len(path_new), path_new))
        return "Failed"

    def get_cost(self, config):
        """
        Get the cost of the given configuration as per the chosen heuristic.
        :param config: Configuration matrix as a 2D list.
        :return: Cost of the input configuration
        """
        if self.cost_type == HeuristicType.MISPLACED:
            return get_heuristic_cost_misplaced(config, self.goal)
        # self.cost_type == HeuristicType.MANHATTAN:
        return get_heuristic_cost_manhattan(config, self.goal)
