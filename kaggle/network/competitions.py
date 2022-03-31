__VIEW_COMPETITION_NODES__ = "SELECT * FROM kaggle.v_competitions_teams_nodes"
__VIEW_COMPETITION_EDGES__ = "SELECT * FROM kaggle.v_competitions_teams_edges"
__GET_COMPETITION_LABELS_MAPPING__ = "SELECT kaggle.pg_Competition_Get_LabelMapping()"

import networkx as nx
import numpy as np

from kaggle.network.utils import _get_nodes, _get_edges, _get_labels_mapping


def get_competition_nodes() -> np.ndarray:
    """Get competitions nodes from database

    :return: 1-D Numpy array of nodes
    """
    return _get_nodes(__VIEW_COMPETITION_NODES__)


def get_competition_edges() -> np.ndarray:
    """Get tag co-occurrence weighted edges.

    Weight is the count of co-occurrence.

    :return: 2-D Numpy array where each row is (u, v, w)
    """
    return _get_edges(__VIEW_COMPETITION_EDGES__)


def get_competition_label_mapping() -> dict:
    """Get label mapping with competition names as labels

    :return: Dictionary with key as node (competition) and value as node (competition) name
    """
    return _get_labels_mapping(__GET_COMPETITION_LABELS_MAPPING__)


def get_competition_graph() -> nx.Graph:
    """Get networkx Graph of tag co-occurrence in competitions

    :return: networkx graph object
    """
    nodes = get_competition_nodes()
    edges = get_competition_edges()
    label_mapping = get_competition_label_mapping()

    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_weighted_edges_from(edges)
    nx.relabel_nodes(g, label_mapping, False)

    return g
