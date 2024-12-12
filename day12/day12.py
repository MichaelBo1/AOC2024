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

def calculate_price(plot: List[List[str]]) -> Tuple[int, int]:
    rows, cols = len(plot), len(plot[0])
    directions = [[1,0], [-1,0], [0,1], [0,-1]]
    visited: Set[Tuple[int,int]] = set()

    def in_bounds(r: int, c: int) -> bool:
        return 0 <= r < rows and 0 <= c < cols
     
    def bfs_region(r: int, c: int) -> Tuple[int, Set[Tuple[int, int]]]:
        q: Deque[Tuple[int, int]] = deque()
        region: Set[Tuple[int, int]] = set()
        perimeter = 0
        plant_type = plot[r][c]

        q.append((r,c))
        visited.add((r,c))
        region.add((r,c))

        while q:
            row, col = q.popleft()
            for dr, dc in directions:
                newr, newc = row + dr, col + dc

                if not in_bounds(newr, newc) or plot[newr][newc] != plant_type:
                    perimeter += 1
                    continue
                
                if (newr, newc) not in visited:
                    q.append((newr, newc))
                    visited.add((newr, newc))
                    region.add((newr, newc))
        
        return region, perimeter

    p1 = 0
    p2 = 0
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                region, perimeter = bfs_region(row, col)
                p1 += len(region) * perimeter
    
    return p1, p2



def main() -> None:
    if len(sys.argv) < 2:
        raw = EXAMPLE_SMALL.splitlines()
    else:
        raw = open(sys.argv[1], "r").read().splitlines()

    puzzle = [list(line) for line in raw]
    p1, p2 = calculate_price(plot=puzzle)
    print(f"Part 1: {p1}")

        
if __name__ == "__main__":
    main()