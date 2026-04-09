
from abc import (ABC, abstractmethod)
from part1 import (dijkstra, bellman_ford)
from part2 import a_star


class Graph:

    def __init__(self):
        self.graph = {} # represent the graph using adjacency list

    def get_adj_nodes(self, node):
        """
        Returns the edges of 'node'
        """
        return self.graph[node]

    def add_node(self, node):
        """
        Adds 'node' to the graph
        """
        self.graph[node] = []

    def add_edge(self, start, end, w):
        """
        Adds the edge (w, end) to the node 'start'
        """
        if start not in self.graph or end not in self.graph:
            # raise an exception if start/end is not in the graph
            raise Exception("The start/end node is not in the graph")

        self.graph[start].append((w, end))

    def get_num_of_nodes(self):
        """
        Gets the total number of nodes in the graph
        """
        total_num_of_nodes = 0

        for node in graph:
            total_num_of_nodes += 1

        return total_num_of_nodes

    def w(node):
        #TODO
        pass


class WeightedGraph(Graph):

    def w(nod1, node2):
        #TODO
        pass


class HeuristicGraph(WeightedGraph):

    def __init__(self, heuristic):
        self._heuristic = heuristic

    def get_heuristic(self):
        return self._heuristic


class SPAlgorithm(ABC):
    """
    This is an abstract class for calculating the
    shortest path
    """

    @abstractmethod
    def calc_sp(self, graph, source, dest):
        """
        An abstract method that calc the shortest path
        from source to dest
        """
        pass


class Dijkstra(SPAlgorithm):

    def calc_sp(self, graph, source, dest):
        distances = dijkstra(graph, source)
        return distances[dest]


class Bellman_Ford(SPAlgorithm):
    
    def calc_sp(self, graph, source, dest):
        distances = bellman_ford(graph, source)
        return distances[dest]


class A_Start(SPAlgorithm):

    def calc_sp(self, graph, source, dest):
        h = graph.get_heuristic()
        (_, s_path) = a_star(graph, source, dest, h)

        if s_path is None:
            return float("inf") # float("inf") is one way to represent positive infinity in python

        # get all the nodes of the shortest path from source to dest
        nodes = [int(node) for node in s_path.split(" -> ")] 
        
        dist = 0
        # calc the total distance
        for i in range(len(nodes) - 1):
            dist += graph.w(nodes[i], nodes[i + 1])
        
        return dist


class ShortPathFinder:

    def __init__(self):
        #based on the UML diagram
        # We think you should always
        # set the graph and algorithm
        # by using the set_graph and set_algorithm
        # functions
        self.graph = None
        self.algorithm = None

    def set_graph(self, graph):
        """
        Sets the graph
        """
        self.graph = graph

    def set_algorithm(self, algorithm):
        """
        Sets the algorithm
        """
        self.algorithm = algorithm

    def calc_short_path(self, source, dest):
        """
        Calcs the total distance of the shortest path from 'source'
        to 'dest'
        """
        return self.algorithm.calc_sp(self.graph, source, dest)

