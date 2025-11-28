"""
Task 2: DFS and BFS Path Finding in Milan Metro Graph

This module implements Depth-First Search (DFS) and Breadth-First Search (BFS) 
algorithms to find paths in the Milan Metro system graph created in Task 1.
"""

import networkx as nx
from collections import deque
from task_1 import load_data, create_metro_graph


def dfs_path(graph, start, goal, path=None):
    """
    Depth-First Search algorithm to find a path between two nodes.
    
    Args:
        graph: NetworkX graph
        start: Starting node ID
        goal: Target node ID
        path: Current path (used for recursion)
        
    Returns:
        List representing the path from start to goal, or None if no path exists
    """
    if path is None:
        path = []
    
    # Add current node to path
    path = path + [start]
    
    # If we reached the goal, return the path
    if start == goal:
        return path
    
    # Explore neighbors
    for neighbor in graph.neighbors(start):
        if neighbor not in path:  # Avoid cycles
            new_path = dfs_path(graph, neighbor, goal, path)
            if new_path:
                return new_path
    
    return None


def bfs_path(graph, start, goal):
    """
    Breadth-First Search algorithm to find a path between two nodes.
    
    Args:
        graph: NetworkX graph
        start: Starting node ID
        goal: Target node ID
        
    Returns:
        List representing the path from start to goal, or None if no path exists
    """
    if start == goal:
        return [start]
    
    # Queue for BFS: each element is (current_node, path_to_current_node)
    queue = deque([(start, [start])])
    visited = {start}
    
    while queue:
        current_node, path = queue.popleft()
        
        # Explore neighbors
        for neighbor in graph.neighbors(current_node):
            if neighbor not in visited:
                new_path = path + [neighbor]
                
                # If we found the goal, return the path
                if neighbor == goal:
                    return new_path
                
                # Add to queue for further exploration
                queue.append((neighbor, new_path))
                visited.add(neighbor)
    
    return None


def get_station_name(graph, station_id):
    """
    Get station name by ID.
    
    Args:
        graph: NetworkX graph
        station_id: Station ID
        
    Returns:
        Station name string
    """
    return graph.nodes[station_id]['name']


def print_path_details(graph, path, algorithm_name):
    """
    Print detailed information about the found path.
    
    Args:
        graph: NetworkX graph
        path: List of station IDs representing the path
        algorithm_name: Name of the algorithm used (DFS or BFS)
    """
    if not path:
        print(f"{algorithm_name}: No path found")
        return
    
    print(f"\n{algorithm_name} Path:")
    print(f"Length: {len(path)} stations")
    print("Route:")
    
    for i, station_id in enumerate(path):
        station_name = get_station_name(graph, station_id)
        if i == 0:
            print(f"  Start: {station_name}")
        elif i == len(path) - 1:
            print(f"  End: {station_name}")
        else:
            print(f"  {i}: {station_name}")


def compare_algorithms(graph, start_station, end_station):
    """
    Compare DFS and BFS algorithms for finding paths between two stations.
    
    Args:
        graph: NetworkX graph
        start_station: Starting station ID
        end_station: Target station ID
    """
    start_name = get_station_name(graph, start_station)
    end_name = get_station_name(graph, end_station)
    
    print("=" * 70)
    print(f"PATHFINDING COMPARISON: {start_name} -> {end_name}")
    print("=" * 70)
    
    # Find paths using both algorithms
    dfs_result = dfs_path(graph, start_station, end_station)
    bfs_result = bfs_path(graph, start_station, end_station)
    
    # Print results
    print_path_details(graph, dfs_result, "DFS")
    print_path_details(graph, bfs_result, "BFS")
    
    # Compare results
    print(f"\nCOMPARISON:")
    if dfs_result and bfs_result:
        print(f"DFS path length: {len(dfs_result)} stations")
        print(f"BFS path length: {len(bfs_result)} stations")
        
        if len(dfs_result) == len(bfs_result):
            print("Both algorithms found paths of equal length")
        elif len(dfs_result) < len(bfs_result):
            print("DFS found a shorter path")
        else:
            print("BFS found a shorter path (optimal)")
            
        if dfs_result == bfs_result:
            print("Both algorithms found the same path")
        else:
            print("Algorithms found different paths")
    else:
        print("One or both algorithms failed to find a path")


def main():
    """
    Main function for Task 2: DFS and BFS pathfinding comparison.
    """
    try:
        # Load data and create graph using functions from task_1
        print("Loading Milan Metro data...")
        stations, edges = load_data()
        G = create_metro_graph(stations, edges)
        
        print(f"Graph loaded: {G.number_of_nodes()} stations, {G.number_of_edges()} connections")
        
        # Test cases for pathfinding comparison
        test_cases = [
            (1, 20),   # Short distance path
            (1, 50),   # Medium distance path  
            (1, 90),   # Long distance path
            (25, 75),  # Cross-network path
        ]
        
        # Run comparisons for each test case
        for start, end in test_cases:
            compare_algorithms(G, start, end)
            print()
        
    except FileNotFoundError as e:
        print(f"Error: Required data files not found - {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
