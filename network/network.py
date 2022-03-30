import json
from itertools import chain

import networkx as nx
import numpy as np

__VIEW_TAG_NODES__ = "SELECT * FROM kaggle.v_tag_co_occurrence_nodes"
__VIEW_TAG_EDGES__ = "SELECT * FROM kaggle.v_tag_co_occurrence_edges"

from db.session import query


def get_tag_nodes() -> np.ndarray:
    """Get tag co-occurrence nodes from database

    :return: 1-D Numpy array of nodes
    """
    return np.fromiter((x[0] for x in query(__VIEW_TAG_NODES__)), dtype=int)


def get_tag_edges() -> np.ndarray:
    """Get tag co-occurrence weighted edges.

    Weight is the count of co-occurrence.

    :return: 2-D Numpy array where each row is (u, v, w)
    """
    return np.fromiter(
        chain.from_iterable(list(x) for x in query(__VIEW_TAG_EDGES__)), dtype=int
    ).reshape((-1, 3))


def get_label_mapping() -> dict:
    """Get label mapping with tag names as labels

    :return: Dictionary with key as node (tag) and value as node (tag) name
    """
    mapping_json = next(query("SELECT kaggle.pg_Get_LabelMapping()"))
    mapping = json.loads(mapping_json[0])

    return {int(k): v for k, v in mapping.items()}


def get_tag_graph() -> nx.Graph:
    """Get networkx Graph of tag co-occurrence in competitions

    :return: networkx graph object
    """
    nodes = get_tag_nodes()
    edges = get_tag_edges()
    label_mapping = get_label_mapping()

    g = nx.Graph()
    g.add_nodes_from(nodes)
    g.add_weighted_edges_from(edges)
    nx.relabel_nodes(g, label_mapping, False)

    return g


def draw_graph(graph: nx.Graph):
    """Draw graph with kamada kawai layout

    :param graph: networkx Graph object
    """
    layout = nx.kamada_kawai_layout(graph)
    all_params = get_all_params(graph, layout)

    nx.draw_networkx_nodes(**all_params["nodes_params"])
    nx.draw_networkx_edges(**all_params["edges_params"])

    for params in all_params["labels_param_list"]:
        nx.draw_networkx_labels(**params)


def get_all_params(graph, layout):
    """Get params for visualization

    :param graph: networkx graph
    :param layout: networkx layout
    :return:
    """
    node_params = {"G": graph, "pos": layout, "node_size": []}
    edges_params = {"G": graph, "pos": layout, "width": []}
    labels_params = {}
    labels = {}

    for node in graph.nodes:
        node_params["node_size"] += [20 * graph.degree[node] ** 2]
        degree = graph.degree[node]

        if degree not in labels:
            labels[degree] = {}
        labels[degree][node] = node
        if degree in labels_params:
            continue

        labels_params[degree] = {
            "G": graph,
            "pos": layout,
            "font_size": max([2 * degree ** 2, 14]),
            "labels": labels[degree],
        }

    for edge in graph.edges:
        edges_params["width"] += [graph.edges[edge]["weight"]]
        edges_params["alpha"] = 0.5

    return {
        "nodes_params": node_params,
        "edges_params": edges_params,
        "labels_param_list": sorted(
            labels_params.values(), key=lambda x: x["font_size"]
        ),
    }
