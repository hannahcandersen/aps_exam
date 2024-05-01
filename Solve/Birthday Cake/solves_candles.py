'''
John wants to divide the cake into pieces so that each piece
has exactly one candle on it, and there are no left-over pieces
'''

# 1 <= n <= 50  - number of candles of distinct points located strictly inside the circle
# 1 <= m <= 15  - number of cuts as a straight line ax+by+c=0 - we can max get 30 pieces
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


n, m, r = map(int, input().split())
#epsilon = 10**-4
candles = []
lines = []
cake_pieces = [set(range(n))] # Initialize a list of sets to represent the pieces of cake, with the first piece containing all candles.

'''
Computers cannot represent most decimal fractions exactly as binary fractions, leading to tiny errors in arithmetic involving floating-point numbers.
When you compare two floating-point numbers for equality, you generally can't check if they're exactly equal because of potential rounding errors.
Instead, you check if the absolute difference between them is less than epsilon.

For instance, if you want to check if the floating-point numbers a and b are "equal," you would do something like this:
    if abs(a - b) < epsilon:
        # a and b are considered "equal"

'''

# Read the coordinates of the candles - n times
for i in range(n):
    (x, y) = map(int, input().split())
    candles.append((x, y))


# Read the coefficients of the cutting lines - m times
for i in range(m):
    (a, b, c) = map(int, input().split())
    lines.append((a, b, c))




'''
for candle in candles:
    print(f'candle : {candle}')
    for line in coefficients:
        print(f'line : {line}')
        result = line[0] * candle[0] + line[1] * candle[1] + line[2]
        print(f'result : {result}')
        if result > 0:
            side_one.add(candle)
        else:
            side_two.add(candle)
'''

# Iterate over each cutting line provided in the input.
for line in lines:
    # Initialize a new list to hold the divided pieces after each cut.
    new_cake_pieces = []
    
    # Iterate over the existing pieces of cake.
    for piece in cake_pieces:
        # Create two new sets to hold the candle indices for each side of the cut.
        one_side = set()
        other_side = set()
        
        # Iterate over the candle indices in the current piece.
        for candle_index in piece:
            # Retrieve the candle's coordinates based on its index.
            candle = candles[candle_index]
            
            # Calculate the position of the candle relative to the cutting line.
            # If the result is positive, the candle is on one side of the line.
            if line[0] * candle[0] + line[1] * candle[1] + line[2] > 0:
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
    cake_pieces = new_cake_pieces
    #print(f'pieces: {cake_pieces}')

print(f'length: {len(cake_pieces)}')
if (len(cake_pieces) == n):
    print('yes')
else:
    print('no')



