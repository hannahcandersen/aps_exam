"""
Iterative bottom-up approach

Find out what was ordered  given the total cost of the order and the cost of each item on the menu.
    
Input: 
- n: number of items on the menu (1 <= n <= 100)
- n space-seperated integers (c1, c2..): the cost of each item on the menu (1 <= cost <= 1000)    
- m: the numbers of orders (1 <= m <= 1000)
- m orders of an integer s (1 <= s <= 30.000): the total cost of the order
Output: 
- For each order
    - If there is one unique order giving this cost, output a space-separated list of the items ordered
    - If there are multiple orders giving this cost, output "Ambiguous"
    - If there is no order giving this cost, output "Impossible"
    
    
Not memory efficient enough 
Change to only storing the last item in the order and then backtracking to find the full order
"""
import time
start = time.time()

n = int(input())
menu = list(map(int, input().split())) # 0-indexed, remember to convert to 1-indexed when printing
m = int(input())
orders = list(map(int, input().split()))
max_order_price = max(orders)

# Tabulation
dp = [None] * (max_order_price + 1) 
dp[0] = (1, []) # 0 cost can be reached in 1 way, with no items


# Go through items on the menu and construct all the possible costs that can be reached
for i, item_price in enumerate(menu):
    for total_price in range(item_price, max_order_price + 1):
        if dp[total_price - item_price] is not None:
            ways, items = dp[total_price - item_price]
            if dp[total_price] is None:
                dp[total_price] = (ways, items + [i+1] if items is not None else [i+1]) # convert to 1-indexed            
            else:
                # If this cost was already reachable in a different way, it is ambiguous
                dp[total_price] = (dp[total_price][0] + ways, dp[total_price][1] if dp[total_price][1] is not None else items + [i+1])
                
for total_cost in orders:
    if dp[total_cost] is None:
        print("Impossible")
    elif dp[total_cost][0] > 1 or dp[total_cost][1] is None:
        print("Ambiguous")
    else:
        print(' '.join(map(str, dp[total_cost][1])))

end = time.time()
print(f"Time: {end-start}")


