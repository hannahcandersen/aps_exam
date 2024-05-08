# Generate worst case input and write it to worst_case.in

import os
import random

# n is max
n = 100

# Generate menu. Randomly generate n prices between 1 and 100 - to keep item prices small
items = [random.randint(1, 1000) for _ in range(n)]

# m is max
m = 1000

# Generate orders. Randomly generate m orders between 1 and 30000
orders = [random.randint(1, 30000) for _ in range(m)]

# Write to file in current folder
file_name = "worst_case.in"
current_directory = os.getcwd()
file_path = os.path.join(current_directory, file_name)

with open(file_path, "w") as f:
    f.write(f"{n}\n")
    f.write(" ".join(map(str, items)) + "\n")
    f.write(f"{m}\n")
    f.write(" ".join(map(str, orders)) + "\n")