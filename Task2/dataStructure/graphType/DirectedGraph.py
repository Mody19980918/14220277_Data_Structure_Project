from dataStructure.adjancencyMethod.adjacencyMatrix import AdjacencyMatrixGraph
from dataStructure.adjancencyMethod.adjacencyListGraph import AdjacencyListGraph
from dataStructure.graphType.GraphType import GraphType
from typing import List, Tuple
from dataStructure.edge import Edge
class DirectedGraph:
    """
    This is about directed graph implementation
    support both adjacency list and adjacency matrix implementation
    """

    def __init__(self, num_vertices: int, use_matrix: bool = False):
        self.use_matrix = use_matrix
        if use_matrix:
            self.graph = AdjacencyMatrixGraph(num_vertices, GraphType.DIRECTED)
        else:
            self.graph = AdjacencyListGraph(num_vertices, GraphType.DIRECTED)

    def add_vertex(self) -> int:
        """add a new vertex and return its index"""
        return self.graph.add_vertex()

    def remove_vertex(self, vertex: int) -> None:
        """remove a vertex and all its connected edges"""
        self.graph.remove_vertex(vertex)

    def add_edge(self, from_v: int, to_v: int, weight: float = 1.0) -> None:
        """add directed edge"""
        self.graph.add_edge(from_v, to_v, weight)

    def remove_edge(self, from_v: int, to_v: int) -> None:
        """remove directed edge"""
        self.graph.remove_edge(from_v, to_v)

    def has_edge(self, from_v: int, to_v: int) -> bool:
        """check if directed edge exists"""
        return self.graph.has_edge(from_v, to_v)

    def get_neighbors(self, vertex: int) -> List[Tuple[int, float]]:
        """get the neighbors of the vertex"""
        return self.graph.get_neighbors(vertex)

    def get_out_degree(self, vertex: int) -> int:
        """get the out degree of the vertex"""
        return self.graph.get_out_degree(vertex)

    def get_in_degree(self, vertex: int) -> int:
        """get the in degree of the vertex"""
        return self.graph.get_in_degree(vertex)

    def get_degree(self, vertex: int) -> int:
        """get the degree of the vertex"""
        return self.graph.get_degree(vertex)

    def display(self) -> None:
        """display the graph"""
        self.graph.display()

    def get_all_edges(self) -> List[Edge]:
        """get all edges"""
        return self.graph.get_all_edges()

    @property
    def num_vertices(self) -> int:
        """get the number of vertices"""
        return self.graph.num_vertices

