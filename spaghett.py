"""
spaghett.py
Used for testing code before putting it in the correct module.
"""

# Imports
import ast
import configparser
from glob import iglob
from pathlib import Path
from sys import stdlib_module_names
from typing import Any

from graph import (Node, Edge, make_graph)
# ----------------------------------------------------------------------------

# Grab config file settings.
config = configparser.ConfigParser()
config.read('config.ini')

# Variables/Constants
FOLDER_PATH = Path(config['CONFIG']['FOLDER_PATH'])
IGNORE_DIR = Path(config['CONFIG']['IGNORE_DIR'])
graph_nodes: set[Node] = set()
graph_edges: list[Edge] = []
# ----------------------------------------------------------------------------


def get_files(root_dir: Path = None,
              ignore_dir: Path = None) -> list[Path]:
    """Get .PY files from the root_dir

    Args:
        root_dir (Path): Directory to start looking.
        ignore_dir (Path, optional): Directory to ignore.

    Returns:
        list[Path]: List of python files to parse
    """
    pyfiles: list[Path] = []
    pathname: str = str(root_dir) + r'\**\*.py'

    # Grabs all .py files recursively.
    for item in iglob(pathname, root_dir=root_dir, recursive=True):
        pyfiles.append(Path(item))

    # No ignore, return what we found immediately.
    if ignore_dir is None:
        return pyfiles

    # Remove files found in the ignore_dir.
    pyfiles2: list[Path] = []
    for pyfile in pyfiles:
        if not pyfile.is_relative_to(ignore_dir):
            pyfiles2.append(pyfile)

    return pyfiles2


def make_node(node_id: str | int) -> Node:
    """Make a node for the graph.

    Args:
        node_id (str | int): Node ID

    Returns:
        (Node): Node object for the node_id
    """
    # Format stdlib modules
    if node_id in stdlib_module_names:
        return Node(n_id=node_id,
                    label=node_id,
                    title=node_id,
                    level=0,
                    color='red',
                    shape='ellipse')
    # Format default
    return Node(n_id=node_id,
                label=node_id,
                title=node_id)


def make_edge(from_node: str,
              to_node: str,
              edge_title: str = None) -> Edge:
    """Makes an edge item.

    Args:
        from_node (str): First node (src module)
        to_node (str): Second node (referenced module)
        edge_title (str): Label for the edge (what is being imported)
    """
    return Edge(from_node=from_node,
                title=edge_title,
                to_node=to_node)


class ImportLister(ast.NodeVisitor):
    "Imports visitor"

    def __init__(self, src_module: str) -> None:
        self.src_module = src_module

    def visit_Import(self, node: ast.Import) -> Any:
        """Grab Imports from the module"""

        for item in node.names:
            if item.name is not None:
                graph_nodes.add(make_node(item.name))
                graph_edges.append(make_edge(from_node=item.name,
                                             to_node=self.src_module,
                                             edge_title=item.name))

        self.generic_visit(node)


class FromImportLister(ast.NodeVisitor):
    "FromImports visitor"

    def __init__(self, src_module: str) -> None:
        self.src_module = src_module

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        """Grab From * Import ** from the module"""

        for item in node.names:
            if node.module is not None:
                graph_nodes.add(make_node(node.module))
                graph_edges.append(make_edge(from_node=node.module,
                                             to_node=self.src_module,
                                             edge_title=item.name))

        self.generic_visit(node)


def parse_file(myfile: Path):
    """Read and parse"""

    # Get the module relative path since you can have modules with same names
    # in different paths/packages.
    module = str(myfile.relative_to(FOLDER_PATH)).lower().replace(
        '.py', '').replace('\\', '.')

    # Open and read the module/python file.
    with open(myfile, encoding='utf-8') as opened:
        code = opened.read()

    node = ast.parse(code)
    graph_nodes.add(make_node(module))
    ImportLister(src_module=module).visit(node)
    FromImportLister(src_module=module).visit(node)


if __name__ == '__main__':
    print('CODE STARTING!')

    files = get_files(FOLDER_PATH, IGNORE_DIR)

    # Parse files and get graph nodes and edges.
    for file_ in files:
        try:
            parse_file(file_)
        except UnicodeDecodeError:
            print(f'Can not parse {file_}')

    print('\nMODULES')
    for i in graph_nodes:
        print(i)
    print('\nEDGES')
    for i in graph_edges:
        print(i)

    make_graph(nodes=graph_nodes,
               edges=graph_edges,
               graph_filename="spaghett.html")
    print('CODE FINISHED!')
