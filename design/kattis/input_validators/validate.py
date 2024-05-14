#!/usr/bin/env python3
# 43 for failure and 42 for succes 
# (1 <= a, e <= 100, 0 <= h <= m)
import sys
import re

def validate_first_line(line):    
    # Check that line matches regex
    match = re.match(r"^(\d+) (\d+) (\d+)\r?\n$", line)
    if not match:
        return False
    a, e, h = map(int, match.groups())
    
    # Check that numbers are within limits
    #TODO: Change to our limits 
    if not (1 <= a <= 100 and 1 <= e <= 100 and 0 <= h <= e):
        return False
    
    return (a, e, h)

def validate_alliance_member_line(line, expected_enemy_names, alliance_members):
    # Check that the line matches the regex
    match = re.match(r"^([A-Za-z]+) (\d+) ((?:[A-Za-z]+ ?)+)\r?\n$", line)
    if not match:
        return False
    name, capacity, enemies = map(str, match.groups())

    # Check capacity is within limits
    #TODO: Change to our limits 
    if not (1 <= int(capacity) <= 100):
        return False 
        
   # Check if we already have seen this name before
    if name in alliance_members:
        return False
    
    # Initialize sets to keep track of enemies names
    unique_enemies = set()
    
    # Check if each enemy is unique
    for enemy in enemies.split():
        if enemy in unique_enemies:
            return False
    else:
        unique_enemies.add(enemy)
    
    return True, name, enemies

def validate_house_line(line, enemies_seen, houses):
    # Check that the line matches the regex
    match = re.match(r"^([A-Za-z]+) ((?:[A-Za-z]+ ?)+) (\d+)\r?\n$", line)
    if not match:
        return False
    house, members, capacity = map(str, match.groups())

    # Check capacity is within limits
    # TODO: Change to our limits 
    if not (1 <= int(capacity) <= 100):
        return False 
    
    # Check that members are some known enemies
    for member in members.split():
        if member not in enemies_seen:
            return False
        
    #Check if we already has seen this hous before         
    if house in houses:
        return False
        
   # Check that the same member is not used twice in the same line
   # Initialize sets to keep track of members names
    unique_members = set()
    # Check if each member is unique
    for member in members.split():
        if member in unique_members:
            return False
    else:
        unique_members.add(member)

    return True, house


def main():
    alliance_members = set() # All alliance members
    enemies_seen = set() # All enemies that some alliance member wants to kill
    houses = set() # All houses
    
    line = sys.stdin.readline()
    
    # Validate first line
    first_line_validation = validate_first_line(line)
    if not first_line_validation:
        sys.exit(44)
    a, e, h = first_line_validation

    # Validate all alliance members lines
    for _ in range(a):
        line = sys.stdin.readline()
        valid, name, enemies = validate_alliance_member_line(line, enemies_seen, alliance_members)
        if not valid:
            sys.exit(43)
        alliance_members.add(name)
        enemies_seen.update(enemies.split())
    
    print(len(alliance_members))
    # Check that there are number of alliance members as expected
    if len(alliance_members) != a:
        sys.exit(43)
    
    # Check that there are not more enemies than expected
    if len(enemies_seen) > e:
        sys.exit(43)
    
    # Validate all house lines
    for _ in range(h):
        line = sys.stdin.readline()
        valid, house = validate_house_line(line, enemies_seen, houses)
        if not valid:
            sys.exit(43)
        houses.add(house)
            
    # Check that there are number of houses as expected
    if len(houses) != h:
        sys.exit(43)

    # Check that there are no more lines
    if sys.stdin.readline() != "":
        sys.exit(43)
    
    # Success
    sys.exit(42)

if __name__ == "__main__":
    main()