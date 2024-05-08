"""
    Use to find the maximum flow in a graph using the Ford-Fulkerson algorithm.
    
    Can be used for graphs represented as:
      graph = defaultdict(lambda: defaultdict(int)) # vertex -> (vertex -> capacity)
      
    Taken from: https://github.itu.dk/algorithms/aps-24/blob/main/060-network-flows/code/flow.py 
"""
from collections import defaultdict

### BREADTH-FIRST SEARCH ###
from collections import deque

def bfs(graph, src, sink, mincap=0): 
    """
    Implements the Breadth-First Search algorithm to find a path from a source node to a destination node in a graph.
    Works by exploring all the vertices at the current depth/level before moving on to vertices at the next depth level.

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
    parent = {src:src} 

    # Use a queue to keep track of the nodes to visit
    queue = deque([src]) 

    # While there are nodes in the queue
    while queue:
        current_node = queue.popleft()

        for neighbor,cap in graph[current_node].items():
            # If the capacity is greater than the minimum capacity and the node has not been visited
            if cap > mincap and neighbor not in parent:
                parent[neighbor] = current_node
                queue.append(neighbor)

                # If the node is the sink - Reconstruct the path and return it
                if neighbor == sink:
                    path =  []

                    # Start from the sink
                    current = sink

                    while src != current:
                        # Add the edge from the parent to the current node to the path
                        path.append((parent[current],current))

                        # Move on to the parent
                        current = parent[current]

                    # Return true that a path has been found and the path
                    return (True,path)

    # If no path is found, return False and the set of visited nodes
    return (False,set(parent))
    
    
### FORD-FULKERSON ALGORITHM ###
def flow(orggraph, src, dest):
    """
    Implements the Ford-Fulkerson algorithm to find the maximum flow in a flow network.
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