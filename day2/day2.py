import sys
from typing import List

def check_monotonic(report: List[int]) -> bool:
    if all([report[i] < report[i+1] for i in range(len(report) - 1)]):
        return True
    if all([report[i] > report[i+1] for i in range(len(report) - 1)]):
        return True
    return False

def check_report(report: List[int]) -> bool:    
    left, right = 0, 1    
    while right < len(report):
        diff = report[left] - report[right]
        is_safe_diff = (abs(diff) in range(1,4)) and (diff != 0)
        if not is_safe_diff:
            return False
        
        left += 1
        right += 1
    
    return check_monotonic(report)

# Part 2: ending up being a brute-force over each possible version with one number removed
def check_report_with_dampener(report: List[int]) -> bool:
    if check_report(report):
        return True
    
    reports_without_index = [report[:i] + report[i+1:] for i in range(len(report))]
    
    for r in reports_without_index:
        if check_report(r):
            return True
        
    return False

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python <script> <filepath>")
        sys.exit(1)
        
    filepath: str = sys.argv[1]
    
    with open(filepath, "r") as fhand:
        lines = map(lambda x: x.rstrip("\n").split(" "), fhand.readlines())
        reports = [[int(n) for n in line] for line in lines]
        
        num_safe_reports = sum(map(check_report, reports))
        print(f"Part1: {num_safe_reports}")
        
        print(f"Part2:", sum(map(check_report_with_dampener, reports)))

if __name__ == "__main__":
    main()
