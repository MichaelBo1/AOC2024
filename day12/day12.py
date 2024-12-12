import sys
from typing import Dict, List, Set, Tuple, Deque
from collections import deque

EXAMPLE_SMALL = """AAAA
BBCD
BBCC
EEEC
"""

EXAMPLE_LARGE = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

MARKED_SQUARE = "#"

def calculate_price(plot: List[List[str]]):
    rows, cols = len(plot), len(plot[0])
    directions = [[1,0], [-1,0], [0,1], [0,-1]]
    visited: Set[Tuple[int,int]] = set()

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < rows and 0 <= c < cols
     
    def bfs_region(r: int, c: int) -> Tuple[int, int]:
        q: Deque[Tuple[int,int]] = deque()
        area = 1
        perimeter = 0
        plant_type = plot[r][c]

        q.append((r,c))
        visited.add((r,c))

        while q:
            row, col = q.popleft()
            connections = 0 
            for dr, dc in directions:
                newr, newc = row + dr, col + dc
                if not in_bounds(newr, newc):
                    continue

                if plot[newr][newc] != plant_type:
                    continue
                
                connections += 1

                if (newr, newc) not in visited:
                    q.append((newr, newc))
                    visited.add((newr, newc))
                    area += 1
            perimeter += 4 - connections
        
        return area, perimeter

    cost = 0
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                area, perimeter = bfs_region(row, col)
                cost += area * perimeter
    
    return cost



def main() -> None:
    if len(sys.argv) < 2:
        raw = EXAMPLE_SMALL.splitlines()
    else:
        raw = open(sys.argv[1], "r").read().splitlines()

    puzzle = [list(line) for line in raw]
    print(f"Part 1: {calculate_price(puzzle)}")

        
if __name__ == "__main__":
    main()