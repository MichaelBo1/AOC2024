import sys
from typing import Dict, List, Set, Tuple
from collections import defaultdict
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

def shortest_path(grid: List[str], start: Tuple[int, int] , end: Tuple[int, int]) -> Tuple[int,int]:
    start_row, start_col = start
    end_row, end_col = end

    pq = [(0, start_row, start_col, 'E')]

    distances: Dict[Tuple[int, int, str], int] = dict()
    distances[(start_row, start_col, 'E')] = 0

    predecessors: Dict[Tuple[int, int, str], List[Tuple[int, int, str]]] = defaultdict(list)

    while pq:
        cost, row, col, direction = heappop(pq)
        
        dr, dc = directions[direction]
        newr, newc = row + dr, col + dc
        if is_valid(row=newr, col=newc, grid=grid):
            new_cost = cost + MOVE_COST
            if (newr, newc, direction) not in distances or new_cost < distances[(newr, newc, direction)]:
                distances[(newr, newc, direction)] = new_cost
                predecessors[(newr, newc, direction)].append((row, col, direction))
                heappush(pq, (new_cost, newr, newc, direction))
            elif new_cost == distances[(newr, newc, direction)]:
                        predecessors[(newr, newc, direction)].append((row, col, direction))

        for new_dir, (dr, dc) in directions.items():
            if new_dir != direction:
                newr, newc = row + dr, col + dc
                if is_valid(row=newr, col=newc, grid=grid):
                    new_cost = cost + TURN_COST + MOVE_COST
                    if (newr, newc, new_dir) not in distances or new_cost < distances[(newr, newc, new_dir)]:
                        distances[(newr, newc, new_dir)] = new_cost
                        predecessors[(newr, newc, new_dir)].append((row, col, direction))
                        heappush(pq, (new_cost, newr, newc, new_dir))
                    elif new_cost == distances[(newr, newc, new_dir)]:
                        predecessors[(newr, newc, new_dir)].append((row, col, direction))

    goal_states = [(cost, row, col, dr) for (row, col, dr), cost in distances.items() if (row, col) == (end_row, end_col)]
    min_cost = min(goal_states)[0]

    unique_in_shortest: Set[Tuple[int, int]] = set()

    def backtrack(current_state: Tuple[int, int, str]):
        row, col, _ = current_state
        unique_in_shortest.add((row, col))
        for predecessor in predecessors.get(current_state, []):
            backtrack(current_state=predecessor)

    shortest_path_goals = [gs for gs in goal_states if gs[0] == min_cost]
    for _, row, col, dr in shortest_path_goals:
        backtrack(current_state=(row, col, dr))

    tiles = len(unique_in_shortest)
    return min_cost, tiles


def main() -> None:
    if len(sys.argv) < 2:
        raw = EXAMPLE_2.splitlines()
    else:
        raw = open(sys.argv[1], "r").read().splitlines()
    
    src, end = get_source_dest(grid=raw)    
    path_len, positions = shortest_path(grid=raw, start=src, end=end)
    print(f"Part 1: {path_len}")
    print(f"Part 2: {positions}")

if __name__ == "__main__":
    main()