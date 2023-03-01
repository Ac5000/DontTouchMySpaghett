""" 
graph.py
Make the graph for the code spaghett.
"""

# Imports
from dataclasses import dataclass

from pyvis.network import Network
# ----------------------------------------------------------------------------


@dataclass(frozen=True, order=True)
class Node:
    """Class for graph nodes"""
    n_id: str | int
    label: str | int
    title: str
    level: int = 1
    physics: bool = True
    shape: str = 'dot'
    size: int = 25
    color: str = 'blue'


@dataclass(order=True)
class Edge:
    """Class for graph edges"""
    from_node: str | int
    title: str
    to_node: str | int
    # value: int
    width: int = 1
    arrow_strikethrough: bool = True
    hidden: bool = False
    physics: bool = True


def add_node_objects(nodes: list[Node],
                     graph: Network) -> None:
    """Adds list of Node objects to the Network object

    Args:
        nodes (list[Node]): List of Node objects to add
        graph (Network): Network object to add nodes
    """
    for node in nodes:
        try:
            graph.add_node(n_id=node.n_id,
                           label=node.label,
                           level=node.level,
                           physics=node.physics,
                           shape=node.shape,
                           size=node.size,
                           title=node.title,
                           color=node.color)
        except AssertionError:
            print(f'Can not add node: {node}')


def add_edge_objects(edges: list[Edge],
                     graph: Network) -> None:
    """Adds list of Edge objects to the Network object

    Args:
        edges (list[Node]): List of Edge objects to add
        graph (Network): Network object to add edges
    """
    for edge in edges:
        try:
            graph.add_edge(arrowStrikethrough=edge.arrow_strikethrough,
                           source=edge.from_node,
                           hidden=edge.hidden,
                           physics=edge.physics,
                           title=edge.title,
                           to=edge.to_node,
                           width=edge.width)
        except AssertionError:
            print(f'Can not add edge: {edge}')


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
                       bgcolor='#d3dbe3')

    # Add the nodes and edges
    add_node_objects(nodes, my_graph)
    add_edge_objects(edges, my_graph)

    # Show the buttons for adjusting the graph
    my_graph.show_buttons()

    # Make the html file
    my_graph.show(graph_filename, notebook=False)
