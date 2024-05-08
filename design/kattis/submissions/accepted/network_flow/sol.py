"""
- Input:
First line with 3 integers
    - A: number of members in alliance
    - E: number of enemies
    - H: number of houses

A lines, where line 1 is alliance member 1, line 2 is alliance member 2, etc       
    - a: name of the alliance member
    - k: number of enemies this alliance member can kill (capacity)
    - t1 t2 ... tk: names of the enemies this alliance member wants to kill

H lines, where line 1 is house 1, line 2 is house 2, etc.
    - h: name of the house  
    - t1 t2 ... tl: name of the enemies in this house
    - r: at most r enemies from this house can be killed (capacity) 

- Output:
    - 

Use Ford-Fulkerson algorithm to find the maximum flow in the graph. 
"""
from collections import defaultdict
from flow import flow

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
    capacity = int(line[1])
    enemies = line[2:] 
    
    # Add edge between source and alliance 
    graph[source_v][alliance_v] = capacity
    
    # Add edge between alliance and enemies
    for enemy in enemies: 
        # Add newly encountered enemies to the list of wanted enemies
        if enemy not in wanted_enemies:
            wanted_enemies.append(enemy)
        
        # Add edge between alliance_index and enemy_index
        enemy_v = wanted_enemies.index(enemy) + enemy_start 
        graph[alliance_v][enemy_v] = 1 # capacity always 1
        
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

#### FIND MAX FLOW ####
(max_flow, residual_graph, visited) = flow(graph, source_v, sink_v)
result = max_flow/e

if result > 0.5:
    print("Dracarys", max_flow)
else:
    print("When you play the game of thrones, you win or you die, therefore we surrender now", max_flow)
