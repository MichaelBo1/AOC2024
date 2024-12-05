import sys
from functools import cmp_to_key
from collections import defaultdict
from typing import Dict, List, Set
    
def is_valid_update(update: List[str], rule_orders: Dict[str, Set[str]]) -> bool:
    seen = set()
    for page_num in update:
        after_current = rule_orders[page_num]
        if seen.intersection(after_current):
            return False
        seen.add(page_num)
    
    return True

def compare(x: str, y:str, rule_orders: Dict[str, Set[str]]) -> int:
    if y in rule_orders.get(x, set()):
        return -1
    elif x in rule_orders.get(y, set()):
        return 1
    return 0

def sort_update(update: List[str], rule_orders: Dict[str, Set[str]]) -> List[str]:
    return sorted(update, key=cmp_to_key(lambda x, y: compare(x,y,rule_orders)))

def main() -> None:
    if len(sys.argv) < 2:
        print("Usage: python <script> <filepath>")
        sys.exit(1)
    # Input formatting
    filepath = sys.argv[1]
    rules, updates = open(filepath, "r").read().split("\n\n")
    rules = rules.splitlines()
    updates = [u.split(",") for u in updates.splitlines()]
    
    # Part 1
    rule_orders = defaultdict(set)
    for rule in rules:
        first, second = rule.split("|")
        rule_orders[first].add(second)
    
    check_valid = lambda x: sort_update(x, rule_orders) == x
    
    valid_updates = filter(check_valid, updates)
    print("Part 1:", sum(map(lambda x: int(x[len(x) // 2]), valid_updates)))
    
    # Part 2
    invalid_updates = list(filter(lambda x: not is_valid_update(update=x, rule_orders=rule_orders), updates))
    validated = [sort_update(update, rule_orders) for update in invalid_updates]
    print("Part 2:", sum(map(lambda x: int(x[len(x) // 2]), validated)))
    
if __name__ == "__main__":
    main()
