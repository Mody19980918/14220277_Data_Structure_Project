from dataclasses import dataclass
from typing import List
from algorithm.dataClass.searchStep import SearchStep
from algorithm.dataClass.searchType import SearchType

@dataclass
class SearchResult:
    """Search Result Data Class"""
    search_type: SearchType
    start_vertex: int
    visited_order: List[int]  
    steps: List[SearchStep] 
    path_found: bool  