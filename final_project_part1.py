import min_heap
import random

testAStar = False
AStarEmpirical = False

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

#####################
# Correctness Tests #
#####################

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


###################
# Empirical Tests #
###################

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
    empirical_dijkstra_vs_astar()
    empirical_heuristic_quality()

##########
# Week 3 #
##########
import pandas as pd
import math as math

class StarGraph(DirectedWeightedGraph):
    def __init__(self):
        self.adj = {}
        self.weights = {}

        # We additionally store the station data (for the heuristics)
        # And the heuristic dictionary
        self.stats = []
        self.h = {}

    def loadStations(self, file1, file2):
        # First file should contain the id, x, and y (or in this case lat and lon)
        # Second file should contain the valid edges
        # Load the stations
        self.stats = pd.read_csv(file1)
        self.stats = self.stats.set_index('id')
        self.stats = self.stats.to_dict(orient='index')

        # Add each station as a node
        for stat in self.stats:
            self.add_node(stat)
        
        # Load the connections
        edges = pd.read_csv(file2)
        for edge in edges.itertuples():
            # Take the node pairs
            stat1 = edge.station1
            stat2 = edge.station2

            # Calculate the distance
            dist = round(math.sqrt((self.stats[stat1]['longitude'] - self.stats[stat2]['longitude']) ** 2 + (self.stats[stat1]['latitude'] - self.stats[stat2]['latitude']) ** 2), 10)
            
            # We can go both ways, so add both edges
            self.add_edge(stat1, stat2, dist)
            self.add_edge(stat2, stat1, dist)

    def createHeuristic(self, goal):
        # Take the goal latitude and longitude
        # Set the heuristic to the goal to 0
        goalLat = self.stats[goal]['latitude']
        goalLon = self.stats[goal]['longitude']
        self.h[goal] = 0

        # Calculate the distance to the goal
        for stat in self.stats:
            if stat != goal:
                self.h[stat] = round(math.sqrt((self.stats[stat]['longitude'] - goalLon) ** 2 + (self.stats[stat]['latitude'] - goalLat) ** 2), 10)

# Helper for comparisons
def get_dijkstra_path(dist, G, source, dest):
    if dist[dest] == float('inf'):
        return None
    path = [dest]
    current = dest
    while current != source:
        for neighbour in G.adj[current]:
            if dist[neighbour] + G.w(neighbour, current) == dist[current]:
                path.append(neighbour)
                current = neighbour
                break
        else:
            return None  
    path.reverse()
    return path


SG = StarGraph()
SG.loadStations('london_stations.csv', 'london_connections.csv')
SG.createHeuristic(25)
testA = a_star(SG, 1, 25, SG.h)
print(testA)
testD = dijkstra(SG, 1)
print(get_dijkstra_path(testD,SG,1,25))

import time
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Count the number of transfers
def count_transfers(path, line_lookup):
    if path is None or len(path) < 2:
        return 0
    transfers = 0
    current_line = line_lookup.get((path[0], path[1]), None)
    for i in range(1, len(path) - 1):
        next_line = line_lookup.get((path[i], path[i+1]), None)
        if next_line != current_line:
            transfers += 1
            current_line = next_line
    return transfers

def build_line_lookup(edges_df):
    line_lookup = {}
    for row in edges_df.itertuples():
        line_lookup[(row.station1, row.station2)] = row.line
        line_lookup[(row.station2, row.station1)] = row.line
    return line_lookup

# Collect all data pairs
def collect_data(SG, line_lookup):
    stations = list(SG.adj.keys())
    records = []
    total = len(stations) * (len(stations) - 1)
    done = 0

    for s in stations:
        # dijkstra once per source
        t0 = time.perf_counter()
        dist_d = dijkstra(SG, s)
        dijkstra_time = time.perf_counter() - t0

        for d in stations:
            if s == d:
                continue

            # a* timed per pair
            SG.createHeuristic(d)
            t0 = time.perf_counter()
            _, path_str = a_star(SG, s, d, SG.h)
            astar_time = time.perf_counter() - t0

            # reconstruct path from dist for transfer counting
            path = get_dijkstra_path(dist_d, SG, s, d)
            reachable = path is not None

            transfers = count_transfers(path, line_lookup) if reachable else -1

            # check if all edges on path share the same line
            if path and len(path) >= 2:
                lines_used = set()
                for i in range(len(path) - 1):
                    ln = line_lookup.get((path[i], path[i+1]))
                    if ln:
                        lines_used.add(ln)
                same_line = len(lines_used) == 1
            else:
                same_line = False

            records.append({
                "source":        s,
                "dest":          d,
                "dijkstra_time": dijkstra_time,
                "astar_time":    astar_time,
                "transfers":     transfers,
                "reachable":     reachable,
                "same_line":     same_line,
                "path_len":      len(path) if path else -1,
            })

            done += 1
            if done % 1000 == 0:
                print(f"  {done}/{total} pairs done...")

    return records

