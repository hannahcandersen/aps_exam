import os
import random
import math

n = 50  # maximum number of candles
m = 15  # maximum number of cuts
r = 100  # maximum radius


# Generate random candles while adhering to the specified constraints
candles = set() # Use a set to ensure distinct candles
while len(candles) < n:
    # Generate coordinates (x, y) such that x^2 + y^2 < r^2
    x = random.randint(-r, r)
    y = random.randint(-r, r)
    if x**2 + y**2 < r**2: # Check if the point is inside the circle
        candles.add((x, y))


# Generate random lines while adhering to the specified constraints
lines = set() # Use a set to ensure distinct lines
while len(lines) < m:
    a = b = 0
    while a == 0 and b == 0:  # Ensure at least one of a or b is non-zero
        a = random.randint(-100, 100)
        b = random.randint(-100, 100)
    
    # Calculate the maximum |c| that ensures the line crosses the circle
    max_c = int(r * math.sqrt(a**2 + b**2))  # Ensure |c| < r * sqrt(a^2 + b^2) to intersect the circle
    
    # Randomly choose c within the valid range
    c = random.randint(-max_c, max_c)

    line = (a, b, c)
    # Add the line if it's not already in the set (ensuring distinct lines)
    lines.add(line)



# Write to file in current folder
file_name = "worst_case4.in"
current_directory = os.getcwd()
file_path = os.path.join(current_directory, file_name)

with open(file_path, "w") as f:
    f.write(f"{n} {m} {r}\n")
    for candle in candles:
        f.write(" ".join(map(str, candle)) + "\n")
    for line in lines:
        f.write(" ".join(map(str, line)) + "\n")