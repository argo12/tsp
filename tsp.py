from node import Node
import math
import time
import copy
import numpy as np


class TSP(object):
    """
    >>> distances = [[0,141,118,171,126,69,158], [141,0,226,34,212,208,82], [118,226,0,232,56,107,194], [171,34,232,0,200,233,63], [126,212,56,200,0,105,145], [69,208,107,233,105,0,212], [158,82,194,63,145,212,0]]
    >>> T = TSP(7,distances)
    >>> T.findSolution()

    """

    constraints = None

    def __init__(self, size, costs, bestTour=math.inf):
        self.size = size
        self.costs = costs
        self.bestTour = bestTour
        self.bestNode = None
        self.bestNodeTime = 0
        self.num_createdNodes = 0
        self.num_prunedNodes = 0
        self.sortedEdges = self.sort_edges()
        self.allSortedEdges = self.sort_all_edges()

    def find_solution(self):
        root = self.create_root()
        self.num_createdNodes += 1
        T1 = time.perf_counter()

        self.branch_and_bound(root)
        T2 = time.perf_counter()

        print('------------------------------------------------')
        print("The shortest tour is:", self.bestNode)
        print("It has a length of", self.bestTour, "km")
        print("Found in", T2 - T1, "seconds")
        print("Best tour was found after:", self.bestNodeTime, "seconds")
        print("Number of  nodes created:", self.num_createdNodes)
        print("Number of nodes pruned:", self.num_prunedNodes)

    def sort_edges(self):
        result = []
        for i in range(self.size):
            result.append([x for (y, x) in sorted(zip(self.costs[i], list(range(self.size))))])

        return result

    def sort_all_edges(self):
        edges = []
        lengths = []
        for i in range(self.size):
            for j in range(i + 1, self.size):

                edges.append([i, j])
                lengths.append([i, j])

        res = [z for (l, z) in sorted(zip(lengths, edges))]
        #print(res)
        return res

    def create_root(self):
        no_constraints = []
        for i in range(self.size):
            row_i = []
            for j in range(self.size):
                if i != j:
                    row_i.append(2)
                else:
                    row_i.append(0)
            no_constraints.append(row_i)
        node = Node(self.size, self.costs, self.sortedEdges, self.allSortedEdges, no_constraints)
        return node

    def branch_and_bound(self, node):
        """

        :param node:
        :return:
        """
        if node.isTour():
            if node.tourLength() < self.bestTour:
                self.bestTour = node.tourLength()
                self.bestNode = node
                self.bestNodeTime = time.perf_counter()
                print("Found better tour:", self.bestNode, "of  length ", self.bestTour, "km")
        else:
            new_constraint = copy.copy(node.next_constraint())
            new_constraint.append(1)

            leftChild = Node(self.size, self.costs, self.sortedEdges, self.allSortedEdges, node.constraints, new_constraint)

            new_constraint[2] = 0
            rightChild = Node(self.size, self.costs, self.sortedEdges, self.allSortedEdges, node.constraints, new_constraint)
            self.num_createdNodes += 2

            if self.num_createdNodes % 401 == 0:
                print("Number of nodes created so far:", self.num_createdNodes)
                print("Number of nodes pruned so far:", self.num_prunedNodes)

            if self.num_createdNodes % 51 == 0:
                print(".")

            if leftChild.contains_subtour() or leftChild.lowerBound > 2 * self.bestTour:
                leftChild = None
                self.num_prunedNodes += 1

            if rightChild.contains_subtour() or rightChild.lowerBound > 2 * self.bestTour:
                rightChild = None
                self.num_prunedNodes += 1

            if leftChild != None and rightChild == None:
                self.branch_and_bound(leftChild)

            elif leftChild == None and rightChild != None:
                self.branch_and_bound(rightChild)

            elif leftChild != None and rightChild != None:
                if leftChild.lowerBound <= rightChild.lowerBound:
                    if leftChild.lowerBound < 2 * self.bestTour:
                        self.branch_and_bound(leftChild)
                    else:
                        leftChild = None
                        self.num_prunedNodes += 1

                    if rightChild.lowerBound < 2 * self.bestTour:
                        self.branch_and_bound(rightChild)
                    else:
                        rightChild = None
                        self.num_prunedNodes += 1

            else:
                if rightChild.lowerBound < 2 * self.bestTour:
                    self.branch_and_bound(rightChild)
                else:
                    rightChild = None
                    self.num_prunedNodes += 1
                if leftChild.lowerBound < 2 * self.bestTour:
                    self.branch_and_bound(leftChild)
                else:
                    leftChild = None
                    self.num_prunedNodes += 1

    def next_constraint(self):
        for edge in self.allSortedEdges:
            i = edge[0]
            j = edge[1]
            if self.constraints[i][j] == 2:
                return edge
        # return []

    def computeLowerBound2(self):
        lb = 0
        onetree = np.zeros((self.size, self.size), np.int8)
        t = 0
        for i in range(1, self.size):
            for j in range(i + 1, self.size):
                if self.constraints[i][j] == 1:
                    onetree[i][j] = 1
                    onetree[j][i] = 1
                    t += 1
                    lb += self.costs[i][j]
        for edge in self.allSortedEdges:
            if t >= self.size - 1:
                break
            i = edge[0]
            j = edge[1]
            if (self.constraints[i][j] == 2) and (i != 0):
                onetree[i][j] = 1
                onetree[j][i] = 1

            # need to clarify what is this
            if self.onetree_contains_cycle( onetree ):
                onetree[i][j] = 0
                onetree[j][i] = 0
            else:
                t += 1
                lb += self.costs[i][j]

        t = 0
        for j in range(self.size):
            if self.constraints[0][j] == 1:
                onetree[0][j] = 1
                onetree[j][0] = 1
                lb += self.costs[0][j]
                t += 1
        tt = 0

        while t < 2:
            shortest = self.sortedEdges[0][tt]
            if self.constraints[0][shortest] == 2:
                onetree[0][shortest] = 1
                onetree[shortest][0] = 1
                lb += self.costs[0][shortest]
                t += 1
            tt += 1

        return lb

def brute_force(n,distances):
    import itertools
    import math
    minLength = math.inf
    minTour = []
    for tour in itertools.permutations(list(range(1, n))):
        fr = 0
        length = 0
        count = 0
        while count < n-1:
            to = tour[count]
            length += distances[fr][to]
            fr = to
            count += 1
        length += distances[fr][0]
        if length < minLength:
            minLength = length
            minTour = tour
    minTour = (0,) + minTour + (0,)
    print("Shortest tour is:", minTour )
    print("It has a length of:", minLength, "km")
