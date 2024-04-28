"""
Recursive top-down approach with memoization

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
"""
import sys
import time
sys.setrecursionlimit(10**6)

def solve(cost, items = [], menu_index = 0):
    # DIDNT FIND A VALID ORDER: Price is negative or we have reached the end of the menu
    if cost < 0 or menu_index == n:
        return 0, []
    
    # FOUND A VALID ORDER: Price is 0
    if cost == 0:
        return 1, items 

    # Memoization: Check if we have already calculated the number of valid orders for the current price
    if cost in num_of_valid_orders:
        return num_of_valid_orders[cost], valid_order[cost]
    
    # Recursively solve subproblems
    num_of_valid_orders.setdefault(cost, 0)
    valid_order.setdefault(cost, [])
    # Case 1: Include current item in the order, and recursively solve for the remaining cost
    ways_include, items_include = solve(cost - menu[menu_index], items + [menu_index+1], menu_index)
    # Case 2: Exclude current item from the order, and recursively solve for the remaining cost
    ways_exclude, items_exclude = solve(cost, items, menu_index + 1)
    
    # Update memoization
    total_ways = ways_include + ways_exclude
    num_of_valid_orders[cost] = total_ways
    
    # Only update the valid order if there is only one way to reach the current cost and the order has not been set before
    if total_ways == 1:
        valid_order[cost] = items_include if ways_include == 1 else items_exclude

    return num_of_valid_orders[cost], valid_order[cost]

# Start timer
start = time.time()

# READ INPUT
n = int(input())
menu = list(map(int, input().split()))
m = int(input())
orders = list(map(int, input().split()))
maxOrder = max(orders)

# INITIALIZE MEMOIZATION
num_of_valid_orders = {} # price -> number of valid orders    
valid_order = {} # price -> valid order
# Cost 0 can be reached in 1 way, by ordering nothing
num_of_valid_orders[0] = 1
valid_order[0] = []
# The cost of each item on the menu can be reached in 1 way, by ordering only that item
for i, item_price in enumerate(menu):
    num_of_valid_orders[item_price] = 1
    valid_order[item_price] = [i+1] # convert to 1-indexed

# PROCESS ORDERS
for order in orders:
    # Find solution for the current order if it has not been calculated before
    if order not in num_of_valid_orders:
        solve(order)
    
    # Now we have the solution for the current order
    if num_of_valid_orders[order] > 1:
        print("Ambiguous")
    elif num_of_valid_orders[order] == 0:
        print("Impossible")
    else:
        print(" ".join(str(x) for x in valid_order[order]))
        
# End timer
end = time.time()
