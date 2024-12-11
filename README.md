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
#### Day 11
The general problem for Day 11 was to expand a list of numbers based on a few rules. This could lead to either increasing the number or splitting the number into two new numbers. From the problem statement:
> As you observe them for a while, you find that the stones have a consistent behavior. Every time you blink, the stones each simultaneously change according to the first applicable rule in this list:
> - If the stone is engraved with the number 0, it is replaced by a stone engraved with the number 1.
> - If the stone is engraved with a number that has an even number of digits, it is replaced by two stones. The left half of the digits are engraved on the new left stone, and the right half of the digits are engraved on the new right stone. (The new numbers don't keep extra leading zeroes: 1000 would become stones 10 and 0.)
> - If none of the other rules apply, the stone is replaced by a new stone; the old stone's number multiplied by 2024 is engraved on the new stone.
>  No matter how the stones change, their order is preserved, and they stay on their perfectly straight line.

The naive approach I took for part 1 just applies the above rules in a straightforward manner: we iterate over of list of "stones" and perform one of the three above transformations. This worked well enough for this part as it ran only for 25 iterations. However, part 2 needed to run for 3x as long which presented some performance issues, especially since I was repeatedly inserting digits into the list every time a number needed to be split. This was done to preserve the ordering as mentioned in the question, however it became apparent that this isn't actually necessary: in the end, we only care about the _resulting length_ of the final list after it has been expanded X number of times. That frees us from having to do expensive insertion operations. Therefore we could expand each "stone" or number individually rather than repeatedly iterating over the list. A recursive solution proved nice for this to repeatedly expand a number until we reach the desired iteration depth. 

As with all recursive solutions, we need a base case to determine when we should exit the recursive loop. In this case, once we have determined that no more iterations need to be done (by decreasing the count each call), we can return the length of our current expansion. In this way, for each number we could sum up its expansion at each iteration, going down the recursive tree until we hit `iteration 0`, and then working our way back up, summing as we go:
![image](https://github.com/user-attachments/assets/497b5fc8-c321-46be-b909-b0f9c0bba0c1)

```
memo: Dict[Tuple[int, int], int] = dict()
def solve(stone: int, iterations: int) -> int:    
    if (stone, iterations) in memo:
        return memo[stone, iterations]
    
    products = apply_rules(stone)
    if iterations == 0:
        return len(products)
    
    result = sum(solve(st, iterations - 1) for st in products)
    memo[stone, iterations] = result
    return result
```
To save on some computation, I also added memoization, which basically means saving computations as we go (in this case the resulting sum from expanding a given number for n iterations), so that we can quickly return a previously-computed result if we have already seen the computation before. In this case I used a simple global dictionary to store this, but Python does provde some nice function decorators like `@cache` which would do provide memoization automatically.
