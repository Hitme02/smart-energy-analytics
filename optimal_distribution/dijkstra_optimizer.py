import heapq
import random

class SmartGridGraph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.nodes = [f"Node_{i}" for i in range(num_nodes)]
        self.edges = {node: [] for node in self.nodes}

    def add_edge(self, from_node, to_node, weight):
        self.edges[from_node].append((to_node, weight))
        self.edges[to_node].append((from_node, weight))  # Assuming undirected graph

    def generate_random_edges(self, max_edges_per_node=3, max_weight=20):
        for node in self.nodes:
            neighbors = random.sample([n for n in self.nodes if n != node], k=random.randint(1, max_edges_per_node))
            for neighbor in neighbors:
                weight = random.randint(1, max_weight)
                self.add_edge(node, neighbor, weight)

    def dijkstra(self, start_node):
        distances = {node: float("inf") for node in self.nodes}
        distances[start_node] = 0
        priority_queue = [(0, start_node)]
        previous = {node: None for node in self.nodes}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            for neighbor, weight in self.edges[current_node]:
                distance = current_distance + weight
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        return distances, previous

    def reconstruct_path(self, previous, target_node):
        path = []
        current = target_node
        while current:
            path.insert(0, current)
            current = previous[current]
        return path

def simulate_dijkstra_run():
    print("🔄 Simulating Smart Grid Topology...")
    num_nodes = 10
    graph = SmartGridGraph(num_nodes)
    graph.generate_random_edges()

    source_node = random.choice(graph.nodes)
    print(f"\n🚀 Running Dijkstra from source node: {source_node}\n")
    distances, previous = graph.dijkstra(source_node)

    for target_node in graph.nodes:
        if target_node != source_node:
            path = graph.reconstruct_path(previous, target_node)
            print(f"🛣️ Path to {target_node}: {' ➡️ '.join(path)} (Cost: {distances[target_node]})")

if __name__ == "__main__":
    simulate_dijkstra_run()

# Expose for import
__all__ = ["SmartGridGraph"]
