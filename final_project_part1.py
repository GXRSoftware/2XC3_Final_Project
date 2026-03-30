import min_heap
import random

testAStar = True
AStarEmpirical = True

class DirectedWeightedGraph:

    def __init__(self):
        self.adj = {}
        self.weights = {}

    def are_connected(self, node1, node2):
        for neighbour in self.adj[node1]:
            if neighbour == node2:
                return True
        return False

    def adjacent_nodes(self, node):
        return self.adj[node]

    def add_node(self, node):
        self.adj[node] = []

    def add_edge(self, node1, node2, weight):
        if node2 not in self.adj[node1]:
            self.adj[node1].append(node2)
        self.weights[(node1, node2)] = weight

    def w(self, node1, node2):
        if self.are_connected(node1, node2):
            return self.weights[(node1, node2)]

    def number_of_nodes(self):
        return len(self.adj)


def dijkstra(G, source):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
    Q.decrease_key(source, 0)

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour]:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node
    return dist


def bellman_ford(G, source):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    nodes = list(G.adj.keys())

    #Initialize distances
    for node in nodes:
        dist[node] = float("inf")
    dist[source] = 0

    #Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        for node in nodes:
            for neighbour in G.adj[node]:
                if dist[neighbour] > dist[node] + G.w(node, neighbour):
                    dist[neighbour] = dist[node] + G.w(node, neighbour)
                    pred[neighbour] = node
    return dist


def total_dist(dist):
    total = 0
    for key in dist.keys():
        total += dist[key]
    return total

def create_random_complete_graph(n,upper):
    G = DirectedWeightedGraph()
    for i in range(n):
        G.add_node(i)
    for i in range(n):
        for j in range(n):
            if i != j:
                G.add_edge(i,j,random.randint(1,upper))
    return G


#Assumes G represents its nodes as integers 0,1,...,(n-1)
def mystery(G):
    n = G.number_of_nodes()
    d = init_d(G)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                if d[i][j] > d[i][k] + d[k][j]: 
                    d[i][j] = d[i][k] + d[k][j]
    return d

def init_d(G):
    n = G.number_of_nodes()
    d = [[float("inf") for j in range(n)] for i in range(n)]
    for i in range(n):
        for j in range(n):
            if G.are_connected(i, j):
                d[i][j] = G.w(i, j)
        d[i][i] = 0
    return d





##########
# Week 2 #
##########
def a_star(G, s, d, h):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())
    path = {}
    visited = set()

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
        path[node] = 0
    Q.decrease_key(s, h[s])
    dist[s] = 0

    # Set a flag to check if the path is found early
    done = False

    # Search through the nodes
    while not Q.is_empty() and not done:
        # Take the minimal cost node
        current_element = Q.extract_min()

        # Check that the minimal cost node is not the target
        # Otherwise, we've found the shortest path
        if (current_element.value != d):
            # Set the current node to the popped element
            # Set the node to visited to know what we've traversed
            current_node = current_element.value
            visited.add(current_node)

            for neighbour in G.adj[current_node]:
                # If we've already traversed the node, skip
                if neighbour in visited:
                    continue

                # Set the new distances based on the neighbouring nodes
                # Add the non-traversed nodes to the priority queue
                new_g = dist[current_node] + G.w(current_node, neighbour)
                if new_g < dist[neighbour]:
                    path[neighbour] = current_node
                    Q.decrease_key(neighbour, new_g + h[neighbour])  # f = g + h in heap
                    dist[neighbour] = new_g                           # only g in dist
                    pred[neighbour] = current_node
        else: done = True
    
    # If a path is not possible
    if dist[d] == float("inf"): return (pred, None)

    # Generate the path
    short = " -> " + str(d)
    while d != s:
        d = path[d]
        short = " -> " + str(d) + short
    short = short[4:]

    # Return the predecessor dictionary and the generated path
    return (pred, short)

import matplotlib.pyplot as plt
import time
import random

##########################
# Correctness Tests      #
##########################

def test_a_star_basic():
    """Simple 4-node graph with known shortest path"""
    G = DirectedWeightedGraph()
    for i in range(4):
        G.add_node(i)
    G.add_edge(0, 1, 1)
    G.add_edge(1, 3, 2)
    G.add_edge(0, 2, 4)
    G.add_edge(2, 3, 1)

    # Admissible heuristic (manually estimated)
    h = {0: 3, 1: 2, 2: 1, 3: 0}
    pred, path = a_star(G, 0, 3, h)
    print(f"[Basic Test] Path: {path}")
    assert path == "0 -> 1 -> 3", f"Expected 0 -> 1 -> 3, got {path}"
    print("PASSED")

def test_a_star_zero_heuristic():
    """A* with h=0 everywhere should behave like Dijkstra"""
    G = create_random_complete_graph(6, 20)
    h = {node: 0 for node in G.adj.keys()}

    dijkstra_dist = dijkstra(G, 0)
    pred, path = a_star(G, 0, 5, h)

    # Extract A* g-cost from pred by retracing dist
    # Just verify the path cost matches dijkstra
    nodes_in_path = path.split(" -> ")
    total = 0
    for i in range(len(nodes_in_path) - 1):
        a, b = int(nodes_in_path[i]), int(nodes_in_path[i+1])
        total += G.w(a, b)

    assert abs(total - dijkstra_dist[5]) < 1e-9, \
        f"A* (h=0) cost {total} != Dijkstra cost {dijkstra_dist[5]}"
    print(f"[Zero Heuristic Test] Path: {path}, Cost: {total} — PASSED")

