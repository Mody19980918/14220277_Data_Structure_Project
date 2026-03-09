from Data_Structure.GraphADT import GraphADT
from Data_Structure.GraphType.GraphType import GraphType
from typing import Optional, List, Tuple
from Data_Structure.Edge import Edge

DIVIDER = "="*50

class AdjacencyMatrixGraph(GraphADT):
    """
    This is about adjacency matrix implementation of graph,
    use two-dimensional list to store the weight of the edge, 0 means no edge
    Adjacency matrix format :
    matrix[i][j] = weight
    Example : 
    matrix = [
        [0.0, 1.0, 2.0],
        [1.0, 0.0, 1.0],
        [2.0, 1.0, 0.0],
    ]
    """

    def __init__(self, num_vertices: int, graph_type: GraphType = GraphType.UNDIRECTED):
        super().__init__(num_vertices, graph_type)
        self.matrix: List[List[float]] = [
            [0.0] * num_vertices for _ in range(num_vertices)
        ]

    def add_edge(self, u: int, v: int, weight: float = 1.0) -> None:
        """add edge to adjacency matrix"""
        self.validate_vertex(u)
        self.validate_vertex(v)

        if u == v:
            raise ValueError("self-loop is not allowed")

        self.matrix[u][v] = weight

        # undirected graph needs to add bidirectional
        if self.graph_type == GraphType.UNDIRECTED:
            self.matrix[v][u] = weight

    def remove_edge(self, u: int, v: int) -> None:
        """remove edge from adjacency matrix"""
        self.validate_vertex(u)
        self.validate_vertex(v)

        self.matrix[u][v] = 0.0

        # undirected graph needs to remove bidirectional
        if self.graph_type == GraphType.UNDIRECTED:
            self.matrix[v][u] = 0.0

    def has_edge(self, u: int, v: int) -> bool:
        """check if edge exists"""
        self.validate_vertex(u)
        self.validate_vertex(v)
        return self.matrix[u][v] != 0.0

    def get_edge_weight(self, u: int, v: int) -> Optional[float]:
        """get the weight of the edge, return None if no edge"""
        self.validate_vertex(u)
        self.validate_vertex(v)
        weight = self.matrix[u][v]
        return weight if weight != 0.0 else None

    def get_neighbors(self, vertex: int) -> List[Tuple[int, float]]:
        """get the neighbors of the vertex"""
        self.validate_vertex(vertex)
        return [
            (v, self.matrix[vertex][v])
            for v in range(self.num_vertices)
            if self.matrix[vertex][v] != 0.0
        ]

    def get_degree(self, vertex: int) -> int:
        """get the degree of the vertex"""
        self.validate_vertex(vertex)

        if self.graph_type == GraphType.UNDIRECTED:
            return sum(1 for w in self.matrix[vertex] if w != 0.0)
        else:
            # directed graph: out degree + in degree
            out_degree = sum(1 for w in self.matrix[vertex] if w != 0.0)
            in_degree = sum(1 for i in range(self.num_vertices) if self.matrix[i][vertex] != 0.0)
            return out_degree + in_degree

    def get_out_degree(self, vertex: int) -> int:
        """get the out degree of the vertex"""
        self.validate_vertex(vertex)
        return sum(1 for w in self.matrix[vertex] if w != 0.0)

    def get_in_degree(self, vertex: int) -> int:
        """get the in degree of the vertex"""
        self.validate_vertex(vertex)
        return sum(1 for i in range(self.num_vertices) if self.matrix[i][vertex] != 0.0)

    def display(self) -> None:
        """display the adjacency matrix"""
        print(f"\n{DIVIDER}")
        print(f"adjacency matrix graph ({self.graph_type.value})")
        print(f"number of vertices: {self.num_vertices}")
        print(f"{DIVIDER}")

        # print the header
        header = "    " + " ".join(f"{i:4}" for i in range(self.num_vertices))
        print(header)
        print("     " + "-" * (5 * self.num_vertices))

        # print the matrix content
        for i in range(self.num_vertices):
            row = f"{i:3} |"
            for j in range(self.num_vertices):
                val = self.matrix[i][j]
                if val == 0.0:
                    row += "   ."
                elif val == int(val):
                    row += f"{int(val):4}"
                else:
                    row += f"{val:4.1f}"
            print(row)

    def get_all_edges(self) -> List[Edge]:
        """Return all edges in the graph."""
        edges: List[Edge] = []

        if self.graph_type == GraphType.UNDIRECTED:
            for u in range(self.num_vertices):
                for v in range(u + 1, self.num_vertices):
                    weight = self.matrix[u][v]
                    if weight != 0.0:
                        edges.append(Edge(u, v, weight))
        else:
            for u in range(self.num_vertices):
                for v in range(self.num_vertices):
                    weight = self.matrix[u][v]
                    if weight != 0.0:
                        edges.append(Edge(u, v, weight))

        return edges