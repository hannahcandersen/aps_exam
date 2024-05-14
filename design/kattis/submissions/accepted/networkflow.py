"""
    FORD FULKERSON FLOW ALGORITHM
    Taken from: https://github.itu.dk/algorithms/aps-24/blob/main/060-network-flows/code/flow.py 
    
    Can be used for graphs represented as:
      graph = defaultdict(lambda: defaultdict(int)) # vertex -> (vertex -> capacity)
"""
from collections import defaultdict

### BREADTH-FIRST SEARCH ###
from collections import deque


def bfs(graph, src, sink, mincap=0):
    """
    Args:
        graph (dict):           The graph, represented as a dictionary where the keys are nodes and the values are dictionaries
                                representing the adjacent nodes and their capacities.
        src (hashable):         The source node from which the path starts.
        sink (hashable):        The destination node where the path ends.
        mincap (int, optional): The minimum capacity that an edge must have to be considered.

    Returns:
        tuple: A tuple where the first element is a boolean indicating whether a path has been found and the second element
               is the path if a path has been found or the set of visited nodes if no path has been found.
    """

    # Parent dictionary storing the nodes' parents. Used to reconstruct the path to be able to return it
    parent = {src: src}

    # Use a queue to keep track of the nodes to visit
    queue = deque([src])

    # While there are nodes in the queue
    while queue:
        current_node = queue.popleft()

        for neighbor, cap in graph[current_node].items():
            # If the capacity is greater than the minimum capacity and the node has not been visited
            if cap > mincap and neighbor not in parent:
                parent[neighbor] = current_node
                queue.append(neighbor)

                # If the node is the sink - Reconstruct the path and return it
                if neighbor == sink:
                    path = []

                    # Start from the sink
                    current = sink

                    while src != current:
                        # Add the edge from the parent to the current node to the path
                        path.append((parent[current], current))

                        # Move on to the parent
                        current = parent[current]

                    # Return true that a path has been found and the path
                    return (True, path)

    # If no path is found, return False and the set of visited nodes
    return (False, set(parent))


### FORD-FULKERSON ALGORITHM ###
def flow(orggraph, src, dest):
    """
    Ford-Fulkerson algorithm to find the maximum flow in a flow network.
    Works by repeatedly finding paths from the source to the destination in the residual graph
    and augmenting the flow along these paths until no more augmenting paths can be found.

    Args:
        orggraph (dict):    The original graph, represented as a dictionary where the keys are nodes and the values
                            are dictionaries representing the adjacent nodes and their capacities.
        src (hashable):     The source node from which the flow starts.
        dest (hashable):    The destination node where the flow ends.

    Returns:
        tuple: A tuple where the first element is the maximum flow, the second element is the residual graph,
               and the third element is the set of visited nodes.
    """
    # Create residual graph
    graph = defaultdict(lambda: defaultdict(int))
    maxcapacity = 0

    # Copy the original graph to the residual graph and find the maximum capacity
    for u, d in orggraph.items():
        for v, c in d.items():
            graph[u][v] = c
            maxcapacity = max(maxcapacity, c)

    # Start flow at 0
    current_flow = 0

    # Initialize the minimum capacity to the maximum capacity. To make it faster and more likely to find a high flow path
    mincap = maxcapacity

    while True:
        # Check if there is a path with the current minimum capacity
        ispath, p_or_seen = bfs(graph, src, dest, mincap)

        ## Path was not found
        if not ispath:
            # Halve the minimum capacity and try again with lower minimum capacity
            if mincap > 0:
                mincap = mincap // 2
                continue
            # Minimum capacity is 0, no more paths can be found. Return the current flow, the residual graph, and the set of visited nodes
            else:
                return (current_flow,
                        {a: {b: c - graph[a][b] for b, c in d.items() if graph[a][b] < c}
                         for a, d in orggraph.items()},
                        p_or_seen)

        ## Path was found
        p = p_or_seen
        # Find the minimum capacity of the path
        saturation = min(graph[u][v] for u, v in p)
        # Increase the current flow by the minimum capacity of the path
        current_flow += saturation
        # For each edge in the path
        for u, v in p:
            # Decrease the capacity of the edge by the minimum capacity of the path
            graph[u][v] -= saturation
            # Increase the capacity of the reverse edge by the minimum capacity of the path
            graph[v][u] += saturation





"""
    SOLUTION
    
    Builds a graph from the input and uses the Ford-Fulkerson algorithm to find the maximum flow in the graph.
"""

a, e, h = map(int, input().split()) # alliances, enemies, houses

#### GRAPH REPRESENTATION ####
# Source -> Alliances -> Enemies -> Houses -> Sink. If no house, go straight to sink with capacity 1 
graph = defaultdict(lambda: defaultdict(int)) # vertex -> (vertex -> capacity).
source_v = 0
alliance_start = 1          # Alliances    Vertices 1 - n
enemy_start = a+1           # Enemies:     Vertices n+1 - n+m
house_start = a+e+1         # Houses:      Vertices n+m+1 - n+m+p
sink_v = a+e+h+1            # Sink:        Vertex n+m+p+1
wanted_enemies = []

#### BUILD GRAPH ####
# Aliance preferences
for alliance_i in range(a): 
    alliance_v = alliance_i + alliance_start 
    line = list(input().split()) # {name, capacity, name .. name}
    capacity = int(line[1]) # Maximum number of enemies the alliance member can kill
    enemies = line[2:] 
    
    # Add edge between source and alliance 
    graph[source_v][alliance_v] = capacity
    
    # Add edge between alliance and enemies
    for enemy in enemies: 
        if enemy not in wanted_enemies:
            wanted_enemies.append(enemy)
        enemy_v = wanted_enemies.index(enemy) + enemy_start 
        graph[alliance_v][enemy_v] = 1
        
# Houses
for house_i in range(h): 
    house_v = house_i + house_start
    line = list(input().split()) # {name, name .. name, capacity}
    
    enemies_in_house = line[1:-1]
    capacity = int(line[-1]) # Maximum number of enemies in the house that can be killed
    
    # Add edge between enemy and house
    for enemy in enemies_in_house: 
        enemy_v = wanted_enemies.index(enemy) + enemy_start 
        graph[enemy_v][house_v] = 1

    # Add edge between houses and sink
    graph[house_v][sink_v] = capacity 

# Add edges between enemies not in any house and the sink
for enemy in wanted_enemies: 
    enemy_v = wanted_enemies.index(enemy) + enemy_start 
    if enemy_v not in graph:
        graph[enemy_v][sink_v] = 1

#### FIND MAX FLOW AND RESULT ####
(max_flow, residual_graph, visited) = flow(graph, source_v, sink_v)
result = max_flow/e

if result > 0.5:
    print("Dracarys", max_flow)
else:
    print("When you play the game of thrones, you win or you die, therefore we surrender now", max_flow)
