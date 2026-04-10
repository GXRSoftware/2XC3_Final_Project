import min_heap
import random
import time
import matplotlib.pyplot as plt
import math

final1e1 = False
final1e2 = False
final1e3 = False
finalmystery = False
printmys = False

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



def dijkstra_approx(G, source, k):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    track = {}

    Q = min_heap.MinHeap([])
    nodes = list(G.adj.keys())

    #Initialize priority queue/heap and distances
    for node in nodes:
        Q.insert(min_heap.Element(node, float("inf")))
        dist[node] = float("inf")
        track[node] = 0
    Q.decrease_key(source, 0)

    #Meat of the algorithm
    while not Q.is_empty():
        current_element = Q.extract_min()
        current_node = current_element.value
        dist[current_node] = current_element.key
        for neighbour in G.adj[current_node]:
            if dist[current_node] + G.w(current_node, neighbour) < dist[neighbour] and track[neighbour] < k:
                Q.decrease_key(neighbour, dist[current_node] + G.w(current_node, neighbour))
                dist[neighbour] = dist[current_node] + G.w(current_node, neighbour)
                pred[neighbour] = current_node
                track[neighbour] += 1
    return dist



def bellman_ford_approx(G, source, k):
    pred = {} #Predecessor dictionary. Isn't returned, but here for your understanding
    dist = {} #Distance dictionary
    nodes = list(G.adj.keys())

    track = {}

    #Initialize distances
    for node in nodes:
        dist[node] = float("inf")
        track[node] = 0 
    dist[source] = 0

    #Meat of the algorithm
    for _ in range(G.number_of_nodes()):
        for node in nodes:
            for neighbour in G.adj[node]:
                if dist[neighbour] > dist[node] + G.w(node, neighbour) and track[neighbour] < k:
                    dist[neighbour] = dist[node] + G.w(node, neighbour)
                    pred[neighbour] = node
                    track[neighbour] += 1
    return dist

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


def create_random_graph(num_nodes, edges, flag=0):
    G = DirectedWeightedGraph()
    nodes = []

    for i in range(num_nodes):
        nodes.append(i)

    for n in nodes:
        G.add_node(n)

    count = 0

    while count < edges:
        y = random.choice(nodes)
        z = random.choice(nodes)

        if y != z and not G.are_connected(y,z):
            
            if flag == 0:
                weight = random.randint(1, 10)
            else:
                weight = random.randint(-10, 10)

            G.add_edge(y,z,weight)
            count += 1

    return G

runs = 100

if final1e1:
    values = [2**i for i in range(6)]

    djikstra_approx_time = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}
    bellman_approx_time = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}

    djikstra_approx_dist = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}
    bellman_approx_dist = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}


    for _ in range(runs):
        random_nodes = random.randint(10,100)
        random_edges = random.randint(100,min(500, random_nodes * (random_nodes - 1)))
    

        G = create_random_graph(random_nodes, random_edges,0) # temp randomize later

        for k in values:                           
                start_time = time.time()
                dist_d = dijkstra_approx(G, 0, k)
                end_time = time.time()

                djikstra_approx_time[k] += end_time - start_time

                start_time = time.time()
                dist_b = bellman_ford_approx(G, 0, k)
                end_time = time.time()
                
                bellman_approx_time[k] += end_time - start_time

                djikstra_approx_dist[k] += sum(n for n in dist_d.values() if n != float('inf'))
                bellman_approx_dist[k] += sum(n for n in dist_b.values() if n != float('inf'))

    for i in values:
        djikstra_approx_dist[i] /= runs
        bellman_approx_dist[i] /= runs

        djikstra_approx_time[i] /= runs
        bellman_approx_time[i] /= runs


    plt.plot(values, djikstra_approx_dist.values(), color="red", label="Dijkstra Approx")
    plt.plot(values, bellman_approx_dist.values(), color="black", label="Bellman-Ford Approx")
    plt.title("Average Distance vs k Value")
    plt.xlabel("k Value")
    plt.ylabel("Total Reachable Distance")
    plt.legend()
    plt.savefig("Distance_Comparison.png")
    plt.clf() 


    plt.plot(values, djikstra_approx_time.values(), color="red", label="Dijkstra Approx")
    plt.plot(values, bellman_approx_time.values(), color="black", label="Bellman-Ford Approx")
    plt.title("Execution Time vs k Value")
    plt.xlabel("k Value")
    plt.ylabel("Average Time in Seconds")
    plt.legend()
    plt.savefig("Time_Comparison.png")
    plt.clf()

