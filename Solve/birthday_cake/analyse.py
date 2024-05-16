import time
from birthday_cake import find_intersection_line_circle, find_intersection_lines

def run_solution(m, r, candles, lines, intersection_points, intersection_points_circle, edges, cake_pieces, candles_on_piece):
    for _ in range(m):
        (a, b, c) = map(int, input().split())

        ######## FIND CAKE PIECES ########
        # Add the intersection points for a line and circle
        inters_circle = find_intersection_line_circle(a, b, c, r)
        intersection_points_circle.update(inters_circle)
        intersection_points.update(inters_circle)

        # Add the intersection points for two lines
        if len(lines) != 0: # If there are already lines, check for intersections with the new line
            for j in range(len(lines)):
                inters_line = find_intersection_lines((a, b, c), lines[j], r)
                if inters_line: # If there is an intersection point
                    if inters_line not in intersection_points:
                        edges += 2  # Increment edges by 2 because two new edges are created
                    else:
                        edges += 1 # Increment edges by 1 because one new edge is created, since the intersection point already exists
                    intersection_points.add(inters_line)

        lines.append((a, b, c))



        ######## CHECK CANDLES ########
        new_cake_pieces = []
        
        # Iterate over the existing pieces of cake.
        for piece in candles_on_piece:
            one_side = set()
            other_side = set()
            
            # Iterate over the candle indices in the current piece.
            for candle_index in piece:
                candle = candles[candle_index]
                
                if a * candle[0] + b * candle[1] + c > 0:
                    one_side.add(candle_index)
                else:
                    other_side.add(candle_index)
            
            # Add the new pieces to the list of new pieces.
            if one_side:
                new_cake_pieces.append(one_side)
            if other_side:
                new_cake_pieces.append(other_side)
        
        # Update the list of pieces to the newly created pieces after the cut.
        candles_on_piece = new_cake_pieces
    

    # Add the edges from the circle
    edges += len(intersection_points_circle)

    # Euler's formula: F = E-V+1 (only 1, because we don't want to count the infinite area outside the cake)
    cake_pieces = edges - len(intersection_points) + 1

    if all(len(s) == 1 for s in candles_on_piece) and len(candles_on_piece) == cake_pieces:
        end_time = time.time()
        print(f'yes, {end_time - start_time}')
    else:
        end_time = time.time()
        print(f'no, {end_time - start_time}')



# Simulate the process of cutting the cake
start_time = time.time()

# Initialize
n, m, r = map(int, input().split())
epsilon = 10**-4
candles = []
lines = []
intersection_points = set()
intersection_points_circle = set()
edges = m
cake_pieces = 1
candles_on_piece = [set(range(n))]  # One set containing all candles

for _ in range(n):
    (x,y) = map(int, input().split())
    candles.append((x,y))

# Run the solution with the generated input
run_solution(m, r, candles, lines, intersection_points, intersection_points_circle, edges, cake_pieces, candles_on_piece)
