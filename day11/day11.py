import sys
from typing import Dict, List, Tuple
from threading import Thread
from functools import cache

EXAMPLE = "125 17"
MULTIPLIER = 2024

def apply_rules(stone: int) -> List[int]:
    if stone == 0:
        return [1]
    
    numstr = str(stone)
    if len(numstr) % 2 == 0:
        return [int(numstr[:len(numstr) // 2]), int(numstr[len(numstr) // 2:])]

    return [stone * MULTIPLIER]

memo: Dict[Tuple[int, int], int] = dict()
def solve(stone: int, iterations: int) -> int:    
    if (stone, iterations) in memo:
        return memo[stone, iterations]
    
    products = apply_rules(stone)
    if iterations == 0:
        return len(products)
    
    result = sum(solve(st, iterations - 1) for st in products)
    memo[stone, iterations] = result
    return result

def main() -> None:
    if len(sys.argv) < 2:
        raw = EXAMPLE.split(" ")
    else:
        raw = open(sys.argv[1], "r").read().split(" ")

    stones = [int(n) for n in raw]
    print(f"Part 1: {sum(solve(stone, 25 - 1) for stone in stones)}")
    print(f"Part 2: {sum(solve(stone, 75 - 1) for stone in stones)}")

        
if __name__ == "__main__":
    main()