# ═══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 1 — scatter: dijkstra vs a* time, coloured by transfers
# ═══════════════════════════════════════════════════════════════════════════════
def experiment_1(records):
    r         = [x for x in records if x["reachable"]]
    d_times   = [x["dijkstra_time"] for x in r]
    a_times   = [x["astar_time"]    for x in r]
    transfers = [x["transfers"]     for x in r]

    fig, ax = plt.subplots(figsize=(8, 6))
    sc = ax.scatter(d_times, a_times, c=transfers, cmap="viridis", alpha=0.4, s=8)
    lim = max(max(d_times), max(a_times))
    ax.plot([0, lim], [0, lim], "r--", linewidth=1, label="equal time")
    plt.colorbar(sc, ax=ax, label="Number of Transfers")
    ax.set_xlabel("Dijkstra Time (s)")
    ax.set_ylabel("A* Time (s)")
    ax.set_title("Exp 1 — Dijkstra vs A* Time per Pair\n(below red line = A* faster)")
    ax.legend()
    plt.tight_layout()
    plt.savefig("exp1_scatter.png", dpi=150)
    plt.show()
    print("Saved: exp1_scatter.png")

# ═══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 2 — grouped bar: avg runtime by number of transfers
# ═══════════════════════════════════════════════════════════════════════════════
def experiment_2(records):
    r = [x for x in records if x["reachable"]]
    by_transfer = defaultdict(list)
    for x in r:
        by_transfer[x["transfers"]].append((x["dijkstra_time"], x["astar_time"]))

    labels = sorted(by_transfer.keys())
    avg_d  = [np.mean([v[0] for v in by_transfer[t]]) for t in labels]
    avg_a  = [np.mean([v[1] for v in by_transfer[t]]) for t in labels]
    counts = [len(by_transfer[t]) for t in labels]

    x = np.arange(len(labels))
    w = 0.35
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.bar(x - w/2, avg_d, w, label="Dijkstra", color="steelblue")
    ax.bar(x + w/2, avg_a, w, label="A*",       color="orange")
    ax.set_xticks(x)
    ax.set_xticklabels([f"{t}\n(n={c})" for t, c in zip(labels, counts)], fontsize=8)
    ax.set_xlabel("Number of Transfers")
    ax.set_ylabel("Average Time (s)")
    ax.set_title("Exp 2 — Avg Runtime by Transfer Count")
    ax.legend()
    plt.tight_layout()
    plt.savefig("exp2_transfers.png", dpi=150)
    plt.show()
    print("Saved: exp2_transfers.png")

# ═══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 3 — box plots: same-line vs multi-line pairs
# ═══════════════════════════════════════════════════════════════════════════════
def experiment_3(records):
    r = [x for x in records if x["reachable"]]

    same      = [x["astar_time"] - x["dijkstra_time"] for x in r if     x["same_line"]]
    different = [x["astar_time"] - x["dijkstra_time"] for x in r if not x["same_line"]]

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.boxplot(
        [same, different],
        labels=[f"Same Line\n(n={len(same)})", f"Multi-Line\n(n={len(different)})"],
        showfliers=False
    )
    ax.axhline(0, color="red", linestyle="--", linewidth=1, label="equal (0 = same speed)")
    ax.set_ylabel("A* Time − Dijkstra Time (s)\n(negative = A* faster)")
    ax.set_title("Exp 3 — A* Advantage: Same Line vs Multi-Line Pairs")
    ax.legend()
    plt.tight_layout()
    plt.savefig("exp3_sameline.png", dpi=150)
    plt.show()
    print("Saved: exp3_sameline.png")