if final1e2:

    values = [2**i for i in range(6)]

    djikstra_approx_dist = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}
    bellman_approx_dist = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}

    djikstra_total = 0
    bellman_total = 0

    for _ in range(runs):
        random_nodes = random.randint(10,100)
        random_edges = random.randint(10,min(500, random_nodes * (random_nodes - 1)))
    
        G = create_random_graph(random_nodes, random_edges,0)
        G2 = create_random_graph(random_nodes, random_edges, 0) 
    
        
        dist_d = dijkstra(G, 0)
        dist_b = bellman_ford(G2, 0)

        djikstra_total += sum(n for n in dist_d.values() if n != float('inf'))
        bellman_total += sum(n for n in dist_b.values() if n != float('inf'))

        for k in values:            
                dist_d_approx = dijkstra_approx(G, 0, k)
                dist_b_approx = bellman_ford_approx(G2, 0, k)
                djikstra_approx_dist[k] += sum(n for n in dist_d_approx.values() if n != float('inf'))
                bellman_approx_dist[k] += sum(n for n in dist_b_approx.values() if n != float('inf'))

    for i in values:
        djikstra_approx_dist[i] /= runs
        bellman_approx_dist[i] /= runs

    djikstra_total /= runs
    bellman_total /= runs

    plt.plot(values, djikstra_approx_dist.values(), color="red", label="Dijkstra Approx")
    plt.axhline(y=djikstra_total, color="black", label="Djikstra")
    plt.title("Djikstra Approximate Distance vs Djikstra's Distance")
    plt.xlabel("k Value")
    plt.ylabel("Total Distance")
    plt.legend()
    plt.savefig("Djikstra Approx distance vs Actual Distance.png")
    plt.clf() 

    plt.plot(values, bellman_approx_dist.values(), color="red", label="Bellman Approx")
    plt.axhline(y=bellman_total, color="black", label="Bellman")
    plt.title("Bellman Approximate Distance vs Bellman's Distance")
    plt.xlabel("k Value")
    plt.ylabel("Total Distance")
    plt.legend()
    plt.savefig("Bellman Approx distance vs Actual Distance.png")
    plt.clf() 



