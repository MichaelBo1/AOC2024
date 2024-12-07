import sys
from itertools import product
from typing import Dict, List

def parse_equations(raw: List[str]) -> Dict[int, List[int]]:
    equations: Dict[int, List[int]] = dict()
    for line in raw:
        part1, part2 = line.split(":")
        total = int(part1)
        operands = [int(n) for n in part2.lstrip(" ").split(" ")]
        equations[total] = operands
     
    return equations

def can_make_total(total: int, operands: List[int]) -> bool:
    for operators in product(["+", "*"], repeat=len(operands) - 1):
        result = operands[0]
        for i, op in enumerate(operators):
            if op == "+":
                result += operands[i+1]
            elif op == "*":
                result *= operands[i+1]
        
        if result == total:
            return True
        
    return False

# It's pretty slow on the larger inputs, but hey, works for now...
def concat(a: int, b: int) -> int:
    return int(str(a) + str(b))

def can_make_total_with_concat(total: int, operands: List[int]) -> bool:
    for operators in product(["+", "*", "||"], repeat=len(operands) - 1):
        result = operands[0]
        for i, op in enumerate(operators):
            if op == "+":
                result += operands[i+1]
            elif op == "*":
                result *= operands[i+1]
            elif op == "||":
                result = concat(a=result, b=operands[i+1])
        
        if result == total:
            return True
        
    return False

def part1(equations: Dict[int, List[int]]) -> int:
    total = 0
    for k,v in equations.items():
        if can_make_total(total=k, operands=v):
            total += k
            
    return total
        
def part2(equations: Dict[int, List[int]]) -> int:
    total = 0
    for k,v in equations.items():
        if can_make_total_with_concat(total=k, operands=v):
            total += k
            
    return total

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python <script> <filepath>")
        sys.exit(1)
    filepath = sys.argv[1]
    raw = open(filepath, "r").read().splitlines()

    equations = parse_equations(raw=raw)
    print("Part 1:", part1(equations=equations))
    # print(can_make_total(total=190, operands=[10, 19]))
    print("Part 2:", part2(equations=equations))
if __name__ == "__main__":
    main()
