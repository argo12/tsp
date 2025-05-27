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
        return Node(self.size, self.costs, self.sorted_edges, self.all_sorted_edges, constraints)

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
                if child.contains_subtour() or child.lower_bound > 2 * self.best_tour:
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
        print(f"The shortest tour is: {self.best_node}")
        print(f"Length: {self.best_tour} km")
        print(f"Found in {end_time - start_time:.4f} seconds")
        print(f"Best tour time: {self.best_node_time - start_time:.4f} seconds")
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
