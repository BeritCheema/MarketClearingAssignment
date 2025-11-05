import pandas as pd
import networkx as nx
import argparse
from collections import defaultdict
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
    print(f"Graph read successfully")
    buyers, sellers = get_buyers_and_sellers(graph)
    print(f"Buyers: {buyers}")
    print(f"Sellers: {sellers}")

    market_clearing(graph, buyers, sellers, args.interactive)
    if args.plot:
        print(f"Plotting graph")
        plot_graph(graph, buyers, sellers)


def get_buyers_and_sellers(graph):
    buyers = [node for node, attrs in graph.nodes(data=True) if attrs.get("bipartite") == 0]
    sellers = [node for node, attrs in graph.nodes(data=True) if attrs.get("bipartite") == 1]
    return buyers, sellers

def plot_graph(graph, buyers, sellers):
    pos = nx.spring_layout(graph)
    node_colors = ["red" if node in buyers else "skyblue" for node in graph.nodes]
    nx.draw(graph, pos, with_labels=True, node_color=node_colors)
    edge_labels = nx.get_edge_attributes(graph, "valuation")
    if edge_labels:
        nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    plt.show()

def market_clearing(graph, buyers, sellers, interactive):

    return 0

def compute_demand_order(graph, buyer):
    demand_order = []
    for seller in buyer.neighbors():
        demand_order.append((seller, graph.get_edge_data(buyer, seller).get("valuation")))
    demand_order.sort(key=lambda x: x[1], reverse=True)
    return demand_order


def read_graph(file):
    print(f"Reading graph from {file}")
    return nx.read_gml(file)
        

if __name__ == "__main__":
    main()