from dataStructure.graphType.UndirectedGraph import UndirectedGraph
from dataStructure.graphType.DirectedGraph import DirectedGraph

DIVIDER = "=" * 60


def main():
    """
    This is the main function of the project,
    it will show that :
    1. the usage of undirected graph, directed graph, adjacency list and adjacency matrix
    2. the internal data structure of the graph
    3. the graph information
    4. the graph operation demo
    """
    print(DIVIDER)
    print("       Graph Data Structure (Graph Data Structure) Demo")
    print(DIVIDER)

    # ==================== undirected graph - adjacency list ====================
    print("\n" + DIVIDER)
    print("【1】undirected graph (Undirected Graph) - adjacency list implementation")
    print(DIVIDER)

    undirected_adj_list = UndirectedGraph(num_vertices=5, use_matrix=False)

    # add edges (build a simple undirected graph)
    edges_to_add = [
        (0, 1, 1.0),  # 0-1
        (0, 2, 2.0),  # 0-2 (weight 2)
        (1, 2, 1.0),  # 1-2
        (1, 3, 3.0),  # 1-3 (weight 3)
        (2, 4, 1.0),  # 2-4
        (3, 4, 2.0),  # 3-4 (weight 2)
    ]

    print("\nadd edges:")
    for u, v, w in edges_to_add:
        undirected_adj_list.add_edge(u, v, w)
        print(f"  add edge ({u} --{w}-- {v})")

    undirected_adj_list.display()

    # print the internal data structure
    print("\n【internal data structure - adjacency list (Adjacency List)】")
    print("  adjacency_list = {{")
    for vertex, neighbors in undirected_adj_list.graph.adjacency_list.items():
        print(f"    {vertex}: {neighbors}")
    print("  }}")

    print("\ngraph information:")
    print(f"  All edges: {undirected_adj_list.get_all_edges()}")
    for i in range(5):
        print(f"  vertex {i} degree: {undirected_adj_list.get_degree(i)}")
        print(f"  vertex {i} neighbors: {undirected_adj_list.get_neighbors(i)}")

    # ==================== undirected graph - adjacency matrix ====================
    print("\n" + DIVIDER)
    print("【2】undirected graph (Undirected Graph) - adjacency matrix implementation")
    print(DIVIDER)

    undirected_adj_matrix = UndirectedGraph(num_vertices=5, use_matrix=True)

    print("\nadd same edges:")
    for u, v, w in edges_to_add:
        undirected_adj_matrix.add_edge(u, v, w)

    undirected_adj_matrix.display()

    # print the internal data structure
    print("\n【internal data structure - adjacency matrix (Adjacency Matrix)】")
    print("  matrix = [")
    for i, row in enumerate(undirected_adj_matrix.graph.matrix):
        row_str = ", ".join(f"{int(val)}" for val in row)
        print(f"    [{row_str}],  # vertex {i}")
    print("  ]")

    print("\ngraph information:")
    print(f"  edge (0,1) exists? {undirected_adj_matrix.has_edge(0, 1)}")
    print(f"  edge (0,3) exists? {undirected_adj_matrix.has_edge(0, 3)}")

    # ==================== directed graph - adjacency list ====================
    print("\n" + DIVIDER)
    print("【3】directed graph (Directed Graph) - adjacency list implementation")
    print(DIVIDER)

    directed_list = DirectedGraph(num_vertices=6, use_matrix=False)

    # add directed edges (build a DAG - directed acyclic graph)
    directed_edges = [
        (0, 1, 1.0),  # 0 -> 1
        (0, 2, 1.0),  # 0 -> 2
        (1, 3, 2.0),  # 1 -> 3
        (2, 3, 1.0),  # 2 -> 3
        (2, 4, 3.0),  # 2 -> 4
        (3, 5, 1.0),  # 3 -> 5
        (4, 5, 2.0),  # 4 -> 5
    ]

    print("\nadd directed edges:")
    for u, v, w in directed_edges:
        directed_list.add_edge(u, v, w)
        print(f"  add edge ({u} --{w}--> {v})")

    directed_list.display()

    # print the internal data structure
    print("\n【internal data structure - adjacency list (Adjacency List)】")
    print("  adjacency_list = {{")
    for vertex, neighbors in directed_list.graph.adjacency_list.items():
        print(f"    {vertex}: {neighbors}")
    print("  }}")

    print("\ngraph information:")
    print(f"  all edges: {directed_list.get_all_edges()}")
    for i in range(6):
        print(
            f"  vertex {i}: out degree={directed_list.get_out_degree(i)}, "
            f"in degree={directed_list.get_in_degree(i)}, "
            f"total degree={directed_list.get_degree(i)}"
        )

    # ==================== directed graph - adjacency matrix ====================
    print("\n" + DIVIDER)
    print("【4】directed graph (Directed Graph) - adjacency matrix implementation")
    print(DIVIDER)

    directed_matrix = DirectedGraph(num_vertices=6, use_matrix=True)

    print("\nadd same directed edges:")
    for u, v, w in directed_edges:
        directed_matrix.add_edge(u, v, w)

    directed_matrix.display()

    # print the internal data structure
    print("\n【internal data structure - adjacency matrix (Adjacency Matrix)】")
    print("  matrix = [")
    for i, row in enumerate(directed_matrix.graph.matrix):
        row_str = ", ".join(f"{int(val)}" for val in row)
        print(f"    [{row_str}],  # vertex {i}")
    print("  ]")

    print("\ngraph information:")
    print(f"  edge (0 -> 1) exists? {directed_matrix.has_edge(0, 1)}")
    print(f"  edge (1 -> 0) exists? {directed_matrix.has_edge(1, 0)}")
    print(f"  vertex 3 neighbors: {directed_matrix.get_neighbors(3)}")

    # ==================== add vertex demo ====================
    print("\n" + DIVIDER)
    print("【5】add vertex (adjacency list and adjacency matrix)")
    print(DIVIDER)

    # demo for adjacency list
    dynamic_graph_list = UndirectedGraph(num_vertices=3, use_matrix=False)
    dynamic_graph_list.add_edge(0, 1)
    dynamic_graph_list.add_edge(1, 2)

    print("\ninitial graph (3 vertices):")
    dynamic_graph_list.display()

    # add new vertices
    new_vertex_1 = dynamic_graph_list.add_vertex()
    print(f"\nadded new vertex: {new_vertex_1}")

    new_vertex_2 = dynamic_graph_list.add_vertex()
    print(f"added new vertex: {new_vertex_2}")

    # add edges to new vertices
    dynamic_graph_list.add_edge(0, new_vertex_1)
    dynamic_graph_list.add_edge(new_vertex_1, new_vertex_2)
    dynamic_graph_list.add_edge(2, new_vertex_2)

    print("\nafter adding 2 new vertices and edges:")
    dynamic_graph_list.display()
    print(f"\nnow total vertices: {dynamic_graph_list.num_vertices}")

    # demo for adjacency matrix
    print("\n" + "-" * 40)
    print("adjacency matrix version:")
    print("-" * 40)

    dynamic_graph_matrix = UndirectedGraph(num_vertices=3, use_matrix=True)
    dynamic_graph_matrix.add_edge(0, 1)
    dynamic_graph_matrix.add_edge(1, 2)

    print("\ninitial graph (3 vertices):")
    dynamic_graph_matrix.display()

    new_vertex_3 = dynamic_graph_matrix.add_vertex()
    print(f"\nadded new vertex: {new_vertex_3}")
    dynamic_graph_matrix.add_edge(0, new_vertex_3)

    print("\nafter adding new vertex and edge:")
    dynamic_graph_matrix.display()
    print(f"\nnow total vertices: {dynamic_graph_matrix.num_vertices}")

    # ==================== operation demo ====================
    print("\n" + DIVIDER)
    print("【6】add / remove edge Demo")
    print(DIVIDER)

    test_graph = UndirectedGraph(num_vertices=4, use_matrix=False)
    test_graph.add_edge(0, 1)
    test_graph.add_edge(0, 2)
    test_graph.add_edge(1, 2)
    test_graph.add_edge(2, 3)

    print("\ninitial graph:")
    test_graph.display()

    print("\nafter removing edge (0, 2):")
    test_graph.remove_edge(0, 2)
    test_graph.display()

    print(f"\ncheck edge (0, 2): {test_graph.has_edge(0, 2)}")
    print(f"check edge (0, 1): {test_graph.has_edge(0, 1)}")

    print("\n" + DIVIDER)
    print("              demo complete - Demo Complete")
    print(DIVIDER)


if __name__ == "__main__":
    main()
