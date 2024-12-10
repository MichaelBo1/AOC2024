import sys
from typing import List, Optional, Tuple, Deque
from collections import deque

def count_trails(grid: List[List[int]], target=9) -> int:
    rows, cols = len(grid), len(grid[0])
    directions = [[1,0], [-1,0], [0,1], [0,-1]]
    
    def bfs(row: int, col: int) -> int:
        q = deque([(row, col, 0)])
        visited = set()
        
        while q:
            row, col, current_height = q.popleft()
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if (
                    0 <= nr < rows and 0 <= nc < cols and
                    grid[nr][nc] == current_height + 1 and
                    (nr, nc) not in visited
                ):
                    q.append((nr, nc, grid[nr][nc]))
                    visited.add((nr, nc))
           
        return len([grid[nr][nc] for nr, nc in visited if grid[nr][nc] == target])  
       
    total = 0      
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:
                total  += bfs(i, j)

    return total

def count_ratings(grid: List[List[int]], target=9) -> int:
    rows, cols = len(grid), len(grid[0])
    directions = [[1,0], [-1,0], [0,1], [0,-1]]
    total_ratings = 0
    
    def bfs(row: int, col: int) -> int:
        q = deque([(row, col, 0)])
        total = 0
        while q:
            row, col, current_height = q.popleft()
            if current_height == target:
                total += 1
                continue
            
            for dr, dc in directions:
                nr, nc = row + dr, col + dc
                if (
                    0 <= nr < rows and 0 <= nc < cols and
                    grid[nr][nc] == current_height + 1
                ):
                    q.append((nr, nc, grid[nr][nc]))
                   
        return total
    
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == 0:
                total_ratings += bfs(i, j)

    return total_ratings
               
def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python <script> <filepath>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    raw = open(filepath, "r").read().splitlines()
    puzzle_grid = [[int(ch) for ch in row] for row in raw]
    print(puzzle_grid)
    print(f"Part 1: {count_trails(grid=puzzle_grid)}")
    print(f"Part 2: {count_ratings(grid=puzzle_grid)}")
    

if __name__ == "__main__":
    main()
