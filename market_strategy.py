import networkx as nx
import argparse
from collections import deque
import matplotlib.pyplot as plt

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("file", type=str)
    parser.add_argument("--plot", action="store_true")
    parser.add_argument("--interactive", action="store_true")
    return parser.parse_args()

def main():
    args = parse_args()
    graph = read_graph(args.file)
    buyers, sellers = get_buyers_and_sellers(graph)

    matching, price = market_clearing(graph, buyers, sellers, args.interactive)
    if args.plot:
        plot_graph(graph, buyers, sellers, matching, price)


def get_buyers_and_sellers(graph):
    buyers = [node for node, attrs in graph.nodes(data=True) if attrs.get("bipartite") == 1]
    sellers = [node for node, attrs in graph.nodes(data=True) if attrs.get("bipartite") == 0]
    return buyers, sellers

def plot_graph(graph, buyers, sellers, matching, price):
    pos = nx.spring_layout(graph)
    node_colors = ["red" if node in buyers else "skyblue" if node in sellers else "gray" for node in graph.nodes]
    nx.draw(graph, pos, with_labels=True, node_color=node_colors)
    edge_labels = nx.get_edge_attributes(graph, "valuation")
    if edge_labels:
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    matched_edges = [(b, s) for b, s in matching.items()]
    nx.draw_networkx_edges(graph, pos, edgelist=matched_edges, edge_color="blue", width=2)
    plt.show()

import networkx as nx
from collections import deque

def market_clearing(graph, buyers, sellers, interactive=False):
    # initialize prices for sellers
    for s in sellers:
        graph.nodes[s]["price"] = graph.nodes[s].get("price", 0)

    i = 0
    while True:
        price = {s: graph.nodes[s]['price'] for s in sellers}

        demand = build_preferred_graph(graph, buyers, sellers)
        matching = bipartite_matching(demand, buyers)

        if interactive:
            demand_edges = list(demand.edges())
            matched_pairs = {b: matching[b] for b in buyers if b in matching}
            print(f"Round {i}: prices={price}, demand={demand_edges}, matching={matched_pairs}")

        # stop when every buyer matched
        if is_perfect_matching(matching, buyers):
            return matching, price

        # find constricted seller set
        buyer_set, seller_set = constricted_set(demand, matching, buyers)

        # --- FIX 1: fallback when constricted_set empty
        if not seller_set:
            counts = {s: 0 for s in sellers}
            for b in buyers:
                for s in demand.neighbors(b):
                    counts[s] += 1
            seller_set = [s for s, c in counts.items() if c > 1]
            if not seller_set:
                raise RuntimeError("No constricted or overdemanded sellers found.")

        # --- FIX 2: raise prices for those sellers
        for s in seller_set:
            graph.nodes[s]['price'] += 1

        i += 1


def build_preferred_graph(graph, buyers, sellers):
    demand = nx.Graph()
    sellers = set(sellers)
    for b in buyers:
        utilities = []
        for s in graph.neighbors(b):
            if s not in sellers:
                continue
            val = graph[b][s]['valuation']
            price = graph.nodes[s]['price']
            utilities.append((val - price, s))
        if not utilities:
            continue
        max_util = max(u for u, _ in utilities)
        for u, s in utilities:
            if u == max_util:
                demand.add_edge(b, s)
    return demand


def bipartite_matching(demand, buyers):
    return nx.algorithms.bipartite.maximum_matching(demand, top_nodes=set(buyers))


def is_perfect_matching(matching, buyers):
    return all(b in matching for b in buyers)


def constricted_set(demand, matching, buyers):
    unmatched = [b for b in buyers if b not in matching]
    visited_buyers = set(unmatched)
    visited_sellers = set()
    queue = deque(unmatched)

    while queue:
        b = queue.popleft()
        for s in demand.neighbors(b):
            if s in visited_sellers:
                continue
            visited_sellers.add(s)
            matched_b = matching.get(s)
            if matched_b and matched_b not in visited_buyers:
                visited_buyers.add(matched_b)
                queue.append(matched_b)
    return visited_buyers, visited_sellers


def read_graph(file):
    try: 
        return nx.read_gml(file)
    except Exception as e:
        print(f"Error reading graph from {file}: {e}")
        raise e
        

if __name__ == "__main__":
    main()