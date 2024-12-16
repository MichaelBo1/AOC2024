import sys
from typing import Dict, List, Set, Tuple, Deque
from collections import deque
from heapq import heappop, heappush

EXAMPLE = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
"""

EXAMPLE_2 = """#################
#...#...#...#..E#
#.#.#.#.#.#.#.#.#
#.#.#.#...#...#.#
#.#.#.#.###.#.#.#
#...#.#.#.....#.#
#.#.#.#.#.#####.#
#.#...#.#.#.....#
#.#.#####.#.###.#
#.#.#.......#...#
#.#.###.#####.###
#.#.#...#.....#.#
#.#.#.#####.###.#
#.#.#.........#.#
#.#.#.#########.#
#S#.............#
#################
"""

TURN_COST = 1000
MOVE_COST = 1

directions = {
    'N': (-1, 0),
    'E': (0, 1),
    'S': (1, 0),
    'W': (0, -1)
} 

def get_source_dest(grid: List[str]) -> Tuple[Tuple[int,int], Tuple[int,int]]:
    src: Tuple[int, int]
    dest: Tuple[int, int]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                src = (i,j)
            elif grid[i][j] == "E":
                dest = (i,j)
    
    return src, dest

def is_valid(row: int, col: int, grid: List[str]) -> bool:
    return 0 <= row < len(grid) and 0 <= col < len(grid[0]) and grid[row][col] != "#"

def shortest_path(grid: List[str], start: Tuple[int, int] , end: Tuple[int, int], print_path=True) -> int:
    start_row, start_col = start
    end_row, end_col = end

    pq = [(0, start_row, start_col, 'E')]

    distances: Dict[Tuple[int, int, str], int] = dict()
    distances[(start_row, start_col, 'E')] = 0

    prev = dict()
    while pq:
        cost, row, col, direction = heappop(pq)
        
        if (row, col) == (end_row, end_col):
            path = []
            current = (row, col, direction)
            while current in prev:
                path.append(current)
                current = prev[current]
            path.append((start_row, start_col, 'E'))
            if (print_path): print(path[::-1])
            return cost
        
        dr, dc = directions[direction]
        newr, newc = row + dr, col + dc
        if is_valid(row=newr, col=newc, grid=grid):
            new_cost = cost + MOVE_COST
            if (newr, newc, direction) not in distances or new_cost < distances[(newr, newc, direction)]:
                distances[(newr, newc, direction)] = new_cost
                prev[(newr, newc, direction)] = (row, col, direction)
                heappush(pq, (new_cost, newr, newc, direction))

        for new_dir, (dr, dc) in directions.items():
            if new_dir != direction:
                newr, newc = row + dr, col + dc
                if is_valid(row=newr, col=newc, grid=grid):
                    new_cost = cost + TURN_COST + MOVE_COST
                    if (newr, newc, new_dir) not in distances or new_cost < distances[(newr, newc, new_dir)]:
                        distances[(newr, newc, new_dir)] = new_cost
                        prev[(newr, newc, new_dir)] = (row, col, direction)
                        heappush(pq, (new_cost, newr, newc, new_dir))
                
    return 0


def main() -> None:
    if len(sys.argv) < 2:
        raw = EXAMPLE_2.splitlines()
    else:
        raw = open(sys.argv[1], "r").read().splitlines()
    
    # Part 1
    src, end = get_source_dest(grid=raw)
    print(shortest_path(grid=raw, start=src, end=end, print_path=False))
if __name__ == "__main__":
    main()