# ═══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 4 — scatter + trend: A* advantage vs path length
# ═══════════════════════════════════════════════════════════════════════════════
def experiment_4(records):
    r         = [x for x in records if x["reachable"]]
    path_lens = [x["path_len"]                         for x in r]
    diff      = [x["dijkstra_time"] - x["astar_time"]  for x in r]

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(path_lens, diff, alpha=0.3, s=8, color="steelblue")
    ax.axhline(0, color="red", linestyle="--", linewidth=1, label="equal")

    z  = np.polyfit(path_lens, diff, 1)
    p  = np.poly1d(z)
    xs = np.linspace(min(path_lens), max(path_lens), 200)
    ax.plot(xs, p(xs), color="darkorange", linewidth=2, label="trend")

    ax.set_xlabel("Path Length (hops)")
    ax.set_ylabel("Dijkstra − A* Time (s)\n(positive = A* faster)")
    ax.set_title("Exp 4 — A* Speed Advantage vs Path Length")
    ax.legend()
    plt.tight_layout()
    plt.savefig("exp4_pathlength.png", dpi=150)
    plt.show()
    print("Saved: exp4_pathlength.png")

# ═══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 5 — bar: average A* advantage per source station
# ═══════════════════════════════════════════════════════════════════════════════
def experiment_5(records):
    r = [x for x in records if x["reachable"]]

    by_source = defaultdict(list)
    for x in r:
        by_source[x["source"]].append(x["dijkstra_time"] - x["astar_time"])

    stations      = sorted(by_source.keys())
    avg_advantage = [np.mean(by_source[s]) for s in stations]
    colors        = ["green" if v > 0 else "red" for v in avg_advantage]

    fig, ax = plt.subplots(figsize=(14, 4))
    ax.bar(range(len(stations)), avg_advantage, color=colors, alpha=0.7)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(range(len(stations)))
    ax.set_xticklabels(stations, rotation=90, fontsize=6)
    ax.set_xlabel("Source Station ID")
    ax.set_ylabel("Avg (Dijkstra − A*) Time (s)\n(green = A* faster on average)")
    ax.set_title("Exp 5 — Average A* Advantage by Source Station")
    plt.tight_layout()
    plt.savefig("exp5_bysource.png", dpi=150)
    plt.show()
    print("Saved: exp5_bysource.png")

# ═══════════════════════════════════════════════════════════════════════════════
# EXPERIMENT 6 — are costs actually equal between dijkstra and a*?
# ═══════════════════════════════════════════════════════════════════════════════
def experiment_6(records, dist_cache, SG):
    """Sanity check: compare path costs found by each algorithm"""
    r = [x for x in records if x["reachable"]]

    mismatches = 0
    cost_diffs = []

    for x in r:
        s, d    = x["source"], x["dest"]
        d_cost  = dist_cache[(s, d)]

        SG.createHeuristic(d)
        _, path_str = a_star(SG, s, d, SG.h)
        if path_str:
            nodes     = [int(n) for n in path_str.split(" -> ")]
            a_cost    = sum(SG.w(nodes[i], nodes[i+1]) for i in range(len(nodes) - 1))
            diff      = abs(a_cost - d_cost)
            cost_diffs.append(diff)
            if diff > 1e-9:
                mismatches += 1

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.hist(cost_diffs, bins=30, color="steelblue", edgecolor="black")
    ax.set_xlabel("|A* cost − Dijkstra cost|")
    ax.set_ylabel("Number of Pairs")
    ax.set_title(f"Exp 6 — Cost Agreement Between A* and Dijkstra\n({mismatches} mismatches out of {len(cost_diffs)} pairs)")
    plt.tight_layout()
    plt.savefig("exp6_costcheck.png", dpi=150)
    plt.show()
    print(f"Saved: exp6_costcheck.png  |  Mismatches: {mismatches}")

# ── run everything ─────────────────────────────────────────────────────────────
edges_df    = pd.read_csv('london_connections.csv')
line_lookup = build_line_lookup(edges_df)

print("Collecting all-pairs data...")
records = collect_data(SG, line_lookup)

reachable_count   = sum(1 for r in records if r["reachable"])
unreachable_count = sum(1 for r in records if not r["reachable"])
print(f"\nTotal pairs: {len(records)} | Reachable: {reachable_count} | Unreachable: {unreachable_count}\n")

# cache dijkstra costs for experiment 6
print("Caching Dijkstra costs for exp 6...")
dist_cache = {}
for s in list(SG.adj.keys()):
    dist_d = dijkstra(SG, s)
    for d in SG.adj.keys():
        if s != d:
            dist_cache[(s, d)] = dist_d[d]

experiment_1(records)
experiment_2(records)
experiment_3(records)
experiment_4(records)
experiment_5(records)
experiment_6(records, dist_cache, SG)















