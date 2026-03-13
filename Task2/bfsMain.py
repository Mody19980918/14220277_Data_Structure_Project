from algorithm.dataClass.searchResult import SearchResult
from algorithm.dataClass.searchType import SearchType
from algorithm.graphTraversal import GraphTraversal

def print_step_comparison(bfs_result: SearchResult, dfs_result: SearchResult):
    """
    Compare each step of BFS and DFS side by side
    """
    print("\n" + "="*100)
    print("                    Compare BFS vs DFS Steps")
    print("="*100)
    
    max_steps = max(len(bfs_result.steps), len(dfs_result.steps))
    
    print(f"\n{'Step':<6} | {'BFS (Queue - FIFO)':<45} | {'DFS (Stack - LIFO)':<45}")
    print("-" * 100)
    
    for i in range(max_steps):
        bfs_step = bfs_result.steps[i] if i < len(bfs_result.steps) else None
        dfs_step = dfs_result.steps[i] if i < len(dfs_result.steps) else None
        
        bfs_str = ""
        dfs_str = ""
        
        if bfs_step:
            bfs_str = f"V{bfs_step.current_vertex}, Q{bfs_step.data_structure}"
        
        if dfs_step:
            dfs_str = f"V{dfs_step.current_vertex}, S{dfs_step.data_structure}"
        
        print(f"{i+1:<6} | {bfs_str:<45} | {dfs_str:<45}")
    
    print("-" * 100)
    print(f"{'':6} | Visited Order: {bfs_result.visited_order}  | Visited Order: {dfs_result.visited_order}")
    print("="*100)


def print_detailed_steps(result: SearchResult, title: str):
    """
    Print detailed search steps
    """
    ds_name = "Queue" if result.search_type == SearchType.BFS else "Stack"
    
    print(f"\n{'='*80}")
    print(f"                    {title}")
    print(f"{'='*80}")
    
    print(f"\nStart Vertex: {result.start_vertex}")
    print(f"Final Visited Order: {result.visited_order}")
    print(f"Total Steps: {len(result.steps)}")
    
    print(f"\nDetailed Steps:")
    print("-" * 80)
    
    for step in result.steps:
        print(f"\nStep {step.step_number}:")
        print(f"   Current Vertex: {step.current_vertex}")
        print(f"  {ds_name}: {step.data_structure}")
        print(f"  Visited: {sorted(step.visited)}")
        print(f"  Action: {step.action}")
        if step.neighbors_added:
            print(f"  Added Neighbors: {step.neighbors_added}")
    
    print("=" * 80)


