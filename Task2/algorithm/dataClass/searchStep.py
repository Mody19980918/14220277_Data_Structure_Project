from dataclasses import dataclass
from typing import List, Set

@dataclass
class SearchStep:
    """
    Search Step Data Class
    """
    step_number: int
    current_vertex: int
    data_structure: List[int]  # Queue (BFS) or Stack (DFS)
    visited: Set[int]
    action: str  
    neighbors_added: List[int] 