if final1e3:
    values = [2**i for i in range(6)]

    djikstra_approx_dist = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}
    djikstra_approx_dist_sparse = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}

    bellman_approx_dist = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}
    bellman_approx_dist_sparse = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}

    dijkstra_approx_time_sparse = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}
    dijkstra_approx_time_dense  = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}

    bellman_approx_time_sparse  = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}
    bellman_approx_time_dense   = {1:0, 2:0, 4:0, 8:0, 16:0, 32:0}

    djikstra_total_sparse = 0
    djikstra_total_dense = 0

    bellman_total_sparse = 0
    bellman_total_dense = 0


    for _ in range(runs):
        random_nodes = random.randint(10,100)

        sparse_edges = random.randint(10,random_nodes) # Sparse graph

        G = create_random_graph(random_nodes, sparse_edges,0) # sparce graph
        G2 = create_random_complete_graph(random_nodes, 10) # dense graph

        dist_d_sparse = dijkstra(G, 0)
        dist_d_dense= dijkstra(G2, 0)
        
        
        dist_b_sparse = bellman_ford(G, 0)
        dist_b_dense = bellman_ford(G2, 0)

        djikstra_total_sparse += sum(n for n in dist_d_sparse.values() if n != float('inf'))
        djikstra_total_dense += sum(n for n in dist_d_dense.values() if n != float('inf'))

        bellman_total_sparse += sum(n for n in dist_b_sparse.values() if n != float('inf'))
        bellman_total_dense += sum(n for n in dist_b_dense.values() if n != float('inf'))

        for k in values:            
                
                # sparse timing

                start_time = time.time()
                dist_d_approx_sparse = dijkstra_approx(G, 0, k)
                end_time = time.time()
                dijkstra_approx_time_sparse[k] += end_time - start_time

                start_time = time.time()
                dist_b_approx_sparse = bellman_ford_approx(G, 0, k)
                end_time = time.time()
                bellman_approx_time_sparse[k] += end_time - start_time

                # dense timing

                start_time = time.time()
                dist_d_approx = dijkstra_approx(G2, 0, k)
                end_time = time.time()
                dijkstra_approx_time_dense[k] += end_time - start_time

                start_time = time.time()
                dist_b_approx = bellman_ford_approx(G2, 0, k)
                end_time = time.time()
                bellman_approx_time_dense[k] += end_time - start_time

                djikstra_approx_dist[k] += sum(n for n in dist_d_approx.values() if n != float('inf'))
                bellman_approx_dist[k] += sum(n for n in dist_b_approx.values() if n != float('inf'))
                
                djikstra_approx_dist_sparse[k] += sum(n for n in dist_d_approx_sparse.values() if n != float('inf'))
                bellman_approx_dist_sparse[k] += sum(n for n in dist_b_approx_sparse.values() if n != float('inf'))


    for i in values:
        djikstra_approx_dist[i] /= runs
        bellman_approx_dist[i] /= runs
        djikstra_approx_dist_sparse[i] /= runs
        bellman_approx_dist_sparse[i] /= runs

        dijkstra_approx_time_dense[i] /= runs
        dijkstra_approx_time_sparse[i] /= runs
        bellman_approx_time_sparse[i] /= runs
        bellman_approx_time_dense[i] /= runs



    djikstra_total_sparse /= runs
    bellman_total_sparse /= runs
    djikstra_total_dense /= runs
    bellman_total_dense /= runs

    plt.plot(values, djikstra_approx_dist_sparse.values(), color="red", label="Dijkstra Approx")
    plt.axhline(y=djikstra_total_sparse, color="black", label="Dijkstra")
    plt.title("Djikstra Approximate Distance vs Djikstra's Distance on Sparse")
    plt.xlabel("k Value")
    plt.ylabel("Total Distance")
    plt.legend()
    plt.savefig("Djikstra Approx distance vs Actual Distance on Sparse.png")
    plt.clf()

    plt.plot(values, djikstra_approx_dist.values(), color="red",   label="Dijkstra Approx")
    plt.axhline(y=djikstra_total_dense, color="black", label="Dijkstra")
    plt.title("Djikstra Approximate Distance vs Djikstra's Distance on Dense")
    plt.xlabel("k Value")
    plt.ylabel("Total Distance")
    plt.legend()
    plt.savefig("Djikstra Approx distance vs Actual Distance on Dense.png")
    plt.clf()

    plt.plot(values, bellman_approx_dist_sparse.values(), color="red",   label="Bellman Approx")
    plt.axhline(y=bellman_total_sparse,color="black", label="Bellman-Ford")
    plt.title("Bellman Approximate Distance vs Bellman's Distance on Sparse")
    plt.xlabel("k Value")
    plt.ylabel("Total Distance")
    plt.legend()
    plt.savefig("Bellman Approx distance vs Actual Distance on Sparse.png")
    plt.clf()

    plt.plot(values, bellman_approx_dist.values(), color="red",   label="Bellman Approx")
    plt.axhline(y=bellman_total_dense, color="black", label="Bellman-Ford")
    plt.title("Bellman Approximate Distance vs Bellman's Distance on Dense")
    plt.xlabel("k Value")
    plt.ylabel("Total Distance")
    plt.legend()
    plt.savefig("Bellman Approx distance vs Actual Distance on Dense.png")
    plt.clf()

    plt.plot(values, dijkstra_approx_time_sparse.values(), color="red",  label="Sparse")
    plt.plot(values, dijkstra_approx_time_dense.values(),  color="blue", label="Dense")
    plt.title("Dijkstra Approx Execution Time — Sparse vs Dense")
    plt.xlabel("k Value")
    plt.ylabel("Average Time (Seconds)")
    plt.legend()
    plt.savefig("Dijkstra Time Sparse vs Dense.png")
    plt.clf()

    plt.plot(values, bellman_approx_time_sparse.values(), color="red",  label="Sparse")
    plt.plot(values, bellman_approx_time_dense.values(),  color="black", label="Dense")
    plt.title("Bellman-Ford Approx Execution Time, Sparse vs Dense")
    plt.xlabel("k Value")
    plt.ylabel("Average Time (Seconds)")
    plt.legend()
    plt.savefig("Bellman Time Sparse vs Dense.png")
    plt.clf()



if printmys:
    # Negative 

    g1 = DirectedWeightedGraph()
    for i in range(4):
        g1.add_node(i)

    g1.add_edge(0, 1, 3)
    g1.add_edge(1,2, -8)
    g1.add_edge(2,3,9)
    g1.add_edge(0,3,10)
    g1.add_edge(3,0,3)

    #Normal

    g2 = DirectedWeightedGraph()
    for i in range(4):
        g2.add_node(i)

    g2.add_edge(0, 1,-4)
    g2.add_edge(1,2, 2)
    g2.add_edge(2,3,1)
    g2.add_edge(0,3,3)
    g2.add_edge(3,0,2)

    print(mystery(g1))
    print(mystery(g2))


if finalmystery:
    node_sizes = [2**i for i in range(9)]
    amount_time = []

    for i in node_sizes:
        print(i)
        g = create_random_complete_graph(i, 10)
        start_time = time.time()
        mystery(g)
        end_time = time.time()
        amount_time.append(end_time - start_time)

    for i in range(len(node_sizes)):
        print(f"Size: {node_sizes[i]}, Exec Time: {amount_time[i]}")

    plt.loglog(node_sizes, amount_time)
    plt.xlabel("Node Sizes")
    plt.ylabel("Execution Time")
    plt.title("Log-Log Plot")
    plt.savefig("Log-Plot.png")
    plt.clf()

