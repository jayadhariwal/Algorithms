import networkx as nx
import random
from hopcroft_tarjan import hopcroft_tarjan


def test_planarity(G: nx.Graph) -> dict:
    is_planar, certificate = nx.check_planarity(G, counterexample=True)

    return {
        "is_planar": is_planar,
        "embedding": certificate if is_planar else None,
        "kuratowski": certificate if not is_planar else None,
    }

#create a random graph :)
def random_graph_planarity_check(
    n_nodes: int | None = None,
    n_edges: int | None = None,
    seed: int | None = None,
) -> dict:

    rng = random.Random(seed)

    if n_nodes is None:
        n_nodes = rng.randint(4, 12)

    max_edges = n_nodes * (n_nodes - 1) // 2

    if n_edges is None:
        n_edges = rng.randint(0, max_edges)

    if n_edges > max_edges:
        raise ValueError("Too many edges for the number of nodes")

    G = nx.gnm_random_graph(n_nodes, n_edges, seed=seed)

    result = test_planarity(G)

    return {
        "graph": G,
        "n_nodes": n_nodes,
        "n_edges": G.number_of_edges(),
        **result,
    }

#print all the outputs 
def analyze_random_graph(seed: int | None = None):
    r = random_graph_planarity_check(seed=seed)

    G = r["graph"]
    is_planar = r["is_planar"]
    edges = list(G.edges())
    nodes = list(G.nodes())

    articulation_points, bridges = hopcroft_tarjan(edges, nodes)

    verdict = "PLANAR" if is_planar else "NON-PLANAR"

    print(f"Planarity Check : {verdict}")
    print(f"Nodes           : {nodes}")
    print(f"Edges           : {edges}")

    print("Hopcroft-Tarjan :")
    print(f"  Art. points   : {sorted(articulation_points) if articulation_points else 'none'}")
    print(f"  Bridges       : {bridges if bridges else 'none'}")

#let the user pick the seed (seeds are stored so you can revisit a specific graph if case doesn't wotk) :)
if __name__ == "__main__":
    seed_input = input("Enter a seed, or press enter for random: ")
    seed = int(seed_input) if seed_input.strip() else None
    analyze_random_graph(seed=seed)
    
