"""
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
    
    
Description of solution: 
- Iterative bottom-up approach. Start by finding the number of ways to reach each price from 0 up to the maximum order price
- Tabulation to avoid recomputation of subproblems (memoization)
- Keep track of the last item used to reach each price to be able to reconstruct the order. Saves space compared to storing the whole order
"""
import time
start = time.time()

# Read input
n = int(input())                          # Number of items on the menu
menu = list(map(int, input().split()))    # Price of each item on the menu
m = int(input())                          # Number of orders
orders = list(map(int, input().split()))  # Total price of each order
max_order_price = max(orders)             # To avoid unnecessary computation for higher prices than the maximum order price

# Tabulation 
ways = [None] * (max_order_price + 1)       # Number of ways to reach each price. Index corresponds to the price
last_item = [None] * (max_order_price + 1)  # Last item used to reach each price. Index corresponds to the price
ways[0] = 1                                 # Base case: Price=0 can be reached in 1 way, ordering no items

# Fill the lists using iterative bottom-up approach
for i, item_price in enumerate(menu): 
    for price in range(item_price, max_order_price + 1):
        # If the price can be reached from a previous price (without the current item)
        if ways[price - item_price] is not None: 
            # Price reached for the first time
            if ways[price] is None:
                ways[price] = ways[price - item_price]  
                last_item[price] = i + 1 # Store the final item used to reach this price (save as 1-indexed for printing)
            # Found another way to reach price
            else: 
                ways[price] += ways[price - item_price] 
                # We do not care about the last item used to reach the price if there are multiple ways to reach it
        # Else the price cannot be reached from a previous price, it is already None and should remain None

# Output the result for each order
for order_price in orders:
    if ways[order_price] is None:
        print("Impossible")
    elif ways[order_price] > 1:
        print("Ambiguous")
    else:
        # Reconstruct the order by backtracking
        items = []
        price = order_price
        while price > 0:
            item = last_item[price]
            items.append(item)
            price -= menu[item - 1] # Backtrack to last item for the previous price
        print(' '.join(map(str, sorted(items)))) # Should be in sorted order in the output

end = time.time()
print(f"Running time: {end-start}")
