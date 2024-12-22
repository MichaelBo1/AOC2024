from math import floor
import sys
from typing import Dict, List, Tuple
from collections import Counter, defaultdict

NUM_SECRETS = 2000
PRUNING_VALUE = 16777216
initial_secrets = list(map(int, open(sys.argv[1], "r").read().splitlines()))

def next_secret(secret: int) -> int:
    secret = (secret ^ (secret * 64)) % PRUNING_VALUE
    secret = (secret ^ floor(secret / 32)) % PRUNING_VALUE
    return (secret ^ (secret * 2048)) % PRUNING_VALUE

def secret_generator(seed: int):
    current_secret = seed
    while True:
        current_secret = next_secret(current_secret)
        yield current_secret


def get_diff_sequences(secrets: List[int]) -> Dict[Tuple[int,int,int,int], int]:
    prices = [secret % 10 for secret in secrets]
    diffs = [prices[i+1] - prices[i] for i in range(len(prices) - 1)]
    sequences: Dict[Tuple[int,int,int,int], int] = dict()
    left, right = 0, 3
    
    while right < len(diffs):
        seq = tuple(diffs[left: right+1])
        if seq not in sequences:
            sequences[seq] = prices[right+1]
        left += 1
        right += 1
    
    return sequences
    
p1 = 0
p2 = Counter()

for seed in initial_secrets:
    gen = secret_generator(seed=seed)
    secrets = [next(gen) for _ in range(NUM_SECRETS)]
    
    p1 += secrets[-1]
    
    p2 += get_diff_sequences([seed] + secrets)  


print(f"Part 1: {p1}")
print(f"Part 2: {max(p2.values())}")



