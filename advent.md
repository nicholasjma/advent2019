---
jupyter:
  jupytext:
    formats: ipynb,md
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.2'
      jupytext_version: 1.6.0
  kernelspec:
    display_name: Python [conda env:py38]
    language: python
    name: conda-env-py38-py
---

```python
import numpy as np
import pandas as pd
import re
from collections import defaultdict, Counter
from copy import deepcopy
from itertools import permutations, cycle
from math import inf
```

## Day 1

```python
(np.loadtxt("input1.txt", dtype=int) // 3 - 2).sum()
```

```python
mass = np.loadtxt("input1.txt", dtype=int)
fuel = [mass // 3 - 2]
while True:
    # keep adding fuel needed to haul the fuel until nothing is added
    fuel.append(np.clip(fuel[-1] // 3 - 2, 0, None))
    if fuel[-1].max() == 0:
        break
np.sum(fuel)
```

## Day 2


Note that on Day 5 I write an class-based IntCode implementation to better support additional features. This is a really minimal IntCode that became difficult to upgrade when modes were introduced on Day 5.

```python
def calc(noun, verb, input="input2.txt"):
    with open(input) as f:
        l = list(map(int, f.read().split(",")))
    l[1] = noun
    l[2] = verb
    for idx in range(0, len(l), 4):
        code, x, y, loc = l[idx : idx + 4]
        if code == 1:
            l[loc] = l[x] + l[y]
        elif code == 2:
            l[loc] = l[x] * l[y]
        elif code == 99:
            break
    return l[0]
```

```python
calc(12, 2)
```

We can use the full IntCode for this day too

```python
# with open("input2.txt") as f:
#     l = list(map(int, f.read().split(",")))
# l[1], l[2] = 12, 2
# ic = IntCode(l)
# ic.run_all()
# ic[0]
```

```python
with open("input2.txt") as f:
    n = len(f.read().split(","))
try:
    for x in range(n):
        for y in range(n):
            if calc(x, y) == 19690720:
                print(100 * x + y)
                raise AssertionError
except AssertionError:
    pass
```

Note that because of support for additional features, this is half as fast

```python
# try:
#     for x in range(n):
#         for y in range(n):
#             ic = IntCode("input2.txt")
#             ic[1], ic[2] = x, y
#             ic.run_all()
#             if ic[0] == 19690720:
#                 print(100 * x + y)
#                 raise AssertionError
# except AssertionError:
#     pass
```

## Day 3

```python
with open("input3.txt") as f:
    p1, p2 = f.read().splitlines()
    p1, p2 = p1.split(","), p2.split(",")

p1 = [(x[0], int(x[1:])) for x in p1]
p2 = [(x[0], int(x[1:])) for x in p2]

DIRS = {
    "R": (1, 0),
    "L": (-1, 0),
    "U": (0, 1),
    "D": (0, -1),
}
```

```python
def get_pos(p):
    """Return set of points visited"""
    s = set()
    cur = (0, 0)
    for direction, dist in p:
        y = DIRS[direction]
        for _ in range(1, dist + 1):
            cur = (cur[0] + y[0], cur[1] + y[1])
            s.add(cur)
    return s


s1 = get_pos(p1)
s2 = get_pos(p2)
min(abs(x) + abs(y) for x, y in s1 & s2)
```

```python
def get_pos_dict(p):
    """Return dict with points visited as keys and earliest times visited as values"""
    s = {}
    cur = (0, 0)
    steps = 0
    for direction, dist in p:
        y = DIRS[direction]
        for _ in range(1, dist + 1):
            cur = (cur[0] + y[0], cur[1] + y[1])
            steps += 1
            if cur not in s:
                s[cur] = steps
    return s


d1 = get_pos_dict(p1)
d2 = get_pos_dict(p2)
min(d1[k] + d2[k] for k in set(d1) & set(d2))
```

## Day 4

```python
def good(n, part2=False):
    s = str(n)
    doub = False
    for m in re.finditer(r"(\d)\1+", s):
        if not part2 or m.span()[1] - m.span()[0] == 2:
            doub = True
            break
    if not doub:
        return False
    digits = list(map(int, s))
    return all(x <= y for x, y in zip(digits, digits[1:]))
```

```python
sum(good(i) for i in range(382345, 843167 + 1))
```

```python
sum(good(i, part2=True) for i in range(382345, 843167 + 1))
```

## Day 5


Note that this `IntCode` implementation includes additional features from subsequent days. See intcode.py for the implementation.

