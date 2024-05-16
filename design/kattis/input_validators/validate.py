#!/usr/bin/env python3
import sys
import re

def validate_first_line(line):    
    # Check that line matches regex
    match = re.match(r"^(0|[1-9][0-9]*) (0|[1-9][0-9]*) (0|[1-9][0-9]*)\r?\n$", line)
    if not match:
        return False
    a, e, h = map(int, match.groups())
    
    # Check that numbers are within limits
    if not (1 <= a <= 100 and 1 <= e <= 100 and 0 <= h <= e):
        return False
    
    return (a, e, h)

def validate_alliance_member_line(line, alliance_members, e):
    # Check that the line matches the regex
    match = re.match(r"^([A-Za-z]+) (0|[1-9][0-9]*) ((?:[A-Za-z]+ ?)+)\r?\n$", line)
    if not match:
        return False, None, None
    name, capacity, enemies = map(str, match.groups())

    # Check capacity is within limits
    if not (0 <= int(capacity) <= e):
        return False, None, None 
        
   # Check if we already have seen this name before
    if name in alliance_members:
        return False, None, None
    
    # Initialize sets to keep track of enemies names
    unique_enemies = set()
    
    # Check if each enemy is unique
    for enemy in enemies.split():
        if enemy in unique_enemies:
            return False, None, None
    else:
        unique_enemies.add(enemy)
    
    return True, name, enemies

def validate_house_line(line, enemies_seen, houses):
    # Check that the line matches the regex
    match = re.match(r"^([A-Za-z]+) ((?:[A-Za-z]+ ?)+) (0|[1-9][0-9]*)\r?\n$", line)
    if not match:
        return False, None
    house, members, capacity = map(str, match.groups())

    # Check capacity is less than number of members
    if not (0 <= int(capacity) <= members.count(" ") + 1):
        return False, None
    
    # Check that members are some known enemies
    for member in members.split():
        if member not in enemies_seen:
            return False, None
        
    #Check if we already has seen this house before         
    if house in houses:
        return False, None
        
   # Check that the same member is not used twice in the same line
   # Initialize sets to keep track of members names
    unique_members = set()
    # Check if each member is unique
    for member in members.split():
        if member in unique_members:
            return False, None
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
        sys.exit(43)
    a, e, h = first_line_validation

    # Validate all alliance members lines
    for _ in range(a):
        line = sys.stdin.readline()
        valid, name, enemies = validate_alliance_member_line(line, alliance_members, e)
        if not valid:
            sys.exit(43)
        alliance_members.add(name)
        enemies_seen.update(enemies.split())
    
    print(len(alliance_members))
    # Check that there are not more allies than expected
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
            
    # Check that there are not more houses than expected
    if len(houses) != h:
        sys.exit(43)

    # Check that there are no more lines
    if sys.stdin.readline() != "":
        sys.exit(43)
    
    # Success
    sys.exit(42)

if __name__ == "__main__":
    main()