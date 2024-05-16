"""
Find out what was ordered given the total cost of the order and the cost of each item on the menu.
    Iterative bottom-up dynamic programming approach. 
    Memoization/tabulation to avoid recomputation of subproblems
    Keep track of the last item used to reach each price to be able to reconstruct the order. 
"""

# Read input
n = int(input())                          # Number of items on the menu
menu = list(map(int, input().split()))    # Price of each item on the menu
m = int(input())                          # Number of orders
orders = list(map(int, input().split()))  # Total price of each order
max_order_price = max(orders)             

# Memoization/Tabulation 
ways = [0] * (max_order_price + 1)       # Number of ways to reach each price. Index corresponds to the price
last_item = [0] * (max_order_price + 1)  # Last item used to reach each price. Index corresponds to the price
ways[0] = 1                              # Base case: Price=0 can be reached in 1 way, ordering no items

# Fill the lists 
for i, item_price in enumerate(menu): 
    for price in range(item_price, max_order_price + 1):
        ways_without_item = ways[price - item_price] # Sub-problem: Number of ways to reach the price without the current item
        # If the price can be reached from a previous price (without the current item)
        if ways_without_item != 0: 
            # Price with item reached for the first time
            if ways[price] == 0:
                ways[price] = ways_without_item 
                last_item[price] = i + 1 # Store the final item used to reach this price (save as 1-indexed for printing)            
            # Price with item has been reached before, mark ambiguous
            else: 
                ways[price] = 2
        # Else the price cannot be reached from a previous price, keep the current value


# Output the result for each order
for order_price in orders:
    if ways[order_price] == 0:
        print("Impossible")
    elif ways[order_price] == 2:
        print("Ambiguous")
    else:
        # Reconstruct the order
        items = []
        price = order_price
        while price > 0:
            item = last_item[price]
            items.append(item)
            price -= menu[item - 1] 
        print(' '.join(map(str, sorted(items)))) # Should be in sorted order in the output
