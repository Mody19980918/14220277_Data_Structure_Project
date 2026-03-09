from abc import ABC, abstractmethod
from typing import List, Tuple
from Data_Structure.GraphType.GraphType import GraphType

class GraphADT(ABC):
    """Abstract Data Type of Graph (ADT)"""

    def __init__(self, num_vertices: int, graph_type: GraphType = GraphType.UNDIRECTED):
        self.num_vertices = num_vertices
        self.graph_type = graph_type

    @abstractmethod
    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """add edge between u and v"""
        pass

    @abstractmethod
    def remove_edge(self, u: int, v: int) -> None:
        """remove edge between u and v"""
        pass

    @abstractmethod
    def has_edge(self, u: int, v: int) -> bool:
        """check edge between u and v is existed"""
        pass

    @abstractmethod
    def get_neighbors(self, vertex: int) -> List[Tuple[int, float]]:
        """get the neighbors of vertex (vertex, weight)"""
        pass

    @abstractmethod
    def get_degree(self, vertex: int) -> int:
        """get the degree of vertex"""
        pass

    @abstractmethod
    def display(self) -> None:
        """display the graph"""
        pass

    def validate_vertex(self, vertex: int) -> None:
        """validate the vertex is valid"""
        if not (0 <= vertex < self.num_vertices):
            raise ValueError(f"vertex {vertex} out of range [0, {self.num_vertices - 1}]")