def main():
    """
    BFS and DFS Demo Program
    Show the operation of Queue and Stack, and the difference between them
    """
    
    print("="*100)
    print("                    BFS & DFS Graph Search Algorithm Demo")
    print("="*100)
    
    # Create an example graph
    # 結構:
    #       0
    #      / \
    #     1   2
    #    / \   \
    #   3   4   5
    #      /
    #     6
    
    graph = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1],
        4: [1, 6],
        5: [2],
        6: [4]
    }
    
    print("\n【Graph Structure】")
    print("       0")
    print("      / \\")
    print("     1   2")
    print("    / \\   \\")
    print("   3   4   5")
    print("      /")
    print("     6")
    print()
    
    print("Adjacency List:")
    for vertex, neighbors in graph.items():
        print(f"   Vertex {vertex} -> {neighbors}")
    
    # Create traverser
    traverser = GraphTraversal(graph)
    
    # ==================== BFS 示範 ====================
    print("\n" + "="*100)
    print("                    【BFS Breadth-First Search Detailed Demo】")
    print("="*100)
    
    print("""
    BFS Core Concept:
    ┌──────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Use Queue (FIFO - First In First Out)                                            │
    │  2. Visit the start vertex first, then visit all neighbors (distance 1)              │ 
    │  3. Then visit the neighbors of the neighbors (distance 2), layer by layer expansion │
    │  4. Like a ripple from the center                                                    │
    └──────────────────────────────────────────────────────────────────────────────────────┘
    
    Big O Analysis:
    • Time Complexity: O(V + E) - Each vertex and edge is visited at most once
    • Space Complexity: O(V) - Queue and visited set can store all vertices at most
    """)
    
    bfs_result = traverser.bfs(start_vertex=0)
    print_detailed_steps(bfs_result, "BFS Detailed Steps")
    
    # ==================== DFS Demo ====================
    print("\n" + "="*100)
    print("                    【DFS Depth-First Search Detailed Demo (For reference only)】")
    print("="*100)
    
    print("""
    DFS Core Concept:
    ┌────────────────────────────────────────────────────────────────────────────────────────────────┐
    │  1. Use Stack (LIFO - Last In First Out)                                                       │
    │  2. Start from the start vertex, follow a path "all the way to the end"                        │
    │  3. When you can't continue, "backtrack" to the previous vertex with unvisited neighbors       │
    │  4. Like a maze, first explore a path all the way, then explore other paths                    │
    └────────────────────────────────────────────────────────────────────────────────────────────────┘
    
    Big O Analysis:
    • Time Complexity: O(V + E) - Each vertex and edge is visited at most once
    • Space Complexity: O(V) - Stack and visited set can store all vertices at most
    """)
    
    dfs_result = traverser.dfs(start_vertex=0)
    print_detailed_steps(dfs_result, "DFS Detailed Steps")
    
    # ==================== Step Comparison ====================
    print_step_comparison(bfs_result, dfs_result)
    
    # ==================== Key Differences Summary ====================
    print("\n" + "="*100)
    print("                    【BFS vs DFS Key Differences Summary】")
    print("="*100)
    
    print("""
    ┌───────────────────────┬───────────────────────────────────────────────────────────────────────┬─────────────────────────────────────────────────────────┐
    │     特性              │            BFS                                                        |            DFS                                          │
    ├───────────────────────┼───────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
    │  Data Structure       │  Queue (Queue) - FIFO                                                 │  Stack (Stack) - LIFO                                   │
    ├───────────────────────┼───────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
    │  Visited Order        │  Layer by layer expansion (distance from the start vertex is closer)  │  All the way to the end (first deep, then wide)         │
    ├───────────────────────┼───────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
    │  Time Complexity      │  O(V + E)                                                             │  O(V + E)                                               │
    ├───────────────────────┼───────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
    │  Space Complexity     │  O(V) - Queue store one layer                                         │  O(V) - Stack store one path                            │
    ├───────────────────────┼───────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
    │  Shortest Path        │  ✓ Can find the shortest path (unweighted graph)                      | ✗ Not necessarily the shortest path                     │
    ├───────────────────────┼───────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
    │  Memory Usage         │  More (need to store all nodes in one layer)                          │  Less (only store one path)                             │
    ├───────────────────────┼───────────────────────────────────────────────────────────────────────┼─────────────────────────────────────────────────────────┤
    │  Applicable Scenarios │  Shortest path, level traversal, connectivity                         │  Path search, topological sorting, maze                 │
    └───────────────────────┴───────────────────────────────────────────────────────────────────────┴─────────────────────────────────────────────────────────┘
    
    【Queue vs Stack】
    
    Queue (BFS):
        enqueue → [1, 2, 3] → dequeue
                   ↑     ↑
                rear front
        The first one in (FIFO)
    
    Stack (DFS):
        push → [1, 2, 3] → pop
                      ↑
                    top
        The last one in (LIFO)
    """)
    
    # ==================== 搜尋目標示範 ====================
    print("\n" + "="*100)
    print("                    【Search Specific Target Demo】")
    print("="*100)
    
    target = 6
    print(f"\nSearch Target: Vertex {target}")
    
    bfs_target = traverser.bfs(start_vertex=0, target_vertex=target)
    dfs_target = traverser.dfs(start_vertex=0, target_vertex=target)
    
    print(f"\nBFS found the target path length: {len(bfs_target.visited_order)} steps")
    print(f"BFS visited order: {bfs_target.visited_order}")
    print(f"BFS total steps: {len(bfs_target.steps)}")
    
    print(f"\nDFS found the target path length: {len(dfs_target.visited_order)} steps")
    print(f"DFS visited order: {dfs_target.visited_order}")
    print(f"DFS total steps: {len(dfs_target.steps)}")
    
    print("\n" + "="*100)
    print("                    Demo Complete - Demo End")
    print("="*100)

if __name__ == "__main__":
    main()