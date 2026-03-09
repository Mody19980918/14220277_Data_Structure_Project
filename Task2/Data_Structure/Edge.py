from dataclasses import dataclass

@dataclass
class Edge:
    """Data class of Edge"""
    from_vertex: int
    to_vertex: int
    weight: float = 1.0

    def edge_msg(self) -> str:
        if self.weight != 1.0:
            return f"({self.from_vertex} --{self.weight}--> {self.to_vertex})"
        return f"({self.from_vertex} -> {self.to_vertex})"