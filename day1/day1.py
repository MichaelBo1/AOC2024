import sys

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python <script> <filepath>")
        sys.exit(1)
    filepath: str = sys.argv[1]
    
    with open(filepath, "r") as fhand:
        lines = map(lambda x: x.rstrip("\n").split("   "), fhand.readlines())

        left, right = list(zip(*[(int(line[0]), int(line[1])) for line in lines]))
        assert len(left) == len(right), "unequal lengths"

        part1 = sum(map(lambda x: abs(x[0] - x[1]), zip(sorted(left), sorted(right))))
        print("Result Part 1:", part1)

        # part 2
        part2 = sum([l * (l==r) for r in right for l in left])
        print("Result Part 2:", part2)
if __name__ == "__main__":
    main()
