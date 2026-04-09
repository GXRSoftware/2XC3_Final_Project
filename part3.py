##########
# Week 3 #
##########

###### Imports  ######
import math as math
import time
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from collections import defaultdict
from part1 import DirectedWeightedGraph, dijkstra, create_random_complete_graph
from part2 import a_star
######################

###### Controls ######
w3e1 = True   
w3e2 = True   
w3e3 = True   
w3e4 = True   
w3e5 = True   
######################

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

            # Use time for the edge weights
            time = edge.time 

            # Add both edges
            self.add_edge(stat1, stat2, time)
            self.add_edge(stat2, stat1, time)

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

SG = StarGraph()
SG.loadStations('london_stations.csv', 'london_connections.csv')

####################
# Helper Functions # 
####################

# This is just used to reconstruct a path from Dijkstra's
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

# Line Lookups
def build_line_lookup(edges_df):
    line_lookup = {}
    for row in edges_df.itertuples():
        line_lookup[(row.station1, row.station2)] = row.line
        line_lookup[(row.station2, row.station1)] = row.line
    return line_lookup

# Counts the number of transfers
def count_transfers(path, line_lookup):
    if path is None or len(path) < 2:
        return 0
    transfers = 0
    current_line = line_lookup.get((path[0], path[1]))
    for i in range(1, len(path) - 1):
        next_line = line_lookup.get((path[i], path[i+1]))
        if next_line != current_line:
            transfers += 1
            current_line = next_line
    return transfers

# Counts the lines used
def count_lines_used(path, line_lookup):
    if path is None or len(path) < 2:
        return 0
    lines = {line_lookup.get((path[i], path[i+1])) for i in range(len(path)-1)}
    lines.discard(None)
    return len(lines)

##########################
#      Data Setup        #
# For measuring in tests #
##########################
edges_df    = pd.read_csv('london_connections.csv')
line_lookup = build_line_lookup(edges_df)
stations    = list(SG.adj.keys())
 
print("Pre-building Dijkstra distance tables...")
full_dist = {}
for s in stations:
    full_dist[s] = dijkstra(SG, s)
 
print("Timing both algorithms per pair...")
records = []
total = len(stations) * (len(stations) - 1)
done  = 0
 
for s in stations:
    for d in stations:
        if s == d:
            continue
 
        t0 = time.perf_counter()
        dijkstra(SG, s)
        dijkstra_time = time.perf_counter() - t0
 
        SG.createHeuristic(d)
        t0 = time.perf_counter()
        _, path_str = a_star(SG, s, d, SG.h)
        astar_time = time.perf_counter() - t0
 
        path      = get_dijkstra_path(full_dist[s], SG, s, d)
        reachable = path is not None
 
        records.append({
            "dijkstra_time": dijkstra_time,
            "astar_time":    astar_time,
            "transfers":     count_transfers(path, line_lookup) if reachable else -1,
            "lines_used":    count_lines_used(path, line_lookup) if reachable else -1,
            "path_len":      len(path) if reachable else -1,
            "reachable":     reachable,
        })
 
        done += 1
        if done % 5000 == 0:
            print(f"  {done}/{total} pairs done...")
 
r = [x for x in records if x["reachable"]]
print(f"Done. Reachable pairs: {len(r)}")
 
