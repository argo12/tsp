import math
import time
import itertools
import copy
import logging

log = logging.getLogger(__name__)


class Node:
    def __init__(self, size, costs, sorted_edges, all_sorted_edges, parent_constraints, extra_constraint=None):
        self.size = size
        self.costs = costs
        self.sorted_edges = sorted_edges
        self.all_sorted_edges = all_sorted_edges
        self.extra_constraint = extra_constraint
        self.constraints = self._apply_constraints(parent_constraints)
        self.lower_bound = self._compute_lower_bound()

    def _compute_lower_bound(self):
        total_lb = 0
        for i in range(self.size):
            edge_cost_sum = 0
            included_edges = 0
            t = 0
            for j in range(self.size):
                if self.constraints[i][j] == 1:
                    edge_cost_sum += self.costs[i][j]
                    included_edges += 1
            while included_edges < 2 and t < self.size:
                j = self.sorted_edges[i][t]
                if self.constraints[i][j] == 2:
                    edge_cost_sum += self.costs[i][j]
                    included_edges += 1
                t += 1
            if included_edges < 2:
                edge_cost_sum = math.inf
            total_lb += edge_cost_sum
        return total_lb

    def _apply_constraints(self, parent_constraints):
        constraints = copy.deepcopy(parent_constraints)
        if not self.extra_constraint:
            return constraints

        i, j, val = self.extra_constraint
        constraints[i][j] = val
        constraints[j][i] = val

        for _ in range(2):
            self._remove_edges(constraints)
            self._add_edges(constraints)

        return constraints

    def _remove_edges(self, constraints):
        for i in range(self.size):
            if sum(1 for j in range(self.size) if i != j and constraints[i][j] == 1) >= 2:
                for j in range(self.size):
                    if constraints[i][j] == 2:
                        constraints[i][j] = constraints[j][i] = 0

        for i in range(self.size):
            for j in range(self.size):
                if self._forms_subtour(i, j, constraints) and constraints[i][j] == 2:
                    constraints[i][j] = constraints[j][i] = 0

    def _add_edges(self, constraints):
        for i in range(self.size):
            if sum(1 for j in range(self.size) if constraints[i][j] == 0) == self.size - 2:
                for j in range(self.size):
                    if constraints[i][j] == 2:
                        constraints[i][j] = constraints[j][i] = 1

    def _forms_subtour(self, start, next_node, constraints):
        visited = set()
        prev = start
        current = next_node
        while True:
            visited.add(prev)
            found, next_ = self._next_node(prev, current, constraints)
            if not found or current in visited:
                break
            prev, current = current, next_
        return current == start and len(visited) < self.size

    def _next_node(self, prev, current, constraints):
        for j in range(self.size):
            if constraints[current][j] == 1 and j != prev:
                return True, j
        return False, None

    def is_tour(self):
        return all(
            sum(1 for j in range(self.size) if self.constraints[i][j] == 0) == self.size - 2 and
            sum(1 for j in range(self.size) if self.constraints[i][j] == 1) == 2
            for i in range(self.size)
        )

    def contains_subtour(self):
        visited = set()
        for start in range(self.size):
            if start in visited:
                continue
            prev, current = start, self._next_node(start, start, self.constraints)[1]
            if current is None:
                continue
            cycle = []
            while current not in visited and current is not None:
                visited.add(prev)
                cycle.append(current)
                prev, current = current, self._next_node(prev, current, self.constraints)[1]
                if current == start:
                    break
            if len(cycle) < self.size and current == start:
                return True
        return False

    def tour_length(self):
        length = 0
        fr = 0
        to = self._next_node(fr, fr, self.constraints)[1]
        for _ in range(self.size):
            length += self.costs[fr][to]
            fr, to = to, self._next_node(fr, to, self.constraints)[1]
        return length

    def next_constraint(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.constraints[i][j] == 2:
                    return [i, j]
        return None

    def __str__(self):
        if not self.is_tour():
            return 'This node is not a tour'

        result = ['0']
        fr = 0
        to = next(j for j in range(self.size) if self.constraints[fr][j] == 1)
        result.append(str(to))

        for _ in range(self.size - 2):
            next_node = next(j for j in range(self.size) if self.constraints[to][j] == 1 and j != fr)
            result.append(str(next_node))
            fr, to = to, next_node

        return '-'.join(result)


class TSP:
    def __init__(self, size, costs, best_tour=math.inf):
        self.size = size
        self.costs = costs
        self.best_tour = best_tour
        self.best_node = None
        self.best_node_time = 0
        self.num_created_nodes = 0
        self.num_pruned_nodes = 0
        self.sorted_edges = self._sort_edges()
        self.all_sorted_edges = self._sort_all_edges()

    def _sort_edges(self):
        return [[x for _, x in sorted(zip(self.costs[i], range(self.size)))] for i in range(self.size)]

    def _sort_all_edges(self):
        edges = [[i, j] for i in range(self.size) for j in range(i + 1, self.size)]
        return sorted(edges, key=lambda e: self.costs[e[0]][e[1]])

    def _create_root(self):
        constraints = [[2 if i != j else 0 for j in range(self.size)] for i in range(self.size)]
        root = Node(self.size, self.costs, self.sorted_edges, self.all_sorted_edges, constraints)
        print(f"Initial root lower bound: {root.lower_bound}")
        return root

    def _branch_and_bound(self, node):
        if node.is_tour():
            length = node.tour_length()
            if length < self.best_tour:
                self.best_tour = length
                self.best_node = node
                self.best_node_time = time.perf_counter()
                print(f"Found better tour: {node} of length {length} km")
        else:
            constraint = node.next_constraint()
            if constraint is None:
                return

            left_child = Node(self.size, self.costs, self.sorted_edges, self.all_sorted_edges, node.constraints, constraint + [1])
            right_child = Node(self.size, self.costs, self.sorted_edges, self.all_sorted_edges, node.constraints, constraint + [0])
            self.num_created_nodes += 2

            if self.num_created_nodes % 401 == 0:
                print(f"Nodes created: {self.num_created_nodes}, Nodes pruned: {self.num_pruned_nodes}")
            if self.num_created_nodes % 51 == 0:
                print(".", end="", flush=True)

            for child in [left_child, right_child]:
                if child.contains_subtour() or child.lower_bound >= self.best_tour:
                    self.num_pruned_nodes += 1
                else:
                    self._branch_and_bound(child)

    def find_solution(self):
        root = self._create_root()
        self.num_created_nodes += 1
        start_time = time.perf_counter()
        self._branch_and_bound(root)
        end_time = time.perf_counter()

        print('\n------------------------------------------------')
        if self.best_node:
            print(f"The shortest tour is: {self.best_node}")
            print(f"Length: {self.best_tour} km")
            print(f"Found in {end_time - start_time:.4f} seconds")
            print(f"Best tour time: {self.best_node_time - start_time:.4f} seconds")
        else:
            print("No tour found.")

        print(f"Nodes created: {self.num_created_nodes}")
        print(f"Nodes pruned: {self.num_pruned_nodes}")


def brute_force(n, distances):
    min_length = math.inf
    min_tour = []
    for tour in itertools.permutations(range(1, n)):
        length = distances[0][tour[0]] + sum(distances[tour[i]][tour[i + 1]] for i in range(n - 2)) + distances[tour[-1]][0]
        if length < min_length:
            min_length = length
            min_tour = tour
    min_tour = (0,) + min_tour + (0,)
    print(f"Shortest tour is: {min_tour}")
    print(f"It has a length of: {min_length} km")
    return min_length


if __name__ == "__main__":
    # Example usage:
    costs = [
        [0, 29, 20, 21],
        [29, 0, 15, 17],
        [20, 15, 0, 28],
        [21, 17, 28, 0]
    ]

    size = len(costs)
    initial_best = brute_force(size, costs)
    print("\nRunning Branch and Bound:")
    tsp = TSP(size, costs, best_tour=initial_best)
    tsp.find_solution()
