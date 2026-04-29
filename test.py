import pytest
from hopcroft_tarjan import hopcroft_tarjan


# --- Articulation Points ---

def test_simple_bridge_and_ap():
    # 1 - 2 - 3: node 2 is AP, edge (1,2) and (2,3) are both bridges
    edges = [(1, 2), (2, 3)]
    aps, bridges = hopcroft_tarjan(edges)
    assert aps == {2}
    assert set(bridges) == {(1, 2), (2, 3)}


def test_triangle_no_ap_no_bridge():
    # Fully connected triangle: no APs, no bridges
    edges = [(1, 2), (2, 3), (1, 3)]
    aps, bridges = hopcroft_tarjan(edges)
    assert aps == set()
    assert bridges == []


def test_star_graph():
    # Centre node 1 connected to 2, 3, 4: centre is AP, all edges are bridges
    edges = [(1, 2), (1, 3), (1, 4)]
    aps, bridges = hopcroft_tarjan(edges)
    assert aps == {1}
    assert set(bridges) == {(1, 2), (1, 3), (1, 4)}


def test_two_triangles_joined_by_bridge():
    # Triangle 1-2-3 and triangle 4-5-6, joined by edge (3, 4)
    # APs: 3 and 4, bridge: (3, 4)
    edges = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5), (5, 6), (4, 6)]
    aps, bridges = hopcroft_tarjan(edges)
    assert aps == {3, 4}
    assert set(bridges) == {(3, 4)}


def test_linear_chain():
    # 1 - 2 - 3 - 4: all interior nodes are APs, all edges are bridges
    edges = [(1, 2), (2, 3), (3, 4)]
    aps, bridges = hopcroft_tarjan(edges)
    assert aps == {2, 3}
    assert set(bridges) == {(1, 2), (2, 3), (3, 4)}


def test_single_edge():
    # Just one edge: no APs (only 2 nodes), but the edge is a bridge
    edges = [(1, 2)]
    aps, bridges = hopcroft_tarjan(edges)
    assert aps == set()
    assert set(bridges) == {(1, 2)}


def test_single_node_isolated():
    # Isolated node with no edges
    edges = []
    aps, bridges = hopcroft_tarjan(edges, nodes=[1])
    assert aps == set()
    assert bridges == []


def test_disconnected_graph():
    # Two separate triangles, no connection between them
    edges = [(1, 2), (2, 3), (1, 3), (4, 5), (5, 6), (4, 6)]
    aps, bridges = hopcroft_tarjan(edges)
    assert aps == set()
    assert bridges == []


def test_multigraph_parallel_edges():
    # Two parallel edges between 1 and 2: neither is a bridge
    edges = [(1, 2), (1, 2)]
    aps, bridges = hopcroft_tarjan(edges)
    assert aps == set()
    assert bridges == []


def test_isolated_nodes_ignored_for_ap():
    # Isolated nodes passed via `nodes` should not affect AP/bridge results
    edges = [(1, 2), (2, 3)]
    aps, bridges = hopcroft_tarjan(edges, nodes=[99, 100])
    assert aps == {2}
    assert set(bridges) == {(1, 2), (2, 3)}
    assert 99 not in aps
    assert 100 not in aps


def test_cycle_no_bridge():
    # A 5-node cycle: no APs, no bridges
    edges = [(1, 2), (2, 3), (3, 4), (4, 5), (5, 1)]
    aps, bridges = hopcroft_tarjan(edges)
    assert aps == set()
    assert bridges == []


def test_complex_graph():
    # Cycle (1-2-3) connected via AP 3 to a chain (3-4-5)
    edges = [(1, 2), (2, 3), (1, 3), (3, 4), (4, 5)]
    aps, bridges = hopcroft_tarjan(edges)
    assert aps == {3, 4}
    assert set(bridges) == {(3, 4), (4, 5)}