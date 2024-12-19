import re
import sys
from typing import List, Set
from itertools import permutations

parts = open(sys.argv[1], "r").read().split("\n\n")
available_patterns = parts[0].split(", ")
designs = parts[1].split("\n")

print(available_patterns, designs)

def can_be_made_from_substrings(target: str, substrings: List[str]) -> bool:
    reg = re.compile("(?:" + "|".join(substrings) + ")*$")
    if reg.match(target) != None:
        return True
    
    return False

                

print(f"Part 1: {sum([can_be_made_from_substrings(design, available_patterns) for design in designs])}")
