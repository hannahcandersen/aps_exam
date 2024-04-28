from sys import setrecursionlimit
setrecursionlimit(10**6)

def solve_menu_orders(menu, orders):
    max_cost = max(orders)
    dp = [0] * (max_cost + 1)
    combinations = [[] for _ in range(max_cost + 1)]
    
    dp[0] = 1  # There's one way to achieve a cost of 0: order nothing
    combinations[0] = [[]]  # The combination to achieve this is an empty list
    
    # Compute all possible ways to reach any cost up to the max order cost
    for cost in menu:
        for current_cost in range(cost, max_cost + 1):
            if dp[current_cost - cost] > 0:
                if dp[current_cost] == 0:
                    combinations[current_cost] = [combo + [cost] for combo in combinations[current_cost - cost]]
                else:
                    combinations[current_cost] += [combo + [cost] for combo in combinations[current_cost - cost]]
                dp[current_cost] += dp[current_cost - cost]
    
    results = []
    for order_cost in orders:
        if dp[order_cost] == 0:
            results.append("Impossible")
        elif dp[order_cost] > 1:
            results.append("Ambiguous")
        else:
            results.append(' '.join(map(str, sorted(combinations[order_cost][0]))))
    
    return results

n = int(input())
menu = list(map(int, input().split()))
m = int(input())
orders = list(map(int, input().split()))

results = solve_menu_orders(menu, orders)
for result in results:
    print(result)
