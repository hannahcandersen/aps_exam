import math

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
candles_on_piece = [set(range(n))] # Initialize a list of sets to represent pieces of cake. Initially there is only one set containing all candles.



# Solve for intersection points between a circle and a line
def intersection_line_circle(a, b, c, r):
    # ax + by + c = 0   - line
    # x² + y² = r²      - circle

    if b == 0:
        x = -c/a
        # Solve for y in the circle equation: y = sqrt(r^2 - x^2)
        y1 = math.sqrt(r**2 - x**2)
        y2 = -math.sqrt(r**2 - x**2)
        return [(x, y1), (x, y2)]
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
    '''
    If d < r, the point is inside the circle.
    If d > r, the point is outside the circle.
    If d = r, the point is on the boundary of the circle.
    '''
    # math.sqrt((x - h)**2 + (y - k)**2)   -> k,h = center of the circle
    '''
    Fra bogen: Euclidean distance
    The Euclidean distance between two points in the plane is the length of the line segment that connects the two points.
    If the points are (x1, y1) and (x2, y2), then the distance between them is given by the formula:
    d = sqrt((x2 - x1)^2 + (y2 - y1)^2)
    With this we can check if the distance is less than the radius of the circle
    '''
    # Since the circle is centered at the origin (0,0), I can simplify the distance formula to:
    d = math.sqrt(x**2 + y**2)
    return d < r



def line_sweep(segments, edges):
    events = []  # List to store events (start and end points of segments)
    for segment in segments:
        events.append((segment.start, 'start', segment))
        events.append((segment.end, 'end', segment))

    #events.sort()  # Sort the events by x-coordinate
    events.sort(key=lambda event: event[0].x)  # Sorting by the x-coordinate of the point in each event tuple

    active_segments = set()  # Set to keep track of active segments
    intersections = set()  # Set to store intersection points

    for event in events:
        point, event_type, segment = event
        if event_type == 'start':
            for active_segment in active_segments:
                #print(f'active_segment: {active_segment.a}, {active_segment.b}, {active_segment.c}')
                #print(f'segment: {segment.a}, {segment.b}, {segment.c}')
                #print(f'point: {point.x}, {point.y}')
                intersection_point = intersection_line_line(segment, active_segment, 3)
                if intersection_point is not None: # If the lines intersect
                    #print(f'intersection_point: {intersection_point.x}, {intersection_point.y}')
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
                #print(f'result: {line[0] * candle[0] + line[1] * candle[1] + line[2]}')
                one_side.add(candle_index)
                #print(f'side_one: {one_side}')
            # If the result is not positive, it's on the other side.
            # Since the problem guarantees no candle is on a cut line, it's on the other side.
            else:
                other_side.add(candle_index)
                #print(f'side_two: {other_side}')
        
        # If there are candles on one_side of the cut, add this as a new piece.
        if one_side:
            new_cake_pieces.append(one_side)
            #print(f'new_pieces: {new_cake_pieces}')
        # If there are candles on other_side of the cut, add this as a new piece too.
        if other_side:
            new_cake_pieces.append(other_side)
            #print(f'new_pieces: {new_cake_pieces}')

    
    # Update the list of pieces to the newly created pieces after the cut.
    #cake_pieces = new_cake_pieces
    return new_cake_pieces
    #print(f'pieces: {cake_pieces}')



# Read the coordinates of the candles - n times
for i in range(n):
    # O(n)
    (x,y) = map(int, input().split())
    candles.append((x,y))

for i in range(m):
    (a, b, c) = map(int, input().split())
    point1, point2 = intersection_line_circle(a, b, c, 3)

    intersection_circle.update((point1, point2))
    segment = Segment(a, b, c, point1, point2)
    lines.append(segment)



intersections, e = line_sweep(lines, edges)
result = len(intersections) + len(intersection_circle)
for each in lines:
    # Iterate over each cutting line provided in the input.
    candles_on_piece = check_candles(candles_on_piece, each)
    
print(f'intersections: {result}')

# Add the edges from the circle
e += len(intersection_circle)
print(f'edges: {e}')

#F = E-V+1
cake_pieces = e - result + 1
print(f'cake_pieces: {cake_pieces}')

if all(len(s) == 1 for s in candles_on_piece) and len(candles_on_piece) == cake_pieces:
   print('yes')
else:
    print('no')



'''
sweepLineIntersection(Points[0..2n-1]):
1. Sort Points[] from left to right (according to x coordinate)

2. Create an empty Self-Balancing BST T. It will contain 
  all active line Segments ordered by y coordinate.

// Process all 2n points 
3. for i = 0 to 2n-1

    // If this point is left end of its line  
    if (Points[i].isLeft) 
       T.insert(Points[i].line())  // Insert into the tree

       // Check if this points intersects with its predecessor and successor
       if ( doIntersect(Points[i].line(), T.pred(Points[i].line()) )
         return true
       if ( doIntersect(Points[i].line(), T.succ(Points[i].line()) )
         return true

    else  // If it's a right end of its line
       // Check if its predecessor and successor intersect with each other
       if ( doIntersect(T.pred(Points[i].line(), T.succ(Points[i].line()))
         return true
       T.delete(Points[i].line())  // Delete from tree

4. return False
'''