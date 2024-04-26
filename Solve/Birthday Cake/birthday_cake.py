'''
John wants to divide the cake into pieces so that each piece
has exactly one candle on it, and there are no left-over pieces
'''

# 1 <= n <= 50  - number of candles of distinct points located strictly inside the circle
# 1 <= m <= 15  - number of cuts as a straight line ax+by+c=0
# 1 <= r <= 100 - radius centered at (0,0)

'''
The candles are given as coordinates (x,y), where  0 <= sqrt(x^2 + y^2) < r
This just means that the candles are located strictly inside the circle
sqrt(x^2 + y^2) represents the Euclidean distance from a point with coordinates (x,y) to the origin (0,0) in a two-dimensional coordinate system
'''

'''
The cutting lines are given as coefficients a, b, and c, where (0 <= |a|, |b| <= 100) and (0 <= |c| <= 20000)
The values a and b are not both zero.

ax+by+c=0 explained:
* a and b determine the slope and orientation of the line in the coordinate plane.
-- if a = 0 and b > 0, the line is horizontal
-- if a > 0 and b = 0, the line is vertical
-- if a and b are both non-zero, the line is diagonal
-- if a and b are both zero, the line is a point
* c affects where the line intersects the y-axis when b != 0
-- If c=0, the line passes through the origin (0,0), simplifying the equation to ax+by=0.
'''

'''
Disclaimers:
- All candles and lines are distinct.
- No candle is on a cut line.
- No line is completely outside or tangent to the cake.
- The input guarantees that the number of cake pieces remains the same if any cut line is shifted by at most 10^-4 in any direction.
- The input also guarantees that each candle remains in the interior of the same piece of cake if its position is shifted by at most 10^-4 in any direction.
'''


n, m, r = map(int, input().split())

# Read the coordinates of the candles - n times
# Read the coefficients of the cutting lines - m times