### Advent of Code 2024
<img src="https://github.com/user-attachments/assets/125e07c1-5061-4e80-8f62-e93a41c2c95a" width=200 height=200 />

> Solutions and brief explanations for [Advent of Code 2024](https://adventofcode.com/2024)
#### Day 1
Day 1's problem was solved nicely by parsing the input into two lists of integers. For this I made use of the `zip` functionality to pair and split corresponding numbers from each list.

Part 1 asks to pair up the correspondingly ranked numbers from each list (i.e., the smallest number on the left paired with the smallest number on the right) from an input like the following:
```
3   4
4   3
2   5
1   3
3   9
3   3
```
It is then trivial to sort and compare corresponding elements from each list, making use of some functional syntax in Python: `sum(map(lambda x: abs(x[0] - x[1]), zip(sorted(left), sorted(right))))`. Here we sort each list to match up corresponding pairs, and then sum the distance (difference) of each pair.

Part 2 was similarly straightforward, this time asking for a `similarity score` by counting how many times each number in the left list appears in the right, which could be solved succintly with Python's support for list comprehensions: `sum([l * (l==r) for r in right for l in left])`.
