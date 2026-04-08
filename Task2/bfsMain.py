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
            bfs_vertex = bfs_step.current_vertex + 1  # Convert to 1-indexed for display
            bfs_queue = [v + 1 for v in bfs_step.data_structure]
            bfs_str = f"V{bfs_vertex}, Q{bfs_queue}"

        if dfs_step:
            dfs_vertex = dfs_step.current_vertex + 1  # Convert to 1-indexed for display
            dfs_stack = [v + 1 for v in dfs_step.data_structure]
            dfs_str = f"V{dfs_vertex}, S{dfs_stack}"

        print(f"{i+1:<6} | {bfs_str:<45} | {dfs_str:<45}")

    # Convert visited order to 1-indexed for display
    bfs_visited = [v + 1 for v in bfs_result.visited_order]
    dfs_visited = [v + 1 for v in dfs_result.visited_order]
    print("-" * 100)
    print(f"{'':6} | Visited Order: {bfs_visited}  | Visited Order: {dfs_visited}")
    print("="*100)


def print_detailed_steps(result: SearchResult, title: str):
    """
    Print detailed search steps
    """
    ds_name = "Queue" if result.search_type == SearchType.BFS else "Stack"

    print(f"\n{'='*80}")
    print(f"                    {title}")
    print(f"{'='*80}")

    # Convert to 1-indexed for display
    start_vertex = result.start_vertex + 1
    visited_order = [v + 1 for v in result.visited_order]

    print(f"\nStart Vertex: {start_vertex}")
    print(f"Final Visited Order: {visited_order}")
    print(f"Total Steps: {len(result.steps)}")

    print(f"\nDetailed Steps:")
    print("-" * 80)

    for step in result.steps:
        # Convert to 1-indexed for display
        current_vertex = step.current_vertex + 1
        visited = [v + 1 for v in step.visited]
        data_structure = [v + 1 for v in step.data_structure]
        neighbors_added = [v + 1 for v in step.neighbors_added]

        print(f"\nStep {step.step_number}:")
        print(f"   Current Vertex: {current_vertex}")
        print(f"  {ds_name}: {data_structure}")
        print(f"  Visited: {sorted(visited)}")
        print(f"  Action: {step.action}")
        if neighbors_added:
            print(f"  Added Neighbors: {neighbors_added}")

    print("=" * 80)


def main():
    """
    BFS and DFS Demo Program
    Show the operation of Queue and Stack, and the difference between them
    """

    print("="*100)
    print("                    BFS & DFS Graph Search Algorithm Demo")
    print("="*100)

    # Create an example graph (Tree Structure)
    # Structure:
    #       1
    #      / \
    #     2   3
    #    / \  | \
    #   4   5 6   7
    #
    # Using 0-indexed for internal representation (1->0, 2->1, 3->2, etc.)
    # BFS: 1 -> 2 -> 3 -> 4 -> 5 -> 6 -> 7 (0 -> 1 -> 2 -> 3 -> 4 -> 5 -> 6)
    # DFS: 1 -> 2 -> 4 -> 5 -> 3 -> 6 -> 7 (0 -> 1 -> 3 -> 4 -> 2 -> 5 -> 6)

    graph = {
        0: [1, 2],      # 1 -> 2, 3
        1: [3, 4],      # 2 -> 4, 5
        2: [5, 6],      # 3 -> 6, 7
        3: [],          # 4 (leaf)
        4: [],          # 5 (leaf)
        5: [],          # 6 (leaf)
        6: []           # 7 (leaf)
    }

    print("\n【Graph Structure】")
    print("       1")
    print("      / \\")
    print("     2   3")
    print("    / \\  | \\")
    print("   4   5 6   7")
    print()

    print("Adjacency List:")
    for vertex, neighbors in graph.items():
        display_vertex = vertex + 1  # Convert 0-indexed to 1-indexed for display
        display_neighbors = [n + 1 for n in neighbors]  # Convert neighbors to 1-indexed
        print(f"   Vertex {display_vertex} -> {display_neighbors}")

    # Create traverser
    traverser = GraphTraversal(graph)

    # ==================== BFS Demo ====================
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
    │  4. Like a maze, first explore a path all the way, then explore other paths                      │
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
    │  Shortest Path        │  [v] Can find the shortest path (unweighted graph)                    | [x] Not necessarily the shortest path                   │
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

    # ==================== Search Target Demo ====================
    print("\n" + "="*100)
    print("                    【Search Specific Target Demo】")
    print("="*100)

    target = 6  # Looking for node 7 (index 6)
    print(f"\nSearch Target: Vertex {target}")

    bfs_target = traverser.bfs(start_vertex=0, target_vertex=target)
    dfs_target = traverser.dfs(start_vertex=0, target_vertex=target)

    # Convert visited order to 1-indexed for display
    bfs_visited = [v + 1 for v in bfs_target.visited_order]
    dfs_visited = [v + 1 for v in dfs_target.visited_order]

    print(f"\nBFS found the target path length: {len(bfs_target.visited_order)} steps")
    print(f"BFS visited order: {bfs_visited}")
    print(f"BFS total steps: {len(bfs_target.steps)}")

    print(f"\nDFS found the target path length: {len(dfs_target.visited_order)} steps")
    print(f"DFS visited order: {dfs_visited}")
    print(f"DFS total steps: {len(dfs_target.steps)}")

    print("\n" + "="*100)
    print("                    Demo Complete - Demo End")
    print("="*100)

if __name__ == "__main__":
    main()
