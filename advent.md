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
    display_name: Python 3
    language: python
    name: python3
---

```python
import numpy as np
import pandas as pd
import re
```

## Day 1

```python
(np.loadtxt("input1.txt", dtype=int) // 3 - 2).sum()
```

```python
# (x + fuel) / 3 - 2 = fuel
```

```python
mass = np.loadtxt("input1.txt", dtype=int)
fuel = [mass // 3 - 2]
while True:
    fuel.append(np.clip(fuel[-1] // 3 - 2, 0, None))
    if fuel[-1].max() == 0:
        break
np.sum(fuel)
```

## Day 2

```python
def calc(noun, verb):
    with open("input2.txt") as f:
        l = list(map(int, f.read().split(",")))
    l[1] = noun
    l[2] = verb
    for idx in range(0, len(l), 4):
        code, x,  y, loc = l[idx:idx + 4]
        if code == 1:
            l[loc] = l[x] + l[y]
        elif code == 2:
            l[loc] = l[x] * l[y]
        elif code == 99:
            break
    return l[0]
```

```python
with open("input2.txt") as f:
    l = list(map(int, f.read().split(",")))
for x in range(len(l)):
    for y in range(len(l)):
        if calc(x,  y) == 19690720:
            print(100 * x + y)
            break
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

def get_pos(p):
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
print(min(abs(x) + abs(y) for x, y in s1 & s2))
```

```python
def get_pos_dict(p):
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
    

print(sum(good(i) for i in range(382345, 843167 + 1)))
print(sum(good(i, part2=True) for i in range(382345, 843167 + 1)))
```
