"""
Task 3: Dijkstra's Algorithm for Shortest Paths in Milan Metro Graph

This module implements Dijkstra's algorithm to find the shortest weighted paths 
in the Milan Metro system graph created in Task 1.
"""

import networkx as nx
from task_1 import load_data, create_metro_graph
from task_2 import get_station_name


def dijkstra(graph, start):
    """
    Dijkstra's algorithm implementation for finding shortest paths from start vertex.
    
    Args:
        graph: NetworkX graph with weighted edges
        start: Starting vertex ID
        
    Returns:
        Dictionary with shortest distances from start to all other vertices
    """
    # Initialize distances and unvisited vertices set
    distances = {vertex: float('infinity') for vertex in graph.nodes()}
    distances[start] = 0
    unvisited = list(graph.nodes())

    while unvisited:
        # Find vertex with minimum distance among unvisited
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])

        # If current distance is infinity, we're done
        if distances[current_vertex] == float('infinity'):
            break

        # Check all neighbors of current vertex
        for neighbor in graph.neighbors(current_vertex):
            if neighbor in unvisited:
                # Get edge weight
                weight = graph[current_vertex][neighbor]['weight']
                distance = distances[current_vertex] + weight

                # If new distance is shorter, update shortest path
                if distance < distances[neighbor]:
                    distances[neighbor] = distance

        # Remove current vertex from unvisited set
        unvisited.remove(current_vertex)

    return distances


def dijkstra_path(graph, start, end):
    """
    Find shortest path between two vertices using Dijkstra's algorithm.
    
    Args:
        graph: NetworkX graph with weighted edges
        start: Starting vertex ID
        end: Target vertex ID
        
    Returns:
        Tuple containing (shortest_distance, path_list)
    """
    # Initialize distances, previous vertices, and unvisited set
    distances = {vertex: float('infinity') for vertex in graph.nodes()}
    previous = {vertex: None for vertex in graph.nodes()}
    distances[start] = 0
    unvisited = list(graph.nodes())

    while unvisited:
        # Find vertex with minimum distance among unvisited
        current_vertex = min(unvisited, key=lambda vertex: distances[vertex])

        # If we reached the target or distance is infinity
        if current_vertex == end or distances[current_vertex] == float('infinity'):
            break

        # Check all neighbors of current vertex
        for neighbor in graph.neighbors(current_vertex):
            if neighbor in unvisited:
                # Get edge weight
                weight = graph[current_vertex][neighbor]['weight']
                distance = distances[current_vertex] + weight

                # If new distance is shorter, update shortest path
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous[neighbor] = current_vertex

        # Remove current vertex from unvisited set
        unvisited.remove(current_vertex)

    # Reconstruct path
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()

    # Return distance and path (empty path if no route found)
    if distances[end] == float('infinity'):
        return float('infinity'), []
    else:
        return distances[end], path


def print_shortest_path(graph, start, end, distance, path):
    """
    Print detailed information about the shortest path found by Dijkstra.
    
    Args:
        graph: NetworkX graph
        start: Starting station ID
        end: Target station ID
        distance: Shortest distance (weighted)
        path: List of station IDs in the shortest path
    """
    start_name = get_station_name(graph, start)
    end_name = get_station_name(graph, end)
    
    print(f"\nSHORTEST PATH: {start_name} -> {end_name}")
    print(f"Total distance (travel time): {distance:.2f} minutes")
    print(f"Number of stations: {len(path)}")
    print("Route:")
    
    if not path:
        print("  No path found")
        return
    
    for i, station_id in enumerate(path):
        station_name = get_station_name(graph, station_id)
        if i == 0:
            print(f"  Start: {station_name}")
        elif i == len(path) - 1:
            print(f"  End: {station_name}")
        else:
            print(f"  {i}: {station_name}")


def analyze_station_distances(graph, station_id, closest_count=10, farthest_count=5):
    """
    Analyze distances from a given station to all other stations.
    
    Args:
        graph: NetworkX graph with weighted edges
        station_id: ID of the station to analyze from
        closest_count: Number of closest stations to display
        farthest_count: Number of farthest stations to display
    """
    station_name = get_station_name(graph, station_id)
    
    print(f"DISTANCES FROM {station_name.upper()} TO ALL STATIONS:")
    print("-" * 50)
    
    distances = dijkstra(graph, station_id)
    sorted_distances = sorted(distances.items(), key=lambda x: x[1])
    
    # Show closest stations (excluding the starting station itself)
    print("CLOSEST STATIONS:")
    closest_stations = [item for item in sorted_distances if item[1] > 0][:closest_count]
    for station_id, distance in closest_stations:
        station_name = get_station_name(graph, station_id)
        print(f"  {station_name}: {distance:.2f} minutes")
    
    # Show farthest stations
    print("\nFARTHEST STATIONS:")
    for station_id, distance in sorted_distances[-farthest_count:]:
        station_name = get_station_name(graph, station_id)
        print(f"  {station_name}: {distance:.2f} minutes")


def analyze_shortest_paths(graph):
    """
    Analyze shortest paths from several key stations in the metro system.
    
    Args:
        graph: NetworkX graph with weighted edges
    """
    print("=" * 70)
    print("DIJKSTRA'S ALGORITHM - SHORTEST WEIGHTED PATHS ANALYSIS")
    print("=" * 70)
    
    # Test shortest paths between key stations (same as Task 2 for consistency)
    test_pairs = [
        (1, 20),   # Rho Fiera to Inganni
        (1, 50),   # Rho Fiera to Centrale  
        (1, 90),   # Rho Fiera to Sant'Agostino
        (25, 75),  # Duomo to Ponale
    ]
    
    for start_id, end_id in test_pairs:
        distance, path = dijkstra_path(graph, start_id, end_id)
        print_shortest_path(graph, start_id, end_id, distance, path)
        print()
    
    # Analyze distances from key transportation hubs
    key_stations = [
        (22, "Central interchange hub M1/M2"),  # Cadorna
        (71, "Terminal station M3"),            # Affori FN
    ]
    
    for station_id, description in key_stations:
        analyze_station_distances(graph, station_id)
        print()

def main():
    """
    Main function for Task 3: Dijkstra's algorithm implementation and analysis.
    """
    try:
        # Load data and create graph
        print("Loading Milan Metro data...")
        stations, edges = load_data()
        G = create_metro_graph(stations, edges)
        
        print(f"Graph loaded: {G.number_of_nodes()} stations, {G.number_of_edges()} connections")
        print(f"Graph has weighted edges: {nx.is_weighted(G)}")
        
        # Verify edge weights
        sample_edges = list(G.edges(data=True))[:3]
        print("\nSample edge weights:")
        
        # Calculate weight statistics
        weights = [data['weight'] for u, v, data in G.edges(data=True)]
        min_weight = min(weights)
        max_weight = max(weights)
        avg_weight = sum(weights) / len(weights)
        
        print(f"Minimum weight: {min_weight} minutes")
        print(f"Maximum weight: {max_weight} minutes")
        print(f"Average weight: {avg_weight:.2f} minutes")
        print()
        
        for u, v, data in sample_edges:
            u_name = get_station_name(G, u)
            v_name = get_station_name(G, v)
            weight = data['weight']
            print(f"  {u_name} -- {v_name}: {weight} minutes")
        
        
        # Run Dijkstra's algorithm analysis
        analyze_shortest_paths(G)
        
    except FileNotFoundError as e:
        print(f"Error: Required data files not found - {e}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
