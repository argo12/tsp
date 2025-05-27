import math
import copy


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
            while included_edges < 2:
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
                    if t >= self.size:
                        edge_cost_sum = math.inf
                        break
                break
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