################
# Experiment 1 #
################
# Does A* outperform Dijkstra more as the number of transfers increases?
# A good heuristic should prune more on simple same-line routes. As transfers
# increase the path becomes less geographically direct, potentially weakening
# the heuristic's guidance.
if w3e1:
    by_t = defaultdict(lambda: {"d": [], "a": []})
    for x in r:
        by_t[x["transfers"]]["d"].append(x["dijkstra_time"])
        by_t[x["transfers"]]["a"].append(x["astar_time"])
 
    labels = sorted(by_t.keys())
    avg_d  = [np.mean(by_t[t]["d"]) for t in labels]
    avg_a  = [np.mean(by_t[t]["a"]) for t in labels]
 
    plt.plot(labels, avg_d, color="blue",   label="Dijkstra")
    plt.plot(labels, avg_a, color="orange", label="A*")
    plt.title("Experiment 1 — Avg Runtime vs Number of Transfers")
    plt.xlabel("Number of Transfers")
    plt.ylabel("Average Time (s)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("exp1_runtime_vs_transfers.png")
    plt.clf()
    print("Saved: exp1_runtime_vs_transfers.png")
 
 
################
# Experiment 2 #
################
# Does A*'s advantage grow or shrink as paths get longer?
# On short paths both algorithms terminate quickly. On longer paths A* has
# more opportunity to skip nodes, but the heuristic may also become less
# reliable as the path winds across the network.
if w3e2:
    by_len = defaultdict(lambda: {"d": [], "a": []})
    for x in r:
        by_len[x["path_len"]]["d"].append(x["dijkstra_time"])
        by_len[x["path_len"]]["a"].append(x["astar_time"])
 
    lens  = sorted(by_len.keys())
    avg_d = [np.mean(by_len[l]["d"]) for l in lens]
    avg_a = [np.mean(by_len[l]["a"]) for l in lens]
 
    plt.plot(lens, avg_d, color="blue",   label="Dijkstra")
    plt.plot(lens, avg_a, color="orange", label="A*")
    plt.title("Experiment 2 — Avg Runtime vs Path Length")
    plt.xlabel("Path Length (Hops)")
    plt.ylabel("Average Time (s)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("exp2_runtime_vs_pathlength.png")
    plt.clf()
    print("Saved: exp2_runtime_vs_pathlength.png")
 
 
################
# Experiment 3 #
################
# Does the number of distinct tube lines used affect which algorithm wins?
# Same-line routes (1 line) are geographically linear so the heuristic
# should guide A* well. Routes crossing many lines are less predictable.
if w3e3:
    by_lines = defaultdict(lambda: {"d": [], "a": []})
    for x in r:
        by_lines[x["lines_used"]]["d"].append(x["dijkstra_time"])
        by_lines[x["lines_used"]]["a"].append(x["astar_time"])
 
    labels = sorted(by_lines.keys())
    avg_d  = [np.mean(by_lines[l]["d"]) for l in labels]
    avg_a  = [np.mean(by_lines[l]["a"]) for l in labels]
 
    plt.plot(labels, avg_d, color="blue",   label="Dijkstra")
    plt.plot(labels, avg_a, color="orange", label="A*")
    plt.title("Experiment 3 — Avg Runtime vs Number of Lines Used")
    plt.xlabel("Number of Tube Lines Used")
    plt.ylabel("Average Time (s)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("exp3_runtime_vs_lines.png")
    plt.clf()
    print("Saved: exp3_runtime_vs_lines.png")

################
# Experiment 4 #
################
# How does A*'s time advantage change as the number of transfers increases?
# Plots a single line: (Dijkstra - A*) time per transfer count.
# Where the line is above 0 A* wins; below 0 Dijkstra wins.
# This directly answers "when does A* outperform Dijkstra and when does
# Dijkstra outperform A*" in one readable chart.
if w3e4:
    by_t = defaultdict(list)
    for x in r:
        by_t[x["transfers"]].append(x["dijkstra_time"] - x["astar_time"])
 
    labels    = sorted(by_t.keys())
    advantage = [np.mean(by_t[t]) for t in labels]
 
    plt.plot(labels, advantage, color="blue", label="Dijkstra - A* Time")
    plt.axhline(0, color="red", linestyle="--", linewidth=1, label="No difference")
    plt.title("Experiment 4 — A* Advantage vs Number of Transfers\n(above 0 = A* faster, below 0 = Dijkstra faster)")
    plt.xlabel("Number of Transfers")
    plt.ylabel("Avg (Dijkstra - A*) Time (s)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("exp4_advantage_vs_transfers.png")
    plt.clf()
    print("Saved: exp4_advantage_vs_transfers.png")
 
################
# Experiment 5 #
################
# How does A*'s advantage change as the number of lines used increases?
# Similar to experiment 4 but split by lines rather than transfers.
# A path using only 1 line is geographically direct so the heuristic
# should work best there. As more lines are used the path meanders more
# and the straight-line heuristic becomes a weaker guide.
if w3e5:
    by_lines = defaultdict(list)
    for x in r:
        by_lines[x["lines_used"]].append(x["dijkstra_time"] - x["astar_time"])
 
    labels    = sorted(by_lines.keys())
    advantage = [np.mean(by_lines[l]) for l in labels]
 
    plt.plot(labels, advantage, color="blue", label="Dijkstra - A* Time")
    plt.axhline(0, color="red", linestyle="--", linewidth=1, label="No difference")
    plt.title("Experiment 5 — A* Advantage vs Number of Lines Used\n(above 0 = A* faster, below 0 = Dijkstra faster)")
    plt.xlabel("Number of Tube Lines Used")
    plt.ylabel("Avg (Dijkstra - A*) Time (s)")
    plt.legend()
    plt.tight_layout()
    plt.savefig("exp5_advantage_vs_lines.png")
    plt.clf()
    print("Saved: exp5_advantage_vs_lines.png")
 
