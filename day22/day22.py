from math import floor
import sys

EXAMPLE = """1
10
100
2024
"""

PRUNING_VALUE = 16777216

initial_secrets = list(map(int, open(sys.argv[1], "r").read().splitlines()))

def next_secret(secret: int) -> int:
    secret = (secret ^ (secret * 64)) % PRUNING_VALUE
    secret = (secret ^ floor(secret / 32)) % PRUNING_VALUE
    return (secret ^ (secret * 2048)) % PRUNING_VALUE

def nth_secret(seed: int, n: int) -> int:
    result = seed
    for _ in range(n):
        result = next_secret(secret=result)

    return result

print(f"Part 1: {sum(nth_secret(seed=seed, n=2000) for seed in initial_secrets)}")

