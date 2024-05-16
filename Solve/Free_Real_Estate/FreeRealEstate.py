import sys

# Returns the sum of the elements in the range [a, b]
def sum(a, b, tree):
    #  Make sure to point to the correct index in the tree (leaf node)
    a = a - 1 + lengthOfTheArray
    b = b - 1 + lengthOfTheArray
    s = 0
    while a <= b:
        # Checks is a right child (odd), if yes add the value of the node to the sum. Increment a by 1 to move to next segment
        if a % 2 == 1:
            s += tree[a]
            a += 1
        # Checks is b right left (even), if yes add the value of the node to the sum. Increment a by 1 to move to next segment
        if b % 2 == 0:
            s += tree[b]
            b -= 1
        a //= 2 # Move to parent node
        b //= 2 # Move to parent node
    return s

# Increases the array value at position k by x:
def update(k, x, tree):
    k = k - 1 + lengthOfTheArray
    tree[k] = x
    while k > 1:
        tree[k // 2] = tree[k] + tree[k ^ 1]
        k //= 2

def buildTree(penthouses, n):
    # Store a segment tree as an array of 2n elements where n is the size of the penthouse array
    tree = [0] * n + penthouses
    for i in range(n - 1, 0, -1):
        tree[i] = tree[2 * i] + tree[2 * i + 1]
    return tree

lengthOfTheArray, numberOfOperations, startPriceOfAllPenthouses = map(int, sys.stdin.readline().split())
penthouses = [startPriceOfAllPenthouses] * lengthOfTheArray
tree = buildTree(penthouses, lengthOfTheArray)

for _ in range(numberOfOperations):
    operation, i, n = sys.stdin.readline().split()
    i = int(i)
    n = int(n)
    if operation == "update":
        update(i, n, tree)
    elif operation == "query":
        price = sum(i, n, tree)
        if price == 0:
            sys.stdout.write("it's free real estate\n")
        else:
            sys.stdout.write(str(price) + "\n")