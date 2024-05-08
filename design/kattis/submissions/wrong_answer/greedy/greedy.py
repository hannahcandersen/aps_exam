"""
Use greedy algorithm to solve the problem
Doesn't always find the optimal solution    
"""


a, e, h = map(int, input().strip().split())

alliance_preferences = {} # Member -> List of enemies
alliance_capacity = {} # Member -> Remaining kills

# Read alliance preferences and capacities
for _ in range(a):
    preference = input().strip().split()
    member_name = preference[0]
    capacity = int(preference[1])
    enemies = preference[2:] 
    alliance_preferences[member_name] = enemies
    alliance_capacity[member_name] = capacity

house_capacity = {} # House -> How many can be killed
house_members = {} # House -> List of members of the house
enemies_to_house = {} # Enemy -> Which house they belong to

# Read house descriptions
for _ in range(h):
    parts = input().strip().split()
    house_name = parts[0]
    members = parts[1:-1]
    capacity = int(parts[-1])
    house_capacity[house_name] = capacity
    house_members[house_name] = members
    for member in members:
        enemies_to_house[member] = house_name

# Sort houses by how many can be killed (ascending)
sorted_houses = sorted(house_capacity.items(), key=lambda x: x[1])

# Assign kills
kills = {}
total_kills = 0

# Priority to houses with smaller capacites 
for house_name, _ in sorted_houses:
    if house_name in house_members:
        members_in_house = house_members[house_name]
        # Members preferred by most allies to least
        preference_count = {}
        for member in members_in_house:
            preference_count[member] = sum(member in alliance_preferences[ally] for ally in alliance_preferences)
        # Sort by number of times each member is preferred (descending)
        sorted_members = sorted(preference_count.items(), key=lambda x: -x[1])
        for member, _ in sorted_members:
            # Go through each alliance member and try to assign this kill
            for ally in alliance_preferences:
                if member in alliance_preferences[ally] and alliance_capacity[ally] > 0:
                    if house_capacity[enemies_to_house[member]] > 0:
                        # Assign the kill
                        kills[(ally, member)] = 1
                        total_kills += 1
                        alliance_capacity[ally] -= 1
                        house_capacity[enemies_to_house[member]] -= 1
                        break  # Only one member can kill an enemy

if total_kills > e / 2:
    print(f"Dracarys {total_kills}")
else:
    print(f"When you play the game of thrones, you win or you die, therefore we surrender now {total_kills}")
