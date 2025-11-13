import networkx as nx
from networkx.drawing.nx_pydot import to_pydot

import matplotlib.pyplot as plt

from IPython.display import SVG, display

def visualize_graph_nx(G):
    pos = nx.planar_layout(G)
    
    # Define color mapping for roles
    role_colors = {
        "input": "#90EE90",      # Light green
        "calculation": "#87CEEB", # Sky blue
        "output": "#FFB6C6"       # Light pink
    }
    
    # Get node colors based on their role attribute
    node_colors = [role_colors.get(G.nodes[node].get("role"), "#CCCCCC") for node in G.nodes()]
    
    nx.draw(G, pos, with_labels=True, node_color=node_colors, node_size=1500, font_size=10, font_weight="bold")
    plt.show()

def visualize_graph_dot(
    G, orienation: str="LR", fontsize: int=8, max_node_height: float=0.3, max_node_width: float=0.3
):

    # 2) Map roles to Graphviz styling
    role_styles = {
        "input": {"shape": "circle", "style": "filled", "fillcolor": "#ffffff"},
        "calculation": {"shape": "square", "style": "filled", "fillcolor": "#cfe8ff"},
        "output": {"shape": "hexagon", "style": "filled", "fillcolor": "#54a24b"},
    }

    dot_graph = to_pydot(G)
    dot_graph.set_rankdir(orienation)

    for node in dot_graph.get_nodes():
        name = node.get_name().strip('"')
        if name in {"graph", "node", "edge"}:
            continue
        label = name.replace("_", "\\n")  # wrap on underscores
        node.set_label(label)
        node.set_width(str(max_node_width))
        node.set_height(str(max_node_height))
        node.set_fixedsize("false")  # let it shrink if shorter, but not grow past width
        node.set_fontsize(fontsize)

    for node in dot_graph.get_nodes():
        name = node.get_name().strip('"')
        if name in {"graph", "node", "edge"}:
            continue
        role = G.nodes[name].get("role")
        style = role_styles.get(role)
        if style:
            node.set_shape(style["shape"])
            node.set_style(style["style"])
            node.set_fillcolor(style["fillcolor"])

    display(SVG(dot_graph.create_svg()))