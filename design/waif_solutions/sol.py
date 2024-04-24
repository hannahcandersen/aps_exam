"""
Assignment: https://itu.kattis.com/courses/BAPS/APS24/assignments/ehr4an/problems/waif

Description:
Daycare center, where only a certain amount of toys from each category are allowed. 
Not all toys are liked by all children.
Find the maximum amount of children who can be satisfied with the toys available.
- Input:
    - First line with 3 integers
        - N: number of children         (1 ≤ N)
        - M: number of toys             (M ≤ 100)
        - P: number of toy categories   (0 ≤ P ≤ M)
        Both children and toys are numbered starting from 1
    - N lines with integers, where line 1 is child 1, line 2 is child 2, etc.
        - k: Number of toys the child likes       (1 ≤ k ≤ M) 
        - t1 t2 ... tk: the toys the child likes  (1 ≤ ti ≤ M)
    - P lines with integers, where line 1 is category 1, line 2 is category 2, etc.
        - l: Number of toys in the category       (1 ≤ l ≤ M)
        - t1 t2 ... tl: the toys in the category  (1 ≤ ti ≤ M)
        - r: At most r of the toys in the category can be used (1 ≤ r ≤ l ≤ m) 
- Output:
    - Maximum number of children that can be satisfied with the toys available

Use Ford-Fulkerson algorithm to find the maximum flow in the graph.
"""
from collections import defaultdict
from flow import flow

n, m, p = map(int, input().split()) # Children, toys, categories

#### GRAPH REPRESENTATION ####
# Source -> Child -> Toys -> Category -> Sink. If no category, go straight to sink with capacity 1 
graph = defaultdict(lambda: defaultdict(int)) # vertex -> (vertex -> capacity).
source_v = 0
child_start = 1         # Children:    Vertices 1 - n
toy_start = n           # Toys:        Vertices n+1 - n+m
category_start = n+m+1  # Categories:  Vertices n+m+1 - n+m+p
sink_v = n+m+p+1        # Sink:        Vertex n+m+p+1


#### BUILD GRAPH ####
# Children preferences
for i in range(n): 
    child_v = i + child_start 
    line = list(map(int, input().split()))
    preferences = line[1:] 
    
    # Add edge between source and child 
    graph[source_v][child_v] = 1
    
    # Add edge between child and toys
    for toy in preferences: 
        toy_v = toy + toy_start 
        graph[child_v][toy_v] = 1
        
# Toy categories
for j in range(p): 
    category_v = j + category_start
    line = list(map(int, input().split()))
    toys_in_j_category = line[1:-1]
    r = line[-1] # Capacity - Maximum number of toys in the category that can be used
    
    # Add edge between toy and category
    for toy in toys_in_j_category: 
        toy_v = toy + toy_start 
        graph[toy_v][category_v] = 1

    # Add edge between category and sink
    graph[category_v][sink_v] = r 

# Add edges between toys not in any category and the sink
for toy_v in range(toy_start, category_start): 
    if toy_v not in graph:
        graph[toy_v][sink_v] = 1

#print(graph)


#### FIND MAX FLOW ####
(max_flow, residual_graph, visited) = flow(graph, source_v, sink_v)
print(max_flow)