import sys
from typing import List

DIRECTIONS = [
    [1,0],
    [0,1],
    [-1,0],
    [0,-1],
    [1,1],
    [1,-1],
    [-1,1],
    [-1,-1]
]

DIAGONALS = [
    [1,1],
    [1,-1],
    [-1,1],
    [-1,-1]
]
def part1(grid: List[str]) -> int:
    rows, cols = len(grid), len(grid[0])
    xs: List[List[int]] = []
    # Only care about X in the grid, to check for matches
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "X":
                xs.append([row, col])

    def in_bounds(row: int, col: int) -> bool:
        return row >= 0 and col >= 0 and row < rows and col < cols
    
    def count_matches(row: int, col: int) -> int:
        matches = 0 
        for dx, dy in DIRECTIONS:
            word = []
            newr, newc = row, col
            for _ in range(4):
                if not in_bounds(newr, newc):
                    break
                word.append(grid[newr][newc])
                newr += dx
                newc += dy
                
            assert len(word) <= 4
            if word == list("XMAS") or word == list("XMAS")[::-1]:
                matches += 1
        return matches
    
    return sum([count_matches(x[0], x[1]) for x in xs])

def part2(grid: List[str]) -> int:
    rows, cols = len(grid), len(grid[0])
    a_chars = []
    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == "A":
                a_chars.append([row, col])
                
    def in_bounds(row: int, col: int) -> bool:
        return row >= 0 and col >= 0 and row < rows and col < cols
    
    def count_crosses(row: int, col: int) -> bool:
        crosses = []
        for dx, dy in DIAGONALS:
            newr = row + dx
            newc = col + dy
            if not in_bounds(newr, newc):
                continue
            
            crosses.append(grid[newr][newc])
        
        
        res =  (
            crosses.count("S") == 2 and
            crosses.count("M") == 2 and
            crosses[0] != crosses[-1]
        )
        return res
            
    return sum([count_crosses(a[0], a[1]) for a in a_chars])

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python <script> <filepath>")
        sys.exit(1)
    filepath = sys.argv[1]
    lines = open(filepath, "r").read().rstrip("\n").split("\n")
    
    #  === Bit hacky and convoluted, but correct===
    print(f"Part 1: {part1(grid=lines)}")
    print(f"Part 2: {part2(grid=lines)}")

    
if __name__ == "__main__":
    main()
