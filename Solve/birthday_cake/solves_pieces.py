# https://www.youtube.com/watch?v=YtkIWDE36qU
import math
import cmath


n, m, r = map(int, input().split())
epsilon = 10**-4
candles = []
lines = []
intersection_points = set()
intersection_points_circle = set()
edges = m
cake_pieces = 1


'''
1. Initialize an empty list of intersection points
2. For each line:
   1. Solve the system of equations formed by the equation of the circle and the equation of the line to find the intersection points
   2. Add the intersection points to the list
3. Sort the intersection points in clockwise order around the circle
4. Initialize a count of circle pieces to 0
5. Initialize an empty set of encountered lines
6. For each intersection point in the sorted list:
   1. Find the line that the point belongs to
   2. If the line is not in the set of encountered lines, increment the count of circle pieces and add the line to the set
   3. Else, remove the line from the set
7. Return the count of circle pieces
'''

'''
For each line:
   Find the intersection points of the line with other lines
      Check if this intersection point is inside the circle
      If it is, add it to the list of intersection points
      If it is on the circle or outside the circle, ignore it
'''

'''
V-E+F = 2
F = E-V+2 => F = E-V+1
'''



# Solve the system of equations formed by the equation of the circle and the equation of the line to find the intersection points
def find_intersection_circle(a, b, c, r):
   # ax + by + c = 0
   # x² + y² = r²

   # Solve for x
   x1 = (-a*c + b*cmath.sqrt((r**2)*(a**2+b**2)-(c**2)))/(a**2+b**2)
   x2 = (-a*c - b*cmath.sqrt((r**2)*(a**2+b**2)-(c**2)))/(a**2+b**2)

   # Solve for y
   y1 = (-c - a*x1) / b
   y2 = (-c - a*x2) / b

   # Return the intersection points
   print(f'({x1}, {y1}), ({x2}, {y2})')
   #return [(x1, y1), (x2, y2)]
   return {(x1, y1), (x2, y2)}


def find_intersection_lines(line1, line2, r):
   print('find_intersection_lines')
   # using cross product
   # Exactly one intersection point that is not a vertex of any line segment
   a1, b1, c1 = line1
   a2, b2, c2 = line2

   denominator = a1*b2 - a2*b1
   print(f'denominator: {denominator}')
   if denominator == 0: # bruge epsilon her? hvordan kan jeg tjekke om den ligger mellem 0 og epsilon begge veje?
      print('denominator less than epsilon')
      return None  # The lines are parallel and don't intersect
   

   x = (b2*c1 - b1*c2) / denominator
   y = (a1*c2 - a2*c1) / denominator

   print(f'x: {x}, y: {y}')

   if not is_point_in_circle(x, y, r):
      print('point is not in circle')
      return None # The intersection point is outside the circle

   return (x, y)



def is_point_in_circle(x, y, r):
   '''
   If d < r, the point is inside the circle.
   If d > r, the point is outside the circle.
   If d = r, the point is on the boundary of the circle.
   '''
   # math.sqrt((x - h)**2 + (y - k)**2)   -> k,h = center of the circle
   # Since the circle is centered at the origin (0,0), I can simplify the distance formula to:
   d = math.sqrt(x**2 + y**2)
   return d < r


# Sort the intersection points in clockwise order around the circle
def sort_points(points):
   print(f'points: {points}')
   # Define a function that returns the angle from the positive x-axis to a point
   def angle(point):
      x,y = point
      print(f'x: {x}')
      print(f'y: {y}')
      return math.atan2(y, x)

   # Sort the points based on their angle from the positive x-axis
   points.sort(key=angle)

   return points


# Takes a point and a list of lines and returns the line that the point belongs to
def find_line(point, lines):
    x, y = point
    for line in lines:
        a, b, c = line
        # due to floating point precision issues, we need to use an epsilon value to check if the point lies on the line
        if a * x + b * y + c < epsilon:
            return line
    return None




# Read the coordinates of the candles - n times
for i in range(n):
   (x,y) = map(int, input().split())
   candles.append((x,y))


# Read the coefficients of the cutting lines - m times
for i in range(m):
   (a, b, c) = map(int, input().split())
   lines.append((a, b, c))
   #intersection_points.extend(find_intersection_circle(a, b, c, r))
   
#intersection_points = sort_points(intersection_points)

'''
# Step 5: Initialize an empty set of encountered lines
encountered_lines = set()

# Step 6: For each intersection point in the sorted list
for point in intersection_points:
    # Step 6.1: Find the line that the point belongs to
    line = find_line(point, lines)
    print(f'line: {line}')

    # Step 6.2: If the line is not in the set of encountered lines, increment the count of circle pieces and add the line to the set
    if line not in encountered_lines:
        circle_pieces += 1
        encountered_lines.add(line)
    # Step 6.3: Else, remove the line from the set
    else:
        encountered_lines.remove(line)

# Step 7: Return the count of circle pieces
print(circle_pieces)
'''


for index in range(len(lines)):
   # Add the intersection points for a line and circle
   inters_circle = find_intersection_circle(lines[index][0], lines[index][1], lines[index][2], r)
   intersection_points_circle.update(inters_circle)
   intersection_points.update(inters_circle)

   # Add the intersection points for two lines
   for j in range(index+1, len(lines)):
      inters_line = find_intersection_lines(lines[index], lines[j], r)
      if inters_line:
         if inters_line not in intersection_points:
            edges += 2  # Increment edges by 2 because two new edges are created
         else:
            edges += 1
         intersection_points.add(inters_line)

print(f'edges before: {edges}')   

# Add the edges from the circle   
edges += len(intersection_points_circle)

#F = E-V+1
cake_pieces = edges - len(intersection_points) + 1

print(f'minus: {edges - len(intersection_points)}')
print(f'intersection_points: {len(intersection_points)}')
print(f'edges: {edges}')
print(cake_pieces)


