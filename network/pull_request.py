import json
from itertools import chain

import networkx as nx
import numpy as np

from ..db.session import query


def get_edges() -> np.ndarray:
    """Get communication edges between users

    :return: :class:`numpy.ndarray` of edges
    """
    return np.fromiter(
        chain.from_iterable(list(x) for x in query('SELECT * FROM github.v_edges')), dtype=int
    ).reshape((-1, 2))


def get_nodes() -> np.ndarray:
    """Get user ids as nodes

    :return: :class:`numpy.ndarray` of nodes
    """
    return np.fromiter((x[0] for x in query('SELECT * FROM github.v_nodes')), dtype=int)


def get_labels() -> dict[int, str]:
    """Get label mapping with user logins names as labels

    :return: Labels mapping
    """
    mapping_json = next(query('SELECT * FROM github.pg_User_GetLogins()'))
    mapping = json.loads(mapping_json[0])

    return {int(k): v for k, v in mapping.items()}


def get_graph() -> nx.MultiDiGraph:
    """Get repository graph

    :return: networkx Graph
    """
    nodes = get_nodes()
    edges = get_edges()
    labels = get_labels()

    g = nx.MultiDiGraph()
    g.add_nodes_from(nodes)
    g.add_edges_from(edges)

    return nx.relabel_nodes(g, labels)
