import networkx as nx
import matplotlib.pyplot as plt

# Define the amino acid sequence directly in the script
sequence = "MTYKLILNGKTLKGETTTEAVDAATAEKVFKQYANDNGVDGEWTYDDATKTFTVTE"
L = len(sequence)

first_node= 1
last_node = L

node_labels = {
        first_node: f"        {first_node}",
        last_node: f"         {last_node}"
    }

# Define edge colors
edge_colors = ["lightgrey", "#572D86"]

# Create a graph
G = nx.Graph(name='Protein Interaction Graph')

# Add nodes
for a in range(1, L + 1):
  G.add_node(a, group='')

# Add edges from 4_satisfied.dat with black color
with open('hydrophobe_2.dat', 'r') as satisfied_file:
  for line in satisfied_file:
    line = line.strip().split()
    G.add_edge(int(line[0]), int(line[2]), color=edge_colors[0])

# Add edges from n2.dat with red color
with open('analysis/try_2_dist_hydrophobe_0.dat', 'r') as native_file:
#with open('native.dat', 'r') as native_file:
  for line in native_file:
    line = line.strip().split()
    G.add_edge(int(line[0]), int(line[2]), color=edge_colors[1])

# Draw the graph in a circular layout
plt.figure(figsize=(8, 8))
pos = nx.circular_layout(G) # Positions for all nodes
nx.draw_networkx_nodes(G, pos, node_color='#343741', node_size=300)
#nx.draw_networkx_labels(G, pos, font_size=8)

# Draw edges with colors
for color in edge_colors:
  edges = [(u, v) for u, v, c in G.edges(data='color') if c == color]
  #nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=color, width=2, connectionstyle='arc3,rad=0', label=f'Edges from {color} data')
  nx.draw_networkx_edges(G, pos, edgelist=edges, edge_color=color, width=4, connectionstyle='arc3,rad=0')

nx.draw_networkx_labels(G, pos, labels=node_labels, font_size=18, font_color='black')

#plt.title('Protein Interaction Graph (Circular Layout)')
plt.axis('off')
plt.tight_layout()
#plt.legend()
plt.savefig("circos_native.png", dpi=320)
plt.savefig("circos_native.pdf", dpi=320)
plt.show()
