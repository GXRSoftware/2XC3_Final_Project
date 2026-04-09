
from abc import (ABC, abstractmethod)
from part1 import (dijkstra, bellman_ford)
from part2 import a_star


class Graph:

    def __init__(self):
        self.graph = {} # represent the graph using adjacency list
        self.adj = self.graph # we do this here because calling code might call self.adj instead of self.graph

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

    def add_edge(self, start, end, w=0):
        """
        Adds the edge from 'start' to 'end'

        Note that since this is an unweighted graph, NO
        weight should be passed to this method
        """
        if start not in self.graph or end not in self.graph:
            # raise an exception if start/end is not in the graph
            raise Exception("The start/end node is not in the graph")

        self.graph[start].append(end)

    def get_num_of_nodes(self):
        """
        Gets the total number of nodes in the graph
        """
        total_num_of_nodes = 0

        for node in self.graph:
            total_num_of_nodes += 1

        return total_num_of_nodes

    def number_of_nodes(self):
        """
        A wrapper around self.get_num_of_nodes

        Exists so that if calling code expects a graph mathod simillar to part1.py
        we have this method
        """
        return self.get_num_of_nodes()


    def w(self, node):
        """
        Gets the weight of an edge
        """
        # we raise an exception here because this graph has no weights
        raise Exception("This graph has no weigths")


class WeightedGraph(Graph):

    def __init__(self):
        super().__init__()
        self.weights = {}

    def add_edge(self, start, end, w):
        """
        Adds the edge from 'start' to 'end' and stores its wieght in self.weights
        """
        super().add_edge(start, end)
        self.weights[(start, end)] = w

    def w(self, node1, node2):
        """
        Gets the weight of the edge (node1, node2)
        """
        if node1 not in self.graph:
            raise Exception(f"{node1} is not in the graph")
        if node2 not in self.graph:
            raise Exception(f"{node2} is not in the graph")

        return self.weights[(node1, node2)]


class HeuristicGraph(WeightedGraph):

    def __init__(self, heuristic):
        super().__init__()
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


class A_Star(SPAlgorithm):

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

