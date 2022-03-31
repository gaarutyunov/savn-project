import networkx as nx
import numpy as np

from kaggle.network.utils import _get_nodes, _get_labels_mapping, _get_edges

__VIEW_TAG_NODES__ = "SELECT * FROM kaggle.v_tag_co_occurrence_nodes"
__VIEW_TAG_EDGES__ = "SELECT * FROM kaggle.v_tag_co_occurrence_edges"
__GET_TAG_LABELS_MAPPING__ = "SELECT kaggle.pg_Tag_Get_LabelMapping()"


def get_tag_nodes() -> np.ndarray:
    """Get tag co-occurrence nodes from database

    :return: 1-D Numpy array of nodes
    """
    return _get_nodes(__VIEW_TAG_NODES__)


def get_tag_edges() -> np.ndarray:
    """Get tag co-occurrence weighted edges.

    Weight is the count of co-occurrence.

    :return: 2-D Numpy array where each row is (u, v, w)
    """
    return _get_edges(__VIEW_TAG_EDGES__)


def get_tag_label_mapping() -> dict:
    """Get label mapping with tag names as labels

    :return: Dictionary with key as node (tag) and value as node (tag) name
    """
    return _get_labels_mapping(__GET_TAG_LABELS_MAPPING__)


def get_tag_graph() -> nx.Graph:
    """Get networkx Graph of tag co-occurrence in competitions

    :return: networkx graph object
    """
    nodes = get_tag_nodes()
    edges = get_tag_edges()
    label_mapping = get_tag_label_mapping()

    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_weighted_edges_from(edges)
    nx.relabel_nodes(g, label_mapping, False)

    return g
