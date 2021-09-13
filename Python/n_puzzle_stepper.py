from utils import swap, print_matrix

n = int(input("Enter number of rows: "))
print("Enter start config: ")
start = []
num_dict = {}
for i in range(n):
    row = input().split()
    for j in range(n):
        if row[j] != '-':
            num_dict[row[j]] = (i, j)
    start.append(row)

steps_str = input("Enter pattern: ")
steps = steps_str.split("),(")
steps[0] = steps[0][1:]
steps[-1] = steps[-1][:-1]

dirs = {"up": (-1, 0), "down": (1, 0), "right": (0, 1), "left": (0, -1)}

for i in steps:
    print("Step:", i)
    num, dir_word = i.split(',')
    pos = num_dict[num]
    direction = dirs[dir_word]
    new_pos = (pos[0] + direction[0], pos[1] + direction[1])
    num_dict[num] = new_pos
    swap(start, pos, new_pos)
    print_matrix(start)
