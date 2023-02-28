"""
spaghett.py
Used for testing code before putting it in the correct module.
"""

# Imports
import ast
from glob import iglob
from pathlib import Path
from sys import stdlib_module_names
from typing import Any

from graph import (Node, Edge, make_graph)
# ----------------------------------------------------------------------------

# Variables/Constants
FOLDER_PATH = Path(r'C:\Users\burns\OneDrive\Repos\FlaskTesting_Copy')
IGNORE_DIR = Path(
    r'C:\Users\burns\OneDrive\Repos\FlaskTesting_Copy\flask_test_env')


graph_nodes: set[str] = set()
graph_edges: list[tuple] = []

graph_nodes2: list[Node] = []
graph_edges2: list[Edge] = []
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


def make_node(node_id: str | int) -> None:
    """Make a node for the graph.

    Args:
        node_id (str | int): Node ID
    """
    if node_id in stdlib_module_names:
        print('loop')


def make_edge(from_node: str,
              to_node: str,
              edge_title: str = None) -> None:
    """Makes an edge item.

    Args:
        from_node (str): First node (src module)
        to_node (str): Second node (referenced module)
        edge_title (str): Label for the edge (what is being imported)
    """
    graph_edges.append((from_node, to_node, edge_title))


class ImportLister(ast.NodeVisitor):
    "Imports visitor"

    def __init__(self, src_module: str) -> None:
        self.src_module = src_module

    def visit_Import(self, node: ast.Import) -> Any:
        """Grab Imports from the module"""
        for item in node.names:
            graph_nodes.add(item.name)
            make_edge(self.src_module, item.name, item.name)
        self.generic_visit(node)


class FromImportLister(ast.NodeVisitor):
    "FromImports visitor"

    def __init__(self, src_module: str) -> None:
        self.src_module = src_module

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        """Grab From * Import ** from the module"""

        for item in node.names:
            graph_nodes.add(node.module)
            make_edge(self.src_module, node.module, item.name)

        self.generic_visit(node)


def ast_test(myfile: Path, src_module: str):
    """Read and parse"""

    print('ast_test START')
    with open(myfile, encoding='utf-8') as opened:
        code = opened.read()

    node = ast.parse(code)
    ImportLister(src_module=src_module).visit(node)
    FromImportLister(src_module=src_module).visit(node)
    print('ast_test END\n')


def mf_funct(files: list[Path]):
    """Finds imports on all files

    Args:
        files (list[Path]): Python filepaths
    """

    for file_ in files:
        # Lowercases the filepath, replaces .py with nothing, replaces \ with .
        module = str(file_.relative_to(FOLDER_PATH)).lower().replace(
            '.py', '').replace('\\', '.')
        print(f'MODULE: {module}')
        graph_nodes.add(module)

        ast_test(file_, module)


if __name__ == '__main__':
    print('CODE STARTING!')
    files = get_files(FOLDER_PATH, IGNORE_DIR)
    for file_ in files:
        print(file_)

    # mf_funct(files_to_parse)
    # print('\nMODULES')
    # for i in graph_nodes:
    #     print(i)
    # print('\nEDGES')
    # for i in graph_edges:
    #     print(i)

    # myspaghett = Graph(graph_nodes, graph_edges, is_directed=True)

    # make_graph(myspaghett, "spaghett.html")
    print('CODE FINISHED!')
