import sys
from collections import defaultdict


def hopcroft_tarjan(edges, nodes=None): #take a list of edge tupeles, nodes is optional

#build an adjacency list
    graph = defaultdict(list)

    for edge_id, (u, v) in enumerate(edges): #give each edge a unique number/ID and store the neighbors as pairs
        graph[u].append((v, edge_id))
        graph[v].append((u, edge_id))
#gives us all the nodes that appear in at least 1 edge (if theres nodes we parse through those too)
    all_nodes = set(graph)
    if nodes is not None: #checks if nodes is not empty
        all_nodes.update(nodes)

#sets a recursion limit, so the program doesn't terminate before python's default limit of 1000
    sys.setrecursionlimit(max(10000, len(all_nodes) * 10))

#set variables to track information in the recursion
    time = 0 #DFS time counter
    visited = set() #tracks which nodes DFS has already visited
    disc = {} #checks the time when U was discovered
    low = {} #the lowest disc value found 
    parent = {} #u node that discovered V in the DFS tree

    #outputs collected
    articulation_points = set()
    bridges = []

    def dfs(u, parent_edge_id=None):
        nonlocal time #used to modify time counter

        #mark u as visited, record time found, intitalize low[u] to its discovery time
        visited.add(u) 
        disc[u] = low[u] = time
        time += 1
        children = 0 #counts DFS children

        #neighbor loop 
        for v, edge_id in graph[u]:
            if edge_id == parent_edge_id: #skip edge we started on (using edge_id)
                continue

            #if v is unvisited, record u as its parent, incremend child count and make sure we don't walk backwards
            if v not in visited: 
                parent[v] = u
                children += 1

                dfs(v, edge_id)
                
                #pull up any low value v discovered
                low[u] = min(low[u], low[v])

                #if v's subtree cannot reach above u, then removing u disconnects v's subtree (non-root articulation)
                if u in parent and low[v] >= disc[u]:
                    articulation_points.add(u)
                #(bridge check) if v's subtree can't even reach u, then edge (u,v) is the only connection
                if low[v] > disc[u]:
                    bridges.append((u, v))
            #v is already visited and isn't the parent edge -> there is a cycle
            else:
                low[u] = min(low[u], disc[v])
        #if a tree has 2+ children, then add u as an articulation point
        if u not in parent and children > 1:
            articulation_points.add(u)
#run DFS from every unvisited node, checks that the disconnected components are not missed
    for node in all_nodes:
        if node not in visited:
            dfs(node)
#return output
    return articulation_points, bridges

