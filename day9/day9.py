import sys
from typing import List, Optional
from math import prod

# Quick and dirty parse into a "memory" array
def parse_memory(raw: str) -> List[Optional[int]]:
    memory: List[Optional[int]] = list()
    current_id = 0

    for i, ch in enumerate(raw):
        if i % 2 == 0:
            memory.extend([current_id] * int(ch))
            current_id += 1
        else:
            memory.extend([None] * int(ch))    
    return memory

def find_next_last(lst: List[Optional[int]]):
    for i in range(len(lst) - 1, -1, -1):
        if lst[i] is not None:
            yield lst[i]

def pack_memory(memory: List[Optional[int]]) -> List[int]:
    packed: List[int] = list()
    gen = find_next_last(lst=memory)
    mem_len = len([n for n in memory if n is not None])
    for n in memory:
        if len(packed) == mem_len:
            break
        if n is not None:
            packed.append(n)
        else:
            disk_id = next(gen)
            packed.append(disk_id)

    return packed

def check_sum(lst: List[int]) -> int:
    return sum(i * n for i, n in enumerate(lst))

def part1(raw: str) -> int:
    memory = parse_memory(raw=raw)
    packed = pack_memory(memory=memory)
    return check_sum(lst=packed)

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python <script> <filepath>")
        sys.exit(1)
    filepath = sys.argv[1]
    raw = open(filepath, "r").read().rstrip("\n")

    print(f"Part 1: {part1(raw=raw)}")

if __name__ == "__main__":
    main()
