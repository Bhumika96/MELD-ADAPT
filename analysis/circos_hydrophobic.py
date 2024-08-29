import networkx as nx
import matplotlib.pyplot as plt

# Define the amino acid sequence directly in the script
sequence = "MTYKLILNGKTLKGETTTEAVDAATAEKVFKQYANDNGVDGEWTYDDATKTFTVTE"
L = len(sequence)

first_node = 1
last_node = L

node_labels = {
    first_node: f"        {first_node}",
    last_node: f"         {last_node}"
}

# Define edge colors
color_all = 'lightgrey'
color_matches = "#17AB6F"  # Color for matching pairs
color_no_matches = "#FB6222"  # Color for non-matching pairs
color_true = "#572D86"

# Create a graph
G = nx.Graph(name='Protein Interaction Graph')

# Add nodes
for a in range(1, L + 1):
    G.add_node(a, group='')

# Read data from try_2_dist_hydrophobe_top_cluster.dat (from top cluster pdb) and try_2_dist_hydrophobe_0.dat (from native pdb)
with open('analysis/try_2_dist_hydrophobe_top_cluster.dat', 'r') as predict_file, open('analysis/try_2_dist_hydrophobe_0.dat', 'r') as native_file:
    set_predict = set((int(line.strip().split()[0]), int(line.strip().split()[2])) for line in predict_file)
    set_native = set((int(line.strip().split()[0]), int(line.strip().split()[2])) for line in native_file)

# Determine edge colors based on the sets
for u, v in set_predict:
    if (u, v) in set_native:
        edge_color = color_matches  # Matching pair (green)
    else:
        edge_color = color_no_matches  # Non-matching pair (red)
    G.add_edge(u, v, color=edge_color)

# Add edges from native contacts with color_true
for u, v in set_native:
    if (u, v) not in set_predict:
        G.add_edge(u, v, color=color_true)

# Draw the graph in a circular layout
plt.figure(figsize=(8, 8))
pos = nx.circular_layout(G)  # Positions for all nodes
nx.draw_networkx_nodes(G, pos, node_color='#343741', alpha=1.0, node_size=300)

# Draw edges based on their colors
for color in [color_all, color_matches, color_no_matches, color_true]:
    edges = [(u, v) for u, v, c in G.edges(data='color') if c == color]
    nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=color, width=3, connectionstyle='arc3,rad=0')

# Draw labels for the first and last nodes
nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=18, font_color='black')

plt.tight_layout()
# Hide axis and show the plot
plt.axis('off')
plt.savefig("circos_plot.png", dpi=320)
plt.savefig("circos_plot.pdf", dpi=320)
plt.show()

