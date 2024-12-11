import sys
import re

# Assuming of the form: mul(d,d)
def parse_mult(mult: str) -> int:
    inner_expr = mult[4:-1]
    parts = inner_expr.split(",")
    assert len(parts) == 2, "should only be 2 parts!"
    
    left, right = int(parts[0]), int(parts[1])
    return left * right

# For part 2: extract the sections around do() and don't()
def extract_enabled(line: str) -> str:
    result = ""
    
    parts = line.split("don't()")
    if parts[0]:
        result += parts[0]
    
    for part in parts[1:]:
        do_segments = part.split('do()')
        for segment in do_segments[1:]:
            result += segment
            
    return result

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python <script> <filepath>")
        sys.exit(1)
        
    filepath: str = sys.argv[1]
    contents = open(filepath, "r").read()
   
    mult_pattern = re.compile(r'mul\(\d{1,3},\d{1,3}\)')
    # Part 1
    matches = re.findall(mult_pattern, contents)
    print(f"Part 1: {sum(map(parse_mult, matches))}")

    # Part 2
    enabled_contents = extract_enabled(contents)
    enabled_matches = re.findall(mult_pattern, enabled_contents)
    print(f"Part 2: {sum(map(parse_mult, enabled_matches))}")

if __name__ == "__main__":
    main()
