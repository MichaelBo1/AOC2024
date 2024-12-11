import sys
from typing import List, Set, Tuple, Optional
    
ORIENTATIONS = ["^", ">", "v", "<"]
MOVEMENTS = [[-1,0], [0, 1], [1, 0], [0, -1]]

def move(pos: Tuple[int, int], orientation: int) -> Tuple[int, int]:
    dx, dy = MOVEMENTS[orientation]
    x,y = pos
    return (x + dx, y + dy)

def parse(grid: List[str]) -> Tuple[Set[Tuple[int,int]], Tuple[int,int], int, Tuple[int, int]]:
    rows, cols = len(grid), len(grid[0])
    obstacles: Set[Tuple[int,int]] = set()
    guard_pos: Tuple[int,int]
    guard_orientation: int
    for row, line in enumerate(grid):
        for i, ch in enumerate(line):
            if ch == "#":
                obstacles.add((row, i))
            elif ch in ORIENTATIONS:
                guard_pos = (row, i)
                guard_orientation = ORIENTATIONS.index(ch)
    
    return obstacles, guard_pos, guard_orientation, (rows, cols)

def get_path(obstacles: Set[Tuple[int,int]], pos: Tuple[int,int], orientation: int, dim: Tuple[int, int]) -> Optional[Set[Tuple[int,int]]]:
    visited: Set[Tuple[int,int,int]] = set() # record orientation to check for loops
    visited.add((pos[0], pos[1], orientation))
    
    def out_of_bounds(pos: Tuple[int, int]) -> bool:
        return pos[0] < 0 or pos[1] < 0 or pos[0] >= dim[0] or pos[1] >= dim[1]
    
    while True:
        new_pos = move(pos=pos, orientation=orientation)
        if out_of_bounds(pos=new_pos): 
            break
        if new_pos in obstacles:
            orientation = (orientation + 1) % 4
        else:
            # We've looped if we re-visit in the same orientation
            if (new_pos[0], new_pos[1], orientation) in visited:
                return None
            
            pos = new_pos
            visited.add((pos[0], pos[1], orientation))
                
    return {p[:2] for p in visited}

def part1(grid: List[str]) -> int:    
    obstacles, guard_pos, guard_orientation, dim = parse(grid=grid)
    visited = get_path(obstacles, guard_pos, guard_orientation, dim)
    assert visited is not None
    return len(visited)

def part2(grid: List[str]) -> int:    
    obstacles, guard_pos, guard_orientation, dim = parse(grid=grid)
    visited = get_path(obstacles, guard_pos, guard_orientation, dim)
    assert visited is not None
    loops = 0
    
    for pos in visited:
        if pos in obstacles:
            continue
        if (guard_pos[0] == pos[0] and guard_pos[1] == pos[1]): 
            continue
        
        obstacles.add(pos)
        
        if get_path(obstacles, guard_pos, guard_orientation, dim) is None:
            loops += 1
            
        obstacles.remove(pos)
        
    return loops

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python <script> <filepath>")
        sys.exit(1)

    filepath = sys.argv[1]
    lines = list(map(lambda x: x.rstrip("\n"), open(filepath, "r").readlines()))
    
    # Part 1
    print(f"Part 1: {part1(grid=lines)}")
    print(f"Part 2: {part2(grid=lines)}")

if __name__ == "__main__":
    main()
