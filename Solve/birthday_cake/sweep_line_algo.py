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


# Calculate intersection points between a circle and a line
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

    return [Point(x1, y1), Point(x2, y2)]
    

# Calculate intersection point between two lines
def intersection_line_line(line1, line2, r):
    a1, b1, c1 = line1.a, line1.b, line1.c
    a2, b2, c2 = line2.a, line2.b, line2.c

    denominator = a1*b2 - a2*b1
    if abs(denominator) < epsilon:
        return None  # The lines are parallel and don't intersect
   
    x = (b2*c1 - b1*c2) / denominator
    y = (a1*c2 - a2*c1) / denominator

    if not is_point_in_circle(x, y, r):
        return None # The intersection point is outside the circle

    return Point(x, y)

def is_point_in_circle(x, y, r):
    # Since the circle is centered at the origin (0,0), we can simplify the distance formula to:
    d = math.sqrt(x**2 + y**2)
    return d < r



def line_sweep(segments, edges):
    events = []  # List to store events (start and end points of segments)
    for segment in segments:
        events.append((segment.start, 'start', segment))
        events.append((segment.end, 'end', segment))

    events.sort(key=lambda event: event[0].x)  # Sort by the x-coordinate of the point in each event tuple

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



def check_candles(lines):
    candles_on_piece = [set(range(n))] # Initially there is only one set containing all candles.
    
    for line in lines:
        new_cake_pieces = [] # A new list to hold the divided pieces after each cut.
        
        # Iterate over the existing pieces of cake.
        for piece in candles_on_piece:
            one_side = set()
            other_side = set()
            
            # Iterate over the candle indices in the current piece.
            for candle_index in piece:
                candle = candles[candle_index]
                
                if line.a * candle[0] + line.b * candle[1] + line.c > 0:
                    one_side.add(candle_index)
                else:
                    other_side.add(candle_index)
            
            if one_side:
                new_cake_pieces.append(one_side)
            if other_side:
                new_cake_pieces.append(other_side)

        # Update the list of pieces to the newly created pieces after the cut.
        candles_on_piece = new_cake_pieces
    
    return all(len(c) == 1 for c in candles_on_piece)




#### START ####
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


intersections, edges = line_sweep(lines, edges)
verticies = len(intersections) + len(intersection_circle)

# Add the edges from the circle
edges += len(intersection_circle)

#F = E-V+1
cake_pieces = edges - verticies + 1


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
