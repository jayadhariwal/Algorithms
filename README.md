Source: https://github.com/naens/hopcroft-tarjan (We took inspiration from this but we changed it because the code was outdated)
Explanation:
The python function takes an input of a list of edges (and also nodes optionally) and builds an adjacency list where every edge has a unique id/number associated with it. It then runs depth first search on every node which tracks:
Disc (when the node was first visited)
Low (earliest discovered node that is reachable from its subtree via back edge)
As DFS recurses, it skips the exact edge it started on and it uses edge ID’s to determine that versus just its nodes so parallel edges can be handled correctly. After returning a child node (v), it’ll check 2 conditions: 
If v’s subtree cannot reach above u -> u is an articulation point whose removal will disconnect v’s subtree
If v’s subtree can’t each u -> then the edge (u,v) is a bridge, whose removal disconnects the graph.
Root nodes in the DFS have a special edge case check, and they’re only critical if there’s 2+ children. 
The outer loop makes sure all disconnected components are visited and the nodes parameter allows isolated nodes with 0 edges be included.
