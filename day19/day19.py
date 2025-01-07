import sys
from typing import Tuple
from functools import cache

parts = open(sys.argv[1], "r").read().split("\n\n")
available_patterns = tuple(parts[0].split(", "))
designs = parts[1].split("\n")

@cache
def design_solutions(design: str, patterns: Tuple[str, ...]) -> int:
    if design == "": return 1
    return sum(design_solutions(design.removeprefix(p), patterns) for p in patterns if design.startswith(p))

            
print(f"Part 1: {sum(1 for design in designs if design_solutions(design, available_patterns) > 0)}")
print(f"Part 2: {sum(design_solutions(design, available_patterns) for design in designs if design_solutions(design, available_patterns) > 0)}")