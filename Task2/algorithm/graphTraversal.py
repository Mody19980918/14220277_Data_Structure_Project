from typing import Dict, List, Optional, Set
from algorithm.dataStructure.queue import Queue
from algorithm.dataStructure.stack import Stack
from algorithm.dataClass.searchResult import SearchResult
from algorithm.dataClass.searchStep import SearchStep
from algorithm.dataClass.searchType import SearchType

class GraphTraversal:
    """
    Implementation of BFS and DFS
    """
    
    def __init__(self, adjacency_list: Dict[int, List[int]]):
        """
        Initialize the graph traversal
        
        Args:
            adjacency_list: adjacency list, e.g. {0: [1, 2], 1: [0, 3], ...}
        """
        self.adjacency_list = adjacency_list
        self.num_vertices = len(adjacency_list)
    
    def bfs(self, start_vertex: int, target_vertex: Optional[int] = None) -> SearchResult:
        """
        ============================================================================
                                BFS (Breadth-First Search)
        ============================================================================
        
        【Core Idea】
        - Start from the start vertex, visit all "direct neighbors" (distance 1)
        - Then visit "neighbors of neighbors" (distance 2)
        - Expand layer by layer, like a ripple spreading outward
        
        【Data Structure Used】
        - Queue (Queue) - FIFO：Ensure the first discovered vertex is processed first
        
        【Big O Time Complexity Analysis】
        - Each vertex is visited at most once: O(V)
        - Each edge is checked at most once: O(E)
        - Total time complexity: O(V + E)
        
        【Big O Space Complexity Analysis】
        - visited set: O(V)
        - Queue stores one layer of nodes: O(V) worst case
        - Total space complexity: O(V)
        
        【Applicable Scenarios】
        - Shortest path (unweighted graph)
        - Level traversal
        - Connectivity detection
        ============================================================================
        """
        
        if start_vertex not in self.adjacency_list:
            raise ValueError(f"Start vertex {start_vertex} is not in the graph")
        
        # Initialize
        visited: Set[int] = set()
        queue = Queue()
        visited_order: List[int] = []
        steps: List[SearchStep] = []
        step_count = 0
        path_found = False
        
        # Step 0: start vertex is enqueued
        queue.enqueue(start_vertex)
        
        step_count += 1
        steps.append(SearchStep(
            step_number=step_count,
            current_vertex=start_vertex,
            data_structure=queue.to_list(),
            visited=set(visited),
            action=f"Initialize: start vertex {start_vertex} is enqueued",
            neighbors_added=[start_vertex]
        ))
        
        # BFS main loop
        while not queue.is_empty():
            # 1. dequeue the vertex from the front of the queue
            current = queue.dequeue()
            
            # 2. if the vertex is visited, skip
            if current in visited:
                continue
            
            # 3. mark as visited and record the order
            visited.add(current)
            visited_order.append(current)
            
            step_count += 1
            
            # check if the target is found
            if target_vertex is not None and current == target_vertex:
                path_found = True
                steps.append(SearchStep(
                    step_number=step_count,
                    current_vertex=current,
                    data_structure=queue.to_list(),
                    visited=set(visited),
                    action=f"Found target {target_vertex}! BFS ends",
                    neighbors_added=[]
                ))
                break
            
            # 4. enqueue the unvisited neighbors
            neighbors_added = []
            for neighbor in self.adjacency_list.get(current, []):
                if neighbor not in visited and neighbor not in queue.to_list():
                    queue.enqueue(neighbor)
                    neighbors_added.append(neighbor)
            
            # record this step
            action_desc = f"Visit vertex {current}"
            if neighbors_added:
                action_desc += f"，neighbors {neighbors_added} are enqueued"
            else:
                action_desc += "，no new neighbors can be enqueued"
            
            steps.append(SearchStep(
                step_number=step_count,
                current_vertex=current,
                data_structure=queue.to_list(),
                visited=set(visited),
                action=action_desc,
                neighbors_added=neighbors_added
            ))
        
        return SearchResult(
            search_type=SearchType.BFS,
            start_vertex=start_vertex,
            visited_order=visited_order,
            steps=steps,
            path_found=path_found
        )
    
    def dfs(self, start_vertex: int, target_vertex: Optional[int] = None) -> SearchResult:
        """
        ============================================================================
                                DFS (Depth-First Search)
        ============================================================================
        
       【Core Idea】
        - Start from the start vertex, follow a path "all the way to the end"
        - When you can't continue, "backtrack" to the previous vertex with unvisited neighbors
        - Repeat until all vertices are visited
        
       【Data Structure Used】
        - Stack - LIFO：Ensure the last discovered vertex is processed first
        
        【Big O Time Complexity Analysis】
        - Each vertex is visited at most once: O(V)
        - Each edge is checked at most once: O(E)
        - Total time complexity: O(V + E)
        
        【Big O Space Complexity Analysis】
        - visited set: O(V)
        - Stack worst case (chain graph): O(V)
        - Total space complexity: O(V)
        
        【Applicable Scenarios】
        - Path search
        - Topological sorting
        - Cycle detection
        - Maze solving
        ============================================================================
        """
        
        if start_vertex not in self.adjacency_list:
            raise ValueError(f"Start vertex {start_vertex} is not in the graph")
        
        # Initialize
        visited: Set[int] = set()
        stack = Stack()
        visited_order: List[int] = []
        steps: List[SearchStep] = []
        step_count = 0
        path_found = False
        
        # Step 0: start vertex is pushed
        stack.push(start_vertex)
        
        step_count += 1
        steps.append(SearchStep(
            step_number=step_count,
            current_vertex=start_vertex,
            data_structure=stack.to_list(),
            visited=set(visited),
            action=f"Initialize: start vertex {start_vertex} is pushed",
            neighbors_added=[start_vertex]
        ))
        
        # DFS main loop
        while not stack.is_empty():
            # 1. pop the vertex from the top of the stack (this is the biggest difference from BFS!)
            current = stack.pop()
            
            # 2. if the vertex is visited, skip
            if current in visited:
                continue
            
            # 3. mark as visited and record the order
            visited.add(current)
            visited_order.append(current)
            
            step_count += 1
            
            # check if the target is found
            if target_vertex is not None and current == target_vertex:
                path_found = True
                steps.append(SearchStep(
                    step_number=step_count,
                    current_vertex=current,
                    data_structure=stack.to_list(),
                    visited=set(visited),
                    action=f"Found target {target_vertex}! DFS ends",
                    neighbors_added=[]
                ))
                break
            
            # 4. push the unvisited neighbors to the top of the stack 
            # To maintain a specific order, we reverse the neighbor list
            neighbors_added = []
            neighbors = self.adjacency_list.get(current, [])
            
            # Reverse the neighbor order, so the first neighbor will be processed last (at the top of the stack)
            for neighbor in reversed(neighbors):
                if neighbor not in visited:
                    stack.push(neighbor)
                    neighbors_added.insert(0, neighbor)  # maintain the original order for display
            
            # record this step
            action_desc = f"Visit vertex {current}"
            if neighbors_added:
                action_desc += f"，neighbors {neighbors_added} are pushed (LIFO)"
            else:
                action_desc += "，no new neighbors can be pushed, prepare to backtrack"
            
            steps.append(SearchStep(
                step_number=step_count,
                current_vertex=current,
                data_structure=stack.to_list(),
                visited=set(visited),
                action=action_desc,
                neighbors_added=neighbors_added
            ))
        
        return SearchResult(
            search_type=SearchType.DFS,
            start_vertex=start_vertex,
            visited_order=visited_order,
            steps=steps,
            path_found=path_found
        )