from dataStructure.adjancencyMethod.adjacencyMatrix import AdjacencyMatrixGraph
from dataStructure.adjancencyMethod.adjacencyListGraph import AdjacencyListGraph
from dataStructure.graphType.GraphType import GraphType
from typing import List, Tuple
from dataStructure.edge import Edge
class UndirectedGraph:
    """
    This is about undirected graph implementation
    support both adjacency list and adjacency matrix implementation
    """

    def __init__(self, num_vertices: int, use_matrix: bool = False):
        self.use_matrix = use_matrix
        if use_matrix:
            self.graph = AdjacencyMatrixGraph(num_vertices, GraphType.UNDIRECTED)
        else:
            self.graph = AdjacencyListGraph(num_vertices, GraphType.UNDIRECTED)

    def add_vertex(self) -> int:
        """add a new vertex and return its index"""
        return self.graph.add_vertex()

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """add undirected edge"""
        self.graph.add_edge(u, v, weight)

    def remove_edge(self, u: int, v: int) -> None:
        """remove undirected edge"""
        self.graph.remove_edge(u, v)

    def has_edge(self, u: int, v: int) -> bool:
        """check if undirected edge exists"""
        return self.graph.has_edge(u, v)

    def get_neighbors(self, vertex: int) -> List[Tuple[int, float]]:
        """get the neighbors of the vertex"""
        return self.graph.get_neighbors(vertex)

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
