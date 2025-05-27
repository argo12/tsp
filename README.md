# TSP Solver

This repository contains Python and R implementations related to solving the Traveling Salesman Problem (TSP) using branch-and-bound, brute-force, and potentially other methods. The TSP is a classic combinatorial optimization problem: given a list of cities and the distances between each pair, find the shortest possible tour that visits each city exactly once and returns to the origin.

## Features

Python Implementation:
      - Branch-and-bound TSP solver (see tsp.py, node.py)
      - Brute-force search for small problem instances
      - Custom node class for constraint management and lower bound computation
      - Uses NumPy for efficient array operations

R Implementation:
      - Early-stage port or experimentation (see tsp.R)

## Project Structure


    .
    ├── node.py         # Node class for state representation and constraint logic
    ├── tsp.py          # Main TSP solver logic (branch-and-bound, brute force)
    ├── tsp.R           # R prototype/port (not fully functional)
    ├── tsp.zip         # Zipped source files
    ├── trs2.zip        # Additional zipped resources


## Getting Started
### Prerequisites

    - Python 3.x
    - numpy

### Usage

**Example (Python):**

    from tsp import TSP
    # Define distances as a 2D list or numpy array
    distances = [
        [0, 141, 118, ...],  # fill in actual distances
        [141, 0, ...],
        ...
    ]
    tsp = TSP(len(distances), distances)
    tsp.find_solution()
    
### R Version

The R code appears to be an early-stage prototype and may require adaptation for practical use.

### Motivation

This repository was created to explore and experiment with different approaches to the TSP, particularly focusing on constraint propagation and lower bound calculation to prune the search space efficiently.
If you are revisiting this project, reviewing tsp.py and node.py is a good starting point to understand the core logic.


### References

    Traveling Salesman Problem - Wikipedia
    Branch and Bound - Wikipedia

### License

MIT
