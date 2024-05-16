import math
import time

n, m, r = map(int, input().split())
epsilon = 10**-4
candles = []
lines = []
intersection_points = set()
intersection_points_circle = set()
edges = m


######## METHODS ########
# Find intersection points between a circle and a line
def find_intersection_line_circle(a, b, c, r):
    # ax + by + c = 0   - line
    # x² + y² = r²      - circle

    '''
    Given that the input guarantees no line is tangent to or completely outside the circle,
    we don't have to check the denominator in our calculations, since we will always get two intersection points.
    '''
    
    # The line is vertical, so x is the same for both intersection points
    if b == 0:
        x = -c/a
        # Solve for y in the circle equation
        y1 = math.sqrt(r**2 - x**2)
        y2 = -math.sqrt(r**2 - x**2)
        return {(x, y1), (x, y2)}
    else:
        # Solve for x
        x1 = (-a*c + b*math.sqrt((r**2)*(a**2+b**2)-(c**2)))/(a**2+b**2)
        x2 = (-a*c - b*math.sqrt((r**2)*(a**2+b**2)-(c**2)))/(a**2+b**2)

        # Solve for y
        y1 = (-c - a*x1) / b
        y2 = (-c - a*x2) / b

    return {(x1, y1), (x2, y2)}


# Find intersection point between two lines
def find_intersection_lines(line1, line2, r):
    a1, b1, c1 = line1
    a2, b2, c2 = line2

    denominator = a1*b2 - a2*b1
    if abs(denominator) < epsilon:
        return None  # The lines are parallel and don't intersect
   
    x = (b2*c1 - b1*c2) / denominator
    y = (a1*c2 - a2*c1) / denominator

    if not is_point_in_circle(x, y, r):
        return None # The intersection point is outside the circle

    return (x, y)


# Check if intersection point is inside the circle
def is_point_in_circle(x, y, r):
    '''
    Euclidean distance - sqrt((x2 - x1)^2 + (y2 - y1)^2)
    Since the circle is centered at the origin (0,0), the distance formula can be simplifed to: sqrt(x^2 + y^2)
    '''
    d = math.sqrt(x**2 + y**2)
    return d < r


# Check if there is exactly one candle on each piece
def check_candles(lines):
    candles_on_piece = [set(range(n))] # Initially there is only one set containing all candles.
    
    for line in lines:
        new_cake_pieces = []
        
        for piece in candles_on_piece:
            one_side = set()
            other_side = set()
            
            # Check the candles in the current piece.
            for candle_index in piece:
                candle = candles[candle_index]
                
                '''
                The input guarantees that the candle is not on a line and is inside the circle.
                So we can assume that the candle will be either on one piece or another.
                '''
                if line[0] * candle[0] + line[1] * candle[1] + line[2] > 0:
                    one_side.add(candle_index)
                else:
                    other_side.add(candle_index)
            
            # Add the new pieces to the list of new pieces.
            if one_side:
                new_cake_pieces.append(one_side)
            if other_side:
                new_cake_pieces.append(other_side)
            
        candles_on_piece = new_cake_pieces
    
    print(f'candles_on_piece: {candles_on_piece}')
    print(f'len(candles_on_piece): {len(candles_on_piece)}')
    return all(len(c) == 1 for c in candles_on_piece)



######## START ########
start_time = time.time()
for _ in range(n):
    (x,y) = map(int, input().split())
    candles.append((x,y))


for _ in range(m):
    (a, b, c) = map(int, input().split())

    ######## FIND CAKE PIECES ########
    inters_circle = find_intersection_line_circle(a, b, c, r)
    
    intersection_points_circle.update(inters_circle)
    intersection_points.update(inters_circle)


    if len(lines) != 0: # If it's not the first line encountered, check for intersections with the new line and all previous lines
        for j in range(len(lines)):
            inters_line = find_intersection_lines((a, b, c), lines[j], r)
            
            if inters_line: # If there is an intersection point
                if inters_line not in intersection_points:
                    edges += 2  # Increment edges by 2 because two new edges are created
                else:
                    edges += 1 # Increment edges by 1 because one new edge is created, since the intersection point already exists
                intersection_points.add(inters_line)

    lines.append((a, b, c))



# Add the edges from the circle
edges += len(intersection_points_circle)

# Euler's formula: F = E-V+1 (only 1, because we don't want to count the infinite area outside the cake)
cake_pieces = edges - len(intersection_points) + 1


print(f'cake_pieces: {cake_pieces}')

if cake_pieces > n:
    end_time = time.time()
    print('no')
    print(f'time: {end_time - start_time}')
elif check_candles(lines) and n == cake_pieces:
   end_time = time.time()
   print('yes')
   print(f'time: {end_time - start_time}')
else:
    end_time = time.time()
    print('no')
    print(f'time: {end_time - start_time}')