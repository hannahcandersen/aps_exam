import math
import cmath
import time

class Point:
    def __init__(self, x, y):
        self.complex = complex(x, y)

class Segment:
    def __init__(self, a, b, c, start, end):
        self.a = a
        self.b = b
        self.c = c
        if start.complex.real <= end.complex.real:
            self.start = start
            self.end = end
        else:
            # Ensure that the start point is always the leftmost point
            self.start = end
            self.end = start

n, m, r = map(int, input().split())
epsilon = 10**-4
candles = []
lines = []
edges = m
intersection_circle = set()
candles_on_piece = [set(range(n))] # Initially there is only one set containing all candles.


# Solve for intersection points between a circle and a line
def intersection_line_circle(a, b, c, r):
    line = complex(a, b)
    distance = abs(a * 0 + b * 0 + c) / abs(line)  # Distance from origin to line
    if distance > r:
        return []
    angle = cmath.phase(-line.conjugate() * complex(c, 0))
    point_distance = math.sqrt(r**2 - distance**2)
    intersection1 = cmath.rect(point_distance, angle)
    intersection2 = cmath.rect(-point_distance, angle)
    return [Point(intersection1.real, intersection1.imag), Point(intersection2.real, intersection2.imag)]
    

# Solve for intersection point between two lines
def intersection_line_line(line1, line2, r):
    # Extract line coefficients
    a1, b1, c1 = line1.a, line1.b, line1.c
    a2, b2, c2 = line2.a, line2.b, line2.c

    # Form the complex coefficients for both lines
    coef1 = complex(a1, b1)
    coef2 = complex(a2, b2)

    # The determinant of the system (analogous to cross product in complex plane)
    determinant = cross_product(coef1, coef2)
    if abs(determinant) < epsilon:  # Lines are parallel or coincident
        return None

    # Solving the system using Cramer's rule adapted to complex numbers
    # The system: a1*x + b1*y = -c1 and a2*x + b2*y = -c2 can be seen as:
    # [a1 b1] [x] = [-c1]
    # [a2 b2] [y]   [-c2]
    # Determinant should not be zero here (not parallel)
    # Inverse of complex coefficient matrix is used to find intersection
    inv_det = 1 / determinant
    intersect_x = (-c1 * b2 - (-c2) * b1) * inv_det
    intersect_y = (a1 * (-c2) - a2 * (-c1)) * inv_det
    intersection_point = Point(intersect_x.real, intersect_y.real)

    # Check if the point is inside the circle
    if is_point_in_circle(intersection_point.complex.real, intersection_point.complex.imag, r):
        return intersection_point
    else:
        return None
    
def is_point_in_circle(point, r):
    """
    Checks if a point (represented as a complex number) is within a circle centered at the origin with radius r.

    Args:
    point (complex): The complex representation of the point (x + yj).
    r (float): The radius of the circle.

    Returns:
    bool: True if the point is inside the circle, False otherwise.
    """
    # Calculate the magnitude of the complex number (distance from origin)
    return abs(point) < r


def cross_product(z1, z2):
    return z1.real * z2.imag - z1.imag * z2.real



def line_sweep(segments, edges):
    events = []  # List to store events (start and end points of segments)
    for segment in segments:
        events.append((segment.start, 'start', segment))
        events.append((segment.end, 'end', segment))

    #for event in events:
    #    print(f'BEFORE SORT: even_type: {event[1]} point: {event[0].x, event[0].y} line: {event[2].a, event[2].b, event[2].c}')
    events.sort(key=lambda event: event[0].real)  # Sort by the x-coordinate of the point in each event tuple
    #for event in events:
    #    print(f'AFTER SORT: even_type: {event[1]} point: {event[0].x, event[0].y} line: {event[2].a, event[2].b, event[2].c}')


    active_segments = set()  # Set to keep track of active segments
    intersections = set()  # Set to store intersection points

    for event in events:
        _, event_type, segment = event
        if event_type == 'start':
            for active_segment in active_segments:
                intersection_point = intersection_line_line(segment, active_segment, r)
                if intersection_point is not None: # If the lines intersect
                    if intersection_point not in intersections:
                        edges += 2  # Increment edges by 2 because two new edges are created
                    else:
                        edges += 1 # Increment edges by 1 because one new edge is created, since the intersection point already exists
                    intersections.add(intersection_point)

            active_segments.add(segment)
        else:  # event_type == 'end'
            active_segments.remove(segment)

    return intersections, edges



def check_candles(candles_on_piece, line):
    # Initialize a new list to hold the divided pieces after each cut.
    new_cake_pieces = []
    a, b, c = segment.a, segment.b, segment.c
    line_vector = complex(a, b)
    line_const = complex(c, 0)
    

    for piece in candles_on_piece:
        one_side = set()
        other_side = set()
        
    
        for candle_index in piece:
            candle = candles[candle_index]
            candle_point = complex(candle[0], candle[1])
            
            # Calculate the position of the candle relative to the cutting line.
            position = cross_product(line_vector, candle_point) - c
            if position > 0:
                one_side.add(candle_index)
            else:
                other_side.add(candle_index)
        
        if one_side:
            new_cake_pieces.append(one_side)
        if other_side:
            new_cake_pieces.append(other_side)

    
    # Update the list of pieces to the newly created pieces after the cut.
    return new_cake_pieces



# Read the coordinates of the candles - n times
start_time = time.time()
for _ in range(n):
    (x,y) = map(int, input().split())
    candles.append((x,y))

for _ in range(m):
    (a, b, c) = map(int, input().split())
    point1, point2 = intersection_line_circle(a, b, c, r)

    intersection_circle.update((point1, point2))
    segment = Segment(a, b, c, point1, point2)
    lines.append(segment)


intersections, e = line_sweep(lines, edges)
result = len(intersections) + len(intersection_circle)
for each in lines:
    # Iterate over each cutting line provided in the input.
    candles_on_piece = check_candles(candles_on_piece, each)


# Add the edges from the circle
e += len(intersection_circle)

#F = E-V+1
cake_pieces = e - result + 1

if all(len(s) == 1 for s in candles_on_piece) and len(candles_on_piece) == cake_pieces:
   end_time = time.time()
   print('yes')
   print(f'time: {end_time - start_time}')
else:
    end_time = time.time()
    print('no')
    print(f'time: {end_time - start_time}')

