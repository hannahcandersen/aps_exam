import math
import time

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Segment:
    def __init__(self, a, b, c, start, end):
        self.a = a
        self.b = b
        self.c = c
        if start.x <= end.x:
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
    # ax + by + c = 0   - line
    # x² + y² = r²      - circle
    if b == 0:
        x = -c/a
        # Solve for y in the circle equation: y = sqrt(r^2 - x^2)
        y1 = math.sqrt(r**2 - x**2)
        y2 = -math.sqrt(r**2 - x**2)
        return [Point(x, y1), Point(x, y2)]
    else:
        # Solve for x
        x1 = (-a*c + b*math.sqrt((r**2)*(a**2+b**2)-(c**2)))/(a**2+b**2)
        x2 = (-a*c - b*math.sqrt((r**2)*(a**2+b**2)-(c**2)))/(a**2+b**2)
        # Solve for y
        y1 = (-c - a*x1) / b
        y2 = (-c - a*x2) / b

    # Return the intersection points
    return [Point(x1, y1), Point(x2, y2)]
    

# Solve for intersection point between two lines
def intersection_line_line(line1, line2, r):
    # Using cross product
    a1, b1, c1 = line1.a, line1.b, line1.c
    a2, b2, c2 = line2.a, line2.b, line2.c

    denominator = a1*b2 - a2*b1
    if abs(denominator) < epsilon:
        return None  # The lines are parallel and don't intersect
   
    x = (b2*c1 - b1*c2) / denominator
    y = (a1*c2 - a2*c1) / denominator

    if not is_point_in_circle(x, y, r):
        return None # The intersection point is outside the circle

    #return (x, y)
    return Point(x, y)

def is_point_in_circle(x, y, r):
    # Since the circle is centered at the origin (0,0), I can simplify the distance formula to:
    d = math.sqrt(x**2 + y**2)
    return d < r



def line_sweep(segments, edges):
    events = []  # List to store events (start and end points of segments)
    for segment in segments:
        events.append((segment.start, 'start', segment))
        events.append((segment.end, 'end', segment))

    #for event in events:
    #    print(f'BEFORE SORT: even_type: {event[1]} point: {event[0].x, event[0].y} line: {event[2].a, event[2].b, event[2].c}')
    events.sort(key=lambda event: event[0].x)  # Sort by the x-coordinate of the point in each event tuple
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
    
    # Iterate over the existing pieces of cake.
    for piece in candles_on_piece:
        # Create two new sets to hold the candle indices for each side of the cut.
        one_side = set()
        other_side = set()
        
        # Iterate over the candle indices in the current piece.
        for candle_index in piece:
            # Retrieve the candle's coordinates based on its index.
            candle = candles[candle_index]
            
            # Calculate the position of the candle relative to the cutting line.
            # If the result is positive, the candle is on one side of the line.
            if line.a * candle[0] + line.b * candle[1] + line.c > 0:
                one_side.add(candle_index)
            # If the result is not positive, it's on the other side.
            # Since the problem guarantees no candle is on a cut line, it's on the other side.
            else:
                other_side.add(candle_index)
        
        # If there are candles on one_side of the cut, add this as a new piece.
        if one_side:
            new_cake_pieces.append(one_side)
        # If there are candles on other_side of the cut, add this as a new piece too.
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