```python code_folding=[0]
from intcode import IntCode
```

```python code_folding=[0]
ic = IntCode("input5.txt", [1], verbose=False)
ic.run_all()
```

```python
ic = IntCode("input5.txt", [5], verbose=False)
ic.run_all()
```

## Day 6

```python
with open("input6.txt") as f:
    orbits = [tuple(x.split(")")) for x in f.read().splitlines()]
direct = defaultdict(set)
for x, y in orbits:
    direct[y].add(x)


def compute_indirect(direct):
    """Compute indirect orbits"""
    prev, indirect = deepcopy(direct), deepcopy(direct)
    while True:
        for orbited, orbits in prev.items():
            if not orbits:
                continue
            # add all indirect orbits found to indirect
            indirect[orbited] |= set.union(*(indirect[x] for x in orbits))
        # keep looping until we didn't add anything
        if indirect == prev:
            return indirect
        else:
            prev = deepcopy(indirect)


indirect = compute_indirect(direct)
sum(map(len, indirect.values()))
```

```python
with open("input6.txt") as f:
    orbits = [tuple(x.split(")")) for x in f.read().splitlines()]
graph = defaultdict(set)
# create adjacency dict
for x, y in orbits:
    graph[y].add(x)
    graph[x].add(y)


def min_dist(graph, source, dest):
    """Use Djikstra's algorithm to find the min distance from source to dest"""
    dists = defaultdict(lambda: inf)
    dists[source] = 0
    unvisited = set(graph.keys())
    while True:
        cur = min(unvisited, key=lambda x: dists[x])
        d = dists[cur]
        if d == dists[dest]:
            break
        unvisited.remove(cur)
        for neighbor in graph[cur]:
            dists[neighbor] = dists[cur] + 1
    return dists[dest]


min_dist(graph, "YOU", "SAN") - 2
```

## Day 7

```python
def amp(data):
    """Part 1"""
    best = 0
    for phases in permutations(range(5)):
        signal = 0
        for phase in phases:
            amp = IntCode(data, input=[phase, signal])
            signal = amp.run_all()[0]
        best = max(best, signal)
    return best
```

```python
amp("input7.txt")
```

```python
def feedback(data, verbose=False):
    """Part 2"""
    best = 0
    for phases in permutations(range(5, 10)):
        signal = 0
        # initialize amps with proper phases
        amps = [IntCode(data, input=[phase], verbose=False) for phase in phases]
        for amp in cycle(amps):
            # push previous signal as input
            amp.push_input(signal)
            # run until either waiting for input or halted
            amp.run_all()
            # update current signal
            signal = amp.pop_output()
            # stop amplifying if the last amp halted
            if amp.halt and amp is amps[-1]:
                best = max(best, signal)
                if verbose:
                    print(f"Permutation {phases} signal {signal} best {best}")
                break
    return best


feedback("input7.txt", verbose=False)
```

## Day 8

```python
with open("input8.txt") as f:
    s = f.read()[:-1]  # strip the terminal newline
WIDTH = 25
HEIGHT = 6
imgs = [s[idx : idx + WIDTH * HEIGHT] for idx in range(0, len(s), WIDTH * HEIGHT)]
```

```python
counts = [Counter(x) for x in imgs]
img = min(counts, key=lambda x: x["0"])
img["1"] * img["2"]
```

```python
def first_pixel(l):
    """outputs the first entry that isn't 2"""
    for c in l:
        if c != "2":
            return c


def print_img(img, lpad=2, rpad=1, tpad=1, bpad=1, white=" ", black=None, padcolor=0):
    if black is None:
        black = bytes((219,)).decode("cp437")  # a black block character
    PAD = black if padcolor == 0 else wheite
    # print top padding
    for _ in range(tpad):
        print(PAD * (WIDTH + lpad + rpad))
    # print each row with left and right padding added
    for idx in range(0, WIDTH * HEIGHT, WIDTH):
        print(
            PAD * lpad
            + "".join(img[idx : idx + WIDTH]).replace("1", white).replace("0", black)
            + PAD * rpad
        )
    # print bottom padding
    for _ in range(bpad):
        print(PAD * (WIDTH + lpad + rpad))
```

```python
print_img([first_pixel(x[idx] for x in imgs) for idx in range(WIDTH * HEIGHT)])
```

## Day 9

```python
IntCode("input9.txt", input=[1], verbose=False).run_all()
```

```python
IntCode("input9.txt", input=[2], verbose=False).run_all()
```
