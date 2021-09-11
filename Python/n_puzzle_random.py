from a_star import AStarSearch, HeuristicType
import random
from utils import get_random_config, get_random_goal_using_start, print_matrix

dif_tot = 0
dif_sq_tot = 0

for _ in range(100):
    print("================= Iteration number:", _, "=================")
    n = random.randint(3, 4)

    start_config = get_random_config(n)
    goal_config = get_random_goal_using_start(start_config)
    print("Start:")
    print_matrix(start_config)
    print("\nGoal:")
    print_matrix(goal_config)

    a_star_misplaced = AStarSearch(start_config, goal_config, cost_type=HeuristicType.MISPLACED)
    a_star_manhattan = AStarSearch(start_config, goal_config, cost_type=HeuristicType.MANHATTAN)

    print("Misplaced path:", a_star_misplaced.search())
    print("Manhattan path:", a_star_manhattan.search())

    print("Misplaced Time:", a_star_misplaced.time)
    print("Manhattan Time:", a_star_manhattan.time)

    print("Misplaced iterations:", a_star_misplaced.iter_count)
    print("Manhattan iterations:", a_star_manhattan.iter_count)

    difference = a_star_misplaced.iter_count - a_star_manhattan.iter_count
    dif_tot += difference
    dif_sq_tot += difference * difference

mean = dif_tot/100
std_dev = (dif_sq_tot/99 - dif_tot * dif_tot/9900) ** 0.5

print("\n\n================= Results =================")
print("Mean Difference:", mean)
print("Standard deviation:", std_dev)
print("Calculated T-value:", (mean - 0)/std_dev * 10)
