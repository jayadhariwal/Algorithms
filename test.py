import networkx as nx
import random
from hopcroft_tarjan import hopcroft_tarjan

def test_planarity(G: nx.Graph) -> dict:
    is_planar, certificate = nx.check_planarity(G, counterexample=True)
    return {
        "is_planar": is_planar,
        "embedding": certificate if is_planar else None,
        "kuratowski": None if is_planar else certificate,
    }

def random_graph_planarity_check(
    n_nodes: int = None,
    n_edges: int = None,
    seed: int = None,
) -> dict:

    rng = random.Random(seed)

    if n_nodes is None:
        n_nodes = rng.randint(4, 12)

    max_edges = n_nodes * (n_nodes - 1) // 2
    if n_edges is None:
        n_edges = rng.randint(n_nodes - 1, max_edges)
    n_edges = min(n_edges, max_edges)

    G = nx.gnm_random_graph(n_nodes, n_edges, seed=seed)

    result = test_planarity(G)
    return {
        "graph": G,
        "n_nodes": n_nodes,
        "n_edges": n_edges,
        **result,
    }

def analyze_random_graph(seed: int = None):
    r = random_graph_planarity_check(seed=seed)
    G         = r["graph"]
    is_planar = r["is_planar"]
    edges     = list(G.edges())
    nodes     = list(G.nodes())

    articulation_points, bridges = hopcroft_tarjan(edges, nodes)

    # Planarity
    verdict = "PLANAR" if is_planar else "NON-PLANAR"
    print(f"Planarity Check : {verdict}")
    print(f"Edges           : {edges}")

    # Hopcroft-Tarjan
    print(f"Hopcroft-Tarjan :")
    print(f"  Art. points   : {sorted(articulation_points) if articulation_points else 'none'}")
    print(f"  Bridges       : {bridges if bridges else 'none'}")

if __name__ == "__main__":
    seed = int(input("Enter a seed: "))
    analyze_random_graph(seed=seed)