def test_a_star_unreachable():
    """Destination unreachable should return None for path"""
    G = DirectedWeightedGraph()
    for i in range(4):
        G.add_node(i)
    G.add_edge(0, 1, 5)
    G.add_edge(1, 2, 3)
    # Node 3 is isolated

    h = {0: 10, 1: 5, 2: 2, 3: 0}
    pred, path = a_star(G, 0, 3, h)
    assert path is None, f"Expected None for unreachable node, got {path}"
    print("[Unreachable Test] PASSED")

def test_a_star_single_edge():
    """Direct edge from source to destination"""
    G = DirectedWeightedGraph()
    G.add_node(0)
    G.add_node(1)
    G.add_edge(0, 1, 7)

    h = {0: 7, 1: 0}
    pred, path = a_star(G, 0, 1, h)
    assert path == "0 -> 1", f"Expected '0 -> 1', got {path}"
    print("[Single Edge Test] PASSED")

def test_a_star_matches_dijkstra_random():
    """A* with h=0 must match Dijkstra on 10 random graphs"""
    for trial in range(10):
        n = random.randint(3, 8)
        G = create_random_complete_graph(n, 50)
        source, dest = 0, n - 1
        h = {node: 0 for node in G.adj.keys()}

        dijkstra_dist = dijkstra(G, source)
        pred, path = a_star(G, source, dest, h)

        if path is None:
            assert dijkstra_dist[dest] == float("inf")
        else:
            nodes_in_path = path.split(" -> ")
            total = sum(
                G.w(int(nodes_in_path[i]), int(nodes_in_path[i+1]))
                for i in range(len(nodes_in_path) - 1)
            )
            assert abs(total - dijkstra_dist[dest]) < 1e-9, \
                f"Trial {trial}: A* cost {total} != Dijkstra {dijkstra_dist[dest]}"
    print("[Random Match Test x10] PASSED")


##########################
# Empirical Tests        #
##########################

def empirical_dijkstra_vs_astar():
    runs = 50
    graph_sizes = [10, 50, 100, 200, 500]
    max_weight = 100

    avg_time_dijkstra = []
    avg_time_astar = []

    for n in graph_sizes:
        total_d = 0
        total_a = 0

        for _ in range(runs):
            G = create_random_complete_graph(n, max_weight)
            s, d = 0, n - 1
            h = {node: 0 for node in G.adj.keys()}  # neutral heuristic

            # Time Dijkstra
            t0 = time.time()
            dijkstra(G, s)
            total_d += time.time() - t0

            # Time A*
            t0 = time.time()
            a_star(G, s, d, h)
            total_a += time.time() - t0

        avg_time_dijkstra.append(total_d / runs)
        avg_time_astar.append(total_a / runs)

    plt.plot(graph_sizes, avg_time_dijkstra, color="blue", label="Dijkstra")
    plt.plot(graph_sizes, avg_time_astar, color="orange", label="A* (h=0)")
    plt.title("Dijkstra vs A* Runtime (h=0, Complete Graphs)")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Time (s)")
    plt.legend()
    plt.savefig("Dijkstra vs AStar Time.png")
    plt.clf()


def empirical_heuristic_quality():
    """Compare A* with h=0 vs A* with random (possibly inadmissible) heuristic"""
    runs = 50
    graph_sizes = [10, 50, 100, 200, 500]
    max_weight = 100

    avg_time_h0 = []
    avg_time_hrand = []

    for n in graph_sizes:
        total_h0 = 0
        total_hr = 0

        for _ in range(runs):
            G = create_random_complete_graph(n, max_weight)
            s, d = 0, n - 1

            h_zero = {node: 0 for node in G.adj.keys()}
            h_rand = {node: random.uniform(0, max_weight) for node in G.adj.keys()}
            h_rand[d] = 0

            t0 = time.time()
            a_star(G, s, d, h_zero)
            total_h0 += time.time() - t0

            t0 = time.time()
            a_star(G, s, d, h_rand)
            total_hr += time.time() - t0

        avg_time_h0.append(total_h0 / runs)
        avg_time_hrand.append(total_hr / runs)

    plt.plot(graph_sizes, avg_time_h0, color="green", label="A* (h=0)")
    plt.plot(graph_sizes, avg_time_hrand, color="red", label="A* (h=random)")
    plt.title("A* Heuristic Quality: h=0 vs Random h")
    plt.xlabel("Number of Nodes")
    plt.ylabel("Average Time (s)")
    plt.legend()
    plt.savefig("AStar Heuristic Quality.png")
    plt.clf()
    print("Saved: astar_heuristic_quality.png")

###########
# Testing #
###########

if testAStar:
    test_a_star_basic()
    test_a_star_zero_heuristic()
    test_a_star_unreachable()
    test_a_star_single_edge()
    test_a_star_matches_dijkstra_random()

if AStarEmpirical:
    print("\n=== Empirical Tests ===")
    empirical_dijkstra_vs_astar()
    empirical_heuristic_quality()