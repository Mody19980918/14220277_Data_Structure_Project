from dataStructure.graphADT import GraphADT
from dataStructure.graphType.GraphType import GraphType
from typing import Dict, List, Tuple
from dataStructure.edge import Edge

DIVIDER="="*50

class AdjacencyListGraph(GraphADT):
    """
    This is about adjacency list implementation of graph
    Adjacency list format :
    adjacency_list[vertex] = [(neighbor, weight), ...]
    Example : 
    adjacency_list = {
        0: [(1, 1.0), (2, 2.0)],
        1: [(0, 1.0), (2, 1.0), (3, 3.0)],
        2: [(0, 2.0), (1, 1.0), (4, 1.0)],
        3: [(1, 3.0), (4, 2.0)],
        4: [(2, 1.0), (3, 2.0)],
    }
    """

    def __init__(self, num_vertices: int, graph_type: GraphType = GraphType.UNDIRECTED):
        super().__init__(num_vertices, graph_type)
        """init the adjacency list"""
        self.adjacency_list: Dict[int, List[Tuple[int, float]]] = {
            i: [] for i in range(num_vertices)
        }

    def add_vertex(self) -> int:
        """add a new vertex and return its index"""
        new_vertex_id = self.num_vertices
        self.adjacency_list[new_vertex_id] = []
        self.num_vertices += 1
        return new_vertex_id

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """add edge to adjacency list"""
        self.validate_vertex(u)
        self.validate_vertex(v)

        if u == v:
            raise ValueError("cannot add self-loop edge")

        # check the edge is already exists
        for neighbor in self.adjacency_list[u]:
            if neighbor == v:
                return  # edge already exists, do not add again

        # add edge
        self.adjacency_list[u].append((v, weight))

        # undirected graph needs to add bidirectional
        if self.graph_type == GraphType.UNDIRECTED:
            self.adjacency_list[v].append((u, weight))

    def remove_edge(self, u: int, v: int) -> None:
        """remove edge from adjacency list"""
        self.validate_vertex(u)
        self.validate_vertex(v)

        # remove u -> v
        self.adjacency_list[u] = [
            (neighbor, weight) for neighbor, weight in self.adjacency_list[u]
            if neighbor != v
        ]

        # undirected graph needs to remove v -> u
        if self.graph_type == GraphType.UNDIRECTED:
            self.adjacency_list[v] = [
                (neighbor, weight) for neighbor, weight in self.adjacency_list[v]
                if neighbor != u
            ]

    def has_edge(self, u: int, v: int) -> bool:
        """check if edge exists"""
        self.validate_vertex(u)
        self.validate_vertex(v)

        for neighbor, _ in self.adjacency_list[u]:
            if neighbor == v:
                return True
        return False

    def get_neighbors(self, vertex: int) -> List[Tuple[int, float]]:
        """get the neighbors of the vertex"""
        self.validate_vertex(vertex)
        return self.adjacency_list[vertex].copy()

    def get_degree(self, vertex: int) -> int:
        """get the degree of the vertex"""
        self.validate_vertex(vertex)

        if self.graph_type == GraphType.UNDIRECTED:
            return len(self.adjacency_list[vertex])
        else:
            # directed graph: out degree + in degree
            out_degree = len(self.adjacency_list[vertex])
            in_degree = sum(
                1 for u in range(self.num_vertices)
                for v, _ in self.adjacency_list[u]
                if v == vertex
            )
            return out_degree + in_degree

    def get_out_degree(self, vertex: int) -> int:
        """get the out degree of the vertex"""
        self.validate_vertex(vertex)
        return len(self.adjacency_list[vertex])

    def get_in_degree(self, vertex: int) -> int:
        """get the in degree of the vertex"""
        self.validate_vertex(vertex)
        return sum(
            1 for u in range(self.num_vertices)
            for v in self.adjacency_list[u]
            if v == vertex
        )

    def display(self) -> None:
        """display the adjacency list"""
        print(f"\n{DIVIDER}")
        print(f"adjacency list graph ({self.graph_type.value})")
        print(f"number of vertices: {self.num_vertices}")
        print(f"{DIVIDER}")

        for vertex in range(self.num_vertices):
            neighbors = self.adjacency_list[vertex]
            if neighbors:
                neighbor_str = ", ".join([
                    f"{v}(w={w})" if w != 1.0 else str(v)
                    for v, w in neighbors
                ])
                print(f"  vertex {vertex} -> [{neighbor_str}]")
            else:
                print(f"  vertex {vertex} -> []")

    def get_all_edges(self) -> List[Edge]:
        """get all edges"""
        edges = []
        visited = set()

        for u in range(self.num_vertices):
            for v, w in self.adjacency_list[u]:
                if self.graph_type == GraphType.UNDIRECTED:
                    edge_key = tuple(sorted([u, v]))
                    if edge_key not in visited:
                        visited.add(edge_key)
                        edges.append(Edge(u, v, w))
                else:
                    edges.append(Edge(u, v, w))

        return edges