'''
John wants to divide the cake into pieces so that each piece
has exactly one candle on it, and there are no left-over pieces
'''

# 1 <= n <= 50  - number of candles of distinct points located strictly inside the circle
# 1 <= m <= 15  - number of cuts as a straight line ax+by+c=0 - max cuts is (m(m+1)/2)+1
# 1 <= r <= 100 - radius centered at (0,0)

'''
The candles are given as coordinates (x,y), where  0 <= sqrt(x^2 + y^2) < r
This just means that the candles are located strictly inside the circle
sqrt(x^2 + y^2) represents the Euclidean distance from a point with coordinates (x,y) to the origin (0,0) in a two-dimensional coordinate system
'''

'''
The cutting lines are given as coefficients a, b, and c, where (0 <= |a|, |b| <= 100) and (0 <= |c| <= 20000)
The values a and b are not both zero.
- if a = 0 and b != 0, the line is horizontal
- if a != 0 and b = 0, the line is vertical
- if c = 0, then a is the slope and b is the y-intercept

Denne video forklarer ax+by=c meget godt:
https://www.khanacademy.org/math/algebra/x2f8bb11595b61c86:forms-of-linear-equations/x2f8bb11595b61c86:standard-form/v/standard-form-for-linear-equations
Brug denne til at tegne med: https://www.geogebra.org/calculator
'''

'''
Disclaimers:
- All candles and lines are distinct.
- No candle is on a cut line.
- No line is completely outside or tangent to the cake.
- The input guarantees that the number of cake pieces remains the same if any cut line is shifted by at most 10^-4 in any direction.
--- Regarding the cut lines: When it says that the number of cake pieces remains the same if any cut line is shifted by at most 10^-4
    in any direction, it means that the cuts are made in such a way that moving a cut line a tiny bit will not change the total number of
    pieces into which the cake is divided. This is to avoid ambiguity in cases where a cut might just graze a candle or be very close to doing so.
    If such a situation occurred, a tiny shift could either cause a candle to be on the edge of a piece or split a piece into two, which would
    make the problem ill-posed.
- The input also guarantees that each candle remains in the interior of the same piece of cake if its position is shifted by at most 10^-4 in any direction.
-- Regarding the candles: When the statement assures that each candle remains in the interior of the same piece of cake if its position is
    shifted by at most 10^-4 in any direction, it is ensuring that no candle is precisely on the boundary of a piece. There's a small "safe zone"
    around each candle where, even if the candle were nudged a little in any direction, it would still clearly belong to the same piece of the
    cake without crossing over into another piece.

'''

'''
Euler's characteristic formula: V-E+F = 2 bliver brugt til at finde antal kagestykker
men bliver brugt i denne format: F = E - V + 1 (kun +1, fordi vi ikki ønsker at inkludere det uendelige stykke kage rundt om cirklen)
'''

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
candles_on_piece = [set(range(n))] # Initialize a list of sets to represent pieces of cake. Initially there is only one set containing all candles.



######## METHODS ########
# Solve the system of equations formed by the equation of the circle and the equation of the line to find the intersection points
def find_intersection_circle(a, b, c, r):
    # ax + by + c = 0
    # x² + y² = r²

    if b == 0:
        x = -c/a
        # Solve for y in the circle equation: y = sqrt(r^2 - x^2)
        y1 = cmath.sqrt(r**2 - x**2)
        y2 = -cmath.sqrt(r**2 - x**2)
        return [(x, y1), (x, y2)]
    else:
        # Solve for x
        x1 = (-a*c + b*cmath.sqrt((r**2)*(a**2+b**2)-(c**2)))/(a**2+b**2)
        x2 = (-a*c - b*cmath.sqrt((r**2)*(a**2+b**2)-(c**2)))/(a**2+b**2)

        # Solve for y
        y1 = (-c - a*x1) / b
        y2 = (-c - a*x2) / b

    # Return the intersection points
    return {(x1, y1), (x2, y2)}


def find_intersection_lines(line1, line2, r):
   # using cross product
   # Exactly one intersection point that is not a vertex of any line segment
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



######## START ########
# Read the coordinates of the candles - n times
for i in range(n):
   # O(n)
   (x,y) = map(int, input().split())
   candles.append((x,y))


# Read the coefficients of the cutting lines - m times
for i in range(m):
    (a, b, c) = map(int, input().split())



    ######## FIND CAKE PIECES ########
    # Add the intersection points for a line and circle
    inters_circle = find_intersection_circle(a, b, c, r)
    intersection_points_circle.update(inters_circle)
    intersection_points.update(inters_circle)

    # Add the intersection points for two lines
    if len(lines) != 0: # If there are already lines, check for intersections with the new line
        for j in range(len(lines)):
            # 1 - 2 - 3 - 4
            '''
                1+2+3+4..+m
                = m(m+1)/2
                = m^2
                O(m^2)
            '''
            inters_line = find_intersection_lines((a, b, c), lines[j], r)
            if inters_line: # If there is an intersection point
                if inters_line not in intersection_points:
                    edges += 2  # Increment edges by 2 because two new edges are created
                else:
                    edges += 1 # Increment edges by 1 because one new edge is created, since the intersection point already exists
                intersection_points.add(inters_line)

    lines.append((a, b, c))



    ######## CHECK CANDLES ########
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
            if a * candle[0] + b * candle[1] + c > 0:
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
    candles_on_piece = new_cake_pieces


# Add the edges from the circle
edges += len(intersection_points_circle)

#F = E-V+1
cake_pieces = edges - len(intersection_points) + 1

#print(f'candles_on_piece: {candles_on_piece}')
#print(f'cake_pieces: {cake_pieces}')


if all(len(s) == 1 for s in candles_on_piece) and len(candles_on_piece) == cake_pieces:
   print('yes')
else:
    print('no')
