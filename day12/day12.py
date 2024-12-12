import sys
from typing import List, Set, Tuple, Deque
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
def find_region(grid: List[List[str]], row: int, col: int, visited: Set[Tuple[int, int]]) -> Tuple[int, int, int]:
    q: Deque[Tuple[int, int]] = deque()
    area = 1
    perimeter = 0
    corners = 0 # no. of corners == no. of sides

    def grid_value(r: int, c: int) -> str:
        if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
            return grid[r][c]
        return ""
    
    q.append((row,col))
    visited.add((row, col))

    while q:
        cur_row, cur_col = q.popleft()
        cur_ch = grid_value(r=cur_row, c=cur_col)
        
        ch_up = grid_value(r=cur_row-1, c=cur_col)
        ch_down = grid_value(r=cur_row+1, c=cur_col)
        ch_left = grid_value(r=cur_row, c=cur_col-1)
        ch_right = grid_value(r=cur_row, c=cur_col+1)

        # Perimeter is anything around the current square that isn't part of the connected region
        if ch_up != cur_ch:
            perimeter += 1        
        if ch_down != cur_ch:
            perimeter += 1        
        if ch_left != cur_ch:
            perimeter += 1        
        if ch_right != cur_ch:
            perimeter += 1

        # Corners will equal the number of sides we have -> we look at external corners
        if ch_up != cur_ch and ch_right != cur_ch:
            corners += 1
        if ch_right != cur_ch and ch_down != cur_ch:
            corners += 1
        if ch_down != cur_ch and ch_left != cur_ch:
            corners += 1
        if ch_left != cur_ch and ch_up != cur_ch:
            corners += 1

        if grid_value(cur_row-1, cur_col-1) != cur_ch and ch_up == cur_ch and ch_left == cur_ch:
            corners += 1
        if grid_value(cur_row-1, cur_col+1) != cur_ch and ch_up == cur_ch and ch_right == cur_ch:
            corners += 1
        if grid_value(cur_row+1, cur_col+1) != cur_ch and ch_down == cur_ch and ch_right == cur_ch:
            corners += 1
        if grid_value(cur_row+1, cur_col-1) != cur_ch and ch_down == cur_ch and ch_left == cur_ch:
            corners += 1        
        


        # Then add matching unvisited neighbours to continue search
        if ch_up == cur_ch and (cur_row-1, cur_col) not in visited:
            area += 1
            q.append((cur_row-1, cur_col))
            visited.add((cur_row-1, cur_col))

        if ch_down == cur_ch and (cur_row+1, cur_col) not in visited:
            area += 1
            q.append((cur_row+1, cur_col))
            visited.add((cur_row+1, cur_col))

        if ch_left == cur_ch and (cur_row, cur_col-1) not in visited:
            area += 1
            q.append((cur_row, cur_col-1))
            visited.add((cur_row, cur_col-1))

        if ch_right == cur_ch and (cur_row, cur_col + 1) not in visited:
            area += 1
            q.append((cur_row, cur_col + 1))
            visited.add((cur_row, cur_col + 1))
    return area, perimeter, corners
 
def calculate_field_price(grid: List[List[str]]):
    rows, cols = len(grid), len(grid[0])
    visited: Set[Tuple[int,int]] = set()

    part1 = 0
    part2 = 0
    for row in range(rows):
        for col in range(cols):
            if (row, col) not in visited:
                area, perimeter, corners = find_region(grid=grid, row=row, col=col, visited=visited)
                part1 += area * perimeter
                part2 += area * corners

    print(f"Part 1: {part1}")
    print(f"Part 2: {part2}")

def main() -> None:
    if len(sys.argv) < 2:
        raw = EXAMPLE_SMALL.splitlines()
    else:
        raw = open(sys.argv[1], "r").read().splitlines()

    puzzle = [list(line) for line in raw]
    calculate_field_price(grid=puzzle)
        
if __name__ == "__main__":
    main()