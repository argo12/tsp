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
    ├── tsp.py          # Main TSP solver logic (branch-and-bound, brute force)
    ├── tsp.R           # R prototype/port (not fully functional)

## Getting Started
### Prerequisites

    - Python 3.x
    - numpy

### Usage

**Example (Python):**

      from tsp import TSP
      # Define the distance matrix between cities (0 means same city)
      distances = [
          [0, 29, 20, 21],
          [29, 0, 15, 17],
          [20, 15, 0, 28],
          [21, 17, 28, 0]
      ]
      
      # Create a TSP solver instance
      tsp = TSP(size=4, costs=distances)
      
      # Find and print the optimal tour and its length
      tsp.find_solution()
      
    
### R Version

The R code appears to be an early-stage prototype and may require adaptation for practical use.

### References

    Traveling Salesman Problem - Wikipedia
    Branch and Bound - Wikipedia

### License

MIT
