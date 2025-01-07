import sys
from typing import Dict, List, Optional, Tuple, TypeAlias
from heapq import heappop, heappush

# Input Parsing
raw: List[str] = open(sys.argv[1], "r").read().splitlines()

max_dim = 0
Coord: TypeAlias = Tuple[int,int];
coords: List[Coord] = []

for line in raw:
    x,y = map(int, line.split(","))
    coords.append((x,y))
    max_dim = max(max_dim, x, y)

# Memory Space
BYTES_TO_READ = 1024
CORRUPTED = "#"

grid = [["." for _ in range(max_dim + 1)] for _ in range(max_dim + 1)]
def show_grid(grid: List[List[str]]) -> None:
    rows = ["".join(row) for row in grid]
    print("\n".join(rows))

for x,y in coords[:BYTES_TO_READ]:
    grid[y][x] = CORRUPTED

# Shortest Path Solution
def shortest_path(grid: List[List[str]], start: Coord, end: Coord) -> Optional[int]:
    directions = [[1,0], [-1,0], [0,1], [0,-1]]
    sx, sy = start
    ex, ey = end

    pq = [(0, sx, sy)]
    distances: Dict[Coord, int] = dict()
    distances[(sx, sy)] = 0

    def is_valid(x: int, y: int) -> bool: return 0 <= x < len(grid) and 0 <= y < len(grid) and grid[y][x] != CORRUPTED

    while pq:
        cost, x, y = heappop(pq)
        if (x, y) == (ex, ey):
            return cost
        
        for dx, dy in directions:
            newx, newy = x + dx, y + dy
            if is_valid(newx, newy):
                new_cost = cost + 1
                if (newx, newy) not in distances or new_cost < distances[(newx, newy)]:
                    distances[newx, newy] = new_cost
                    heappush(pq, (new_cost, newx, newy))

    return None # End state couldn't be reached

print(F"Part 1: {shortest_path(grid=grid, start=(0,0), end=(max_dim, max_dim))}")

#  Part 2, binary search remaining coordinates
def binary_search_coords(grid: List[List[str]], coords: List[Coord]) -> Optional[Coord]:
    left, right = 0, len(coords) - 1
    result: Coord = None
    while left <= right:
        mid = (left + right) // 2
        
        for i in range(left, mid + 1):
            x, y = coords[i]
            grid[y][x] = CORRUPTED

        path_cost = shortest_path(grid, (0, 0), (max_dim, max_dim))
        
        if path_cost is not None:
            left = mid + 1
        else:
            result = (coords[mid][0], coords[mid][1])
            for i in range(left, mid + 1):
                x, y = coords[i]
                grid[y][x] = "."
            
            right = mid - 1
            
    return result

remaining_coords = coords[BYTES_TO_READ:]
stop_coord = binary_search_coords(grid, remaining_coords)
print(f"Part 2: {stop_coord[0]},{stop_coord[1]}")