from a_star import AStarSearch, HeuristicType
import random
from utils import get_random_config, get_random_goal_using_start

dif_tot = 0

for _ in range(100):
    print("================= Iteration number:", _, "=================")
    n = random.randint(2, 4)

    start_config = get_random_config(n)
    goal_config = get_random_goal_using_start(start_config)
    print("Start:", start_config)
    print("Goal: ", goal_config)

    a_star_misplaced = AStarSearch(start_config, goal_config, cost_type=HeuristicType.MISPLACED)
    a_star_manhattan = AStarSearch(start_config, goal_config, cost_type=HeuristicType.MANHATTAN)

    print("Misplaced path:", a_star_misplaced.search())
    print("Manhattan path:", a_star_manhattan.search())

    print("Misplaced Time:", a_star_misplaced.time)
    print("Manhattan Time:", a_star_manhattan.time)

    difference = a_star_misplaced.iter_count - a_star_manhattan.iter_count
    print("Misplaced iterations:", a_star_misplaced.iter_count)
    print("Manhattan iterations:", a_star_manhattan.iter_count)

    dif_tot += difference

print("Difference Average: ", dif_tot/100)
