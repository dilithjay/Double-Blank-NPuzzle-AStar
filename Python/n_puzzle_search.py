from a_star import AStarSearch, HeuristicType
from utils import get_input_matrix, get_random_config, get_blanks

n = int(input("Enter value of n: "))

print("Enter start config:")
start = get_input_matrix(n)
print("Enter goal config:")
goal = get_input_matrix(n)

a_star = AStarSearch(start, goal, cost_type=HeuristicType.MISPLACED)
print("Steps:", a_star.search())
print("Time:", a_star.time)
print("Checked Node count:", a_star.iter_count)


"""
# Uncomment to define  inputs manually.

start = [['-', '1', '6', '14'], ['7', '4', '5', '2'], ['3', '11', '8', '9'], ['12', '-', '13', '10']]
blank = [[0, 0], [3, 1]]
goal = [['12', '10', '2', '1'], ['5', '4', '7', '9'], ['-', '11', '8', '13'], ['6', '-', '3', '14']]
"""


"""
# Uncomment to get random configurations

start = get_random_config(n)
print(start)

blank = get_blank(start)
print(blank)

goal = get_random_config(n)
print(goal)
"""
