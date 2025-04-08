# trading/graph_trading.py

import networkx as nx

def build_energy_market():
    G = nx.DiGraph()

    # Sample nodes: buyers and sellers
    sellers = {"S1": 30, "S2": 40, "S3": 20}  # kWh available
    buyers = {"B1": 25, "B2": 35, "B3": 30}   # kWh needed

    # Add sellers
    for seller, supply in sellers.items():
        G.add_node(seller, type="seller", supply=supply)

    # Add buyers
    for buyer, demand in buyers.items():
        G.add_node(buyer, type="buyer", demand=demand)

    # Connect sellers to buyers with dummy costs (edge weight = cost per kWh)
    for s in sellers:
        for b in buyers:
            G.add_edge(s, b, weight=1 + abs(sellers[s] - buyers[b]) * 0.1)

    return G

def run_trading():
    G = build_energy_market()
    print("⚡ Energy Market Graph:")
    for u, v, d in G.edges(data=True):
        print(f"{u} → {v} | Cost: {d['weight']:.2f}")

    # Match buyers to cheapest sellers using Dijkstra's algorithm
    matches = {}
    for buyer in [n for n, attr in G.nodes(data=True) if attr["type"] == "buyer"]:
        paths = nx.single_source_dijkstra_path_length(G, source=None, weight="weight")
        seller = min(paths[buyer], key=lambda x: paths[buyer][x] if x in paths[buyer] else float("inf"))
        matches[buyer] = seller

    print("\n✅ Optimal Trades:")
    for buyer, seller in matches.items():
        print(f"{buyer} buys from {seller}")

if __name__ == "__main__":
    run_trading()
