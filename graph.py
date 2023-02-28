""" 
graph.py
Make the graph for the code spaghett.
"""

# Imports
from dataclasses import dataclass

from pyvis.network import Network
# ----------------------------------------------------------------------------


@dataclass
class Node:
    """Class for graph nodes"""
    n_id: str | int
    label: str | int
    level: int
    physics: bool = True
    shape: str = 'ellipse'
    size: int = 25
    title: str
    color: str = 'blue'


@dataclass
class Edge:
    """Class for graph edges"""
    arrow_strikethrough: bool
    from_node: str | int
    hidden: bool = False
    physics: bool = True
    title: str
    to_node: str | int
    value: int
    width: int


def add_node_objects(nodes: list[Node],
                     graph: Network) -> None:
    """Adds list of Node objects to the Network object

    Args:
        nodes (list[Node]): List of Node objects to add
        graph (Network): Network object to add nodes
    """
    for node in nodes:
        graph.add_node(n_id=node.n_id,
                       label=node.label,
                       level=node.level,
                       physics=node.physics,
                       shape=node.shape,
                       size=node.size,
                       title=node.title,
                       color=node.color)


def add_edge_objects(edges: list[Edge],
                     graph: Network) -> None:
    """Adds list of Edge objects to the Network object

    Args:
        edges (list[Node]): List of Edge objects to add
        graph (Network): Network object to add edges
    """
    for edge in edges:
        graph.add_edge(arrowStrikethrough=edge.arrow_strikethrough,
                       from_=edge.from_node,
                       hidden=edge.hidden,
                       physics=edge.physics,
                       title=edge.title,
                       to=edge.to_node,
                       value=edge.value,
                       width=edge.width)


def make_graph(nodes: list[Node],
               edges: list[Edge],
               graph_filename: str = "spaghett.html") -> None:
    """Makes the pyvis html graph file

    Args:
        nodes (list[Node]): List of Nodes for the graph
        edges (list[Edge]): List of Edges for the graph
        graph_filename (str, optional): Filename. Defaults to "spaghett.html".
    """
    # Define the graph
    my_graph = Network(height='1000px',
                       width='75%',
                       directed=True,
                       bgcolor='#6d6d73')

    # Show the buttons for adjusting the graph
    my_graph.show_buttons()

    # Add the nodes and edges
    add_node_objects(nodes, my_graph)
    add_edge_objects(edges, my_graph)

    # Make the html file
    my_graph.show(graph_filename)
