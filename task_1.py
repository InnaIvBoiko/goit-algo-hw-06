"""
Task 1: Milan Metro Graph Creation and Analysis

This module creates a graph representation of the Milan Metro system using NetworkX,
and performs basic analysis of key characteristics.
"""

import json
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def load_data():
    """
    Load station and edge data from JSON files.
    
    Returns:
        Tuple containing stations list and edges list from JSON files
    """
    with open('stations.json', 'r', encoding='utf-8') as f:
        stations_data = json.load(f)
    
    with open('edges.json', 'r', encoding='utf-8') as f:
        edges_data = json.load(f)
    
    return stations_data['stations'], edges_data['edges']


def create_metro_graph(stations, edges):
    """
    Create Milan metro graph from stations and edges data.
    
    Args:
        stations: List of station dictionaries with id, name, line, coordinates
        edges: List of edge dictionaries with from, to, line, weight
        
    Returns:
        NetworkX Graph representing the Milan metro system
    """
    # Create undirected graph
    G = nx.Graph()
    
    # Add nodes (stations) with attributes
    for station in stations:
        G.add_node(station['id'], 
                  name=station['name'],
                  line=station['line'],
                  coordinates=station['coordinates'])
    
    # Add edges (connections between stations) with attributes
    for edge in edges:
        G.add_edge(edge['from'], edge['to'],
                  line=edge['line'],
                  weight=edge['weight'])
    
    return G


def get_line_colors():
    """
    Get color mapping for different metro lines.
    
    Returns:
        Dictionary mapping line codes to their corresponding colors
    """
    return {
        'M1': '#e74c3c',      # Red line
        'M2': '#2ecc71',      # Green line 
        'M3': '#f39c12',      # Yellow/Orange line
        'M5': '#9b59b6',      # Purple line
        'M1-M2': '#34495e',   # Dark gray for transfer stations
        'M1-M3': '#34495e',   # Dark gray for transfer stations
        'M1-M5': '#34495e',   # Dark gray for transfer stations
        'M2-M3': '#34495e',   # Dark gray for transfer stations
        'M2-M5': '#34495e',   # Dark gray for transfer stations
        'M3-M5': '#34495e'    # Dark gray for transfer stations
    }


def visualize_graph(G):
    """
    Visualize the Milan metro graph with color-coded metro lines.
    
    Args:
        G: NetworkX graph representing the Milan metro system
    """
    fig = plt.figure(figsize=(16.0, 12.0))
    
    # Get colors for metro lines
    colors = get_line_colors()
    
    # Position nodes based on geographical coordinates
    pos = {}
    for node in G.nodes():
        coords = G.nodes[node]['coordinates']
        pos[node] = (coords[1], coords[0])  # longitude, latitude
    
    # Group edges by metro lines for color mapping
    edge_colors = []
    for _, _, data in G.edges(data=True):
        # Ensure the 'line' value is treated as a string for lookup
        line = str(data.get('line', ''))
        color = colors.get(line, '#95a5a6')
        edge_colors.append(color)
    
    # Group nodes by metro lines for color mapping
    node_colors = []
    for node, data in G.nodes(data=True):
        line = str(data.get('line', ''))
        color = colors.get(line, '#95a5a6')
        node_colors.append(color)
    
    # Draw the graph with colored nodes and edges
    nx.draw(G, pos,
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=80,
            width=1.5,
            with_labels=False,
            alpha=0.8)
    
    # Create legend for metro lines
    legend_elements = [
        mpatches.Patch(color=colors['M1'], label='M1 (Red Line)'),
        mpatches.Patch(color=colors['M2'], label='M2 (Green Line)'),
        mpatches.Patch(color=colors['M3'], label='M3 (Yellow Line)'),
        mpatches.Patch(color=colors['M5'], label='M5 (Purple Line)'),
        mpatches.Patch(color=colors['M1-M2'], label='Transfer Stations')
    ]
    plt.legend(handles=legend_elements, loc='upper left')
    
    plt.title("Milan Metro Network Graph", fontsize=14, fontweight='bold')
    plt.axis('off')
    plt.show()


def analyze_graph_characteristics(G):   
    """
    Analyze basic characteristics of the Milan metro graph.
    
    Args:
        G: NetworkX graph representing the Milan metro system
    """
    print("=" * 50)
    print("MILAN METRO GRAPH ANALYSIS")
    print("=" * 50)
    
    # Basic graph characteristics
    num_nodes = G.number_of_nodes()   
    num_edges = G.number_of_edges()   
    density = nx.density(G)   
    
    print(f"Number of stations (vertices): {num_nodes}")
    print(f"Number of connections (edges): {num_edges}")
    print(f"Graph density: {density:.4f}")
    
    # Check if graph is connected
    is_connected = nx.is_connected(G)   
    print(f"Graph is connected: {is_connected}")
    
    if is_connected:
        # Calculate path characteristics
        avg_path_length = nx.average_shortest_path_length(G)   
        diameter = nx.diameter(G)   
        
        print(f"Average shortest path length: {avg_path_length:.2f}")
        print(f"Graph diameter: {diameter}")
    
    # Degree analysis
    degrees = dict(G.degree())   
    avg_degree = sum(degrees.values()) / len(degrees)   
    max_degree = max(degrees.values())   
    min_degree = min(degrees.values())
    print(f"Average degree: {avg_degree:.2f}")
    print(f"Maximum degree: {max_degree}")
    print(f"Minimum degree: {min_degree}")
    
    # Find nodes with maximum degree
    max_degree_nodes = [node for node, degree in degrees.items() if degree == max_degree]   
    print(f"Stations with highest degree ({max_degree}):")
    for node in max_degree_nodes:   
        station_name = G.nodes[node]['name']   
        print(f"  - {station_name}")
    
    print("=" * 50)


def main():
    """
    Main function for Task 1: Graph creation, visualization and analysis.
    """
    try:
        # Load data from JSON files
        print("Loading data...")
        stations, edges = load_data()
        
        # Create graph
        print("Creating graph...")
        G = create_metro_graph(stations, edges)
        
        # Analyze graph characteristics
        analyze_graph_characteristics(G)
        
        # Visualize graph
        print("Visualizing graph...")
        visualize_graph(G)
        
    except FileNotFoundError as e:
        print(f"Error: File not found - {e}")
    except json.JSONDecodeError as e:
        print(f"Error: Invalid JSON format - {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


if __name__ == "__main__":
    main()
