import networkx as nx
import matplotlib.pyplot as plt

# Create a directed graph
G = nx.DiGraph()

# Add nodes to the graph
G.add_node((8, 0, 0))

# Define the movement rules
rules = {
    "left": lambda x1, x2, x3: (x1 - 1, x2, x3 + 1),
    "up": lambda x1, x2, x3: (x1 - 1, x2 + 1, x3),
    "right_up": lambda x1, x2, x3: (x1 - 1, x2 + 1, x3 + 1)
}

# Function to apply movement rules and add edges to the graph
def add_edges(node):
    x1, x2, x3 = node
    for rule in rules.values():
        new_node = rule(x1, x2, x3)
        G.add_edge(node, new_node)
        add_edges(new_node)

# Start from (8, 0, 0)
start_node = (8, 0, 0)

# Build the graph
add_edges(start_node)

# Draw the graph
pos = nx.spring_layout(G, seed=42)
labels = {node: f"{node[0]}\n{node[1]}\n{node[2]}" for node in G.nodes}
nx.draw_networkx(G, pos=pos, with_labels=True, labels=labels, node_size=500, font_size=10)

# Set the axis labels
plt.xlabel('x3')
plt.ylabel('x2')
plt.title('2D Diagonal Grid')

# Show the plot
plt.show()
