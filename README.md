# A Star Grid Path and Puzzle Solver
A Python implementation of the sliding puzzle game with AI solvers using IDDFS and A* algorithms.
## Features
A star, iterative deepening dfs, dijkstra, Heuristic

## Quick Intro
The A* implementation for puzzle solver uses Manhattan distance as a heuristic:
* Heuristic: Sum of Manhattan distances of each square from its goal position
* Data Structure: Priority queue (min heap) based on f(n) = g(n) + h(n)

The grid navigation solver finds paths through a 2D grid uses Euclidean distance as a heuristic:

* Movement: 8-directional (orthogonal and diagonal)


## How to run
For 3 x 3 square_puzzle:
```
 python3 square_puzzle_gui.py 3 3 
```

For grid path:
```
python3 grid_navigation_gui.py scene_path/<file name>
```

## Visualization
![grid](graph/%E6%88%AA%E5%B1%8F2025-03-17%20%E4%B8%8A%E5%8D%882.14.23.png)
*This is simple version of A star grid path*
![path](graph/%E6%88%AA%E5%B1%8F2025-03-17%20%E4%B8%8A%E5%8D%882.15.23.png)
*This is hard version of A star grid path*
![Puzzle](graph/%E6%88%AA%E5%B1%8F2025-03-17%20%E4%B8%8A%E5%8D%882.13.00.png)
*This is start page of puzzle solver*
![puzzle](graph/%E6%88%AA%E5%B1%8F2025-03-17%20%E4%B8%8A%E5%8D%882.13.11.png)
*This is end window of puzzle solve after applying A star*