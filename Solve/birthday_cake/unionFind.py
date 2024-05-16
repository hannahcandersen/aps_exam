import math
#et link: https://yuminlee2.medium.com/union-find-algorithm-ffa9cd7d2dba


class UnionFind:
    def __init__(self, size):
        self.parent = list(range(size))
        self.rank = [1] * size

    def find(self, p):
        if self.parent[p] != p:
            self.parent[p] = self.find(self.parent[p])  # Path compression
        return self.parent[p]

    def union(self, p, q):
        rootP = self.find(p)
        rootQ = self.find(q)

        if rootP != rootQ:
            # Union by rank
            if self.rank[rootP] > self.rank[rootQ]:
                self.parent[rootQ] = rootP
            elif self.rank[rootP] < self.rank[rootQ]:
                self.parent[rootP] = rootQ
            else:
                self.parent[rootQ] = rootP
                self.rank[rootP] += 1

    def count_components(self):
        return len(set(self.find(x) for x in self.parent))



def linear_combination(a, b, c, x, y):
    return a * x + b * y + c

def read_ints():
    return map(int, input().split())

n, m, r = read_ints()
candles = [tuple(read_ints()) for _ in range(n)]
uf = UnionFind(n)


for _ in range(m):
    a, b, c = read_ints()
    
    # Check which side of the line each candle is on
    sides = {}
    for index in range(n):
        candle = candles[index]
        # Calculate the linear combination for each candle
        result = linear_combination(a, b, c, candle[0], candle[1])
        # Determine which side of the line the candle is on
        sides[index] = result > 0
        print(f'candle: {candle}, result: {result}, side: {sides[index]}')
    #sides = {candle_index: sign(a, b, c, *candles[candle_index]) > 0 for candle_index in range(n)}

    # Group all candles by the side of the line they are on
    for i in range(n):
        for j in range(i + 1, n):
            if sides[i] == sides[j]:
                print(f'union: {i}, {j}')
                uf.union(i, j)

# Now we check if each component has exactly one candle
component_sizes = {}
for i in range(n):
    root = uf.find(i)
    if root in component_sizes:
        component_sizes[root] += 1
    else:
        component_sizes[root] = 1

valid = all(size == 1 for size in component_sizes.values())


print("YES" if valid else "NO")
