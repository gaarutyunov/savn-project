import json
from itertools import chain

import networkx as nx
import numpy as np

from kaggle.db.session import query


def _get_nodes(view: str) -> np.ndarray:
    return np.fromiter((x[0] for x in query(view)), dtype=int)


def _get_edges(view: str) -> np.ndarray:
    return np.fromiter(
        chain.from_iterable(list(x) for x in query(view)), dtype=int
    ).reshape((-1, 3))


def _get_labels_mapping(procedure: str) -> dict:
    """Get label mapping with tag names as labels

    :return: Dictionary with key as node (tag) and value as node (tag) name
    """
    mapping_json = next(query(procedure))
    mapping = json.loads(mapping_json[0])

    return {int(k): v for k, v in mapping.items()}


def draw_graph(graph: nx.Graph):
    """Draw graph with kamada kawai layout

    :param graph: networkx Graph object
    """
    layout = nx.kamada_kawai_layout(graph)
    all_params = _get_all_params(graph, layout)

    nx.draw_networkx_nodes(**all_params["nodes_params"])
    nx.draw_networkx_edges(**all_params["edges_params"])

    for params in all_params["labels_param_list"]:
        nx.draw_networkx_labels(**params)


def _get_all_params(graph, layout):
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
        node_params["node_size"] += [2 * graph.degree[node] ** 2]
        degree = graph.degree[node]
        if degree < 4:
            continue

        if degree not in labels:
            labels[degree] = {}
        labels[degree][node] = node
        if degree in labels_params:
            continue

        labels_params[degree] = {
            "G": graph,
            "pos": layout,
            "font_size": 3 * np.power(degree, 1 / 2),
            "labels": labels[degree],
        }

    for edge in graph.edges:
        edges_params["width"] += [graph.edges[edge]["weight"]]
        edges_params["alpha"] = 0.1

    return {
        "nodes_params": node_params,
        "edges_params": edges_params,
        "labels_param_list": sorted(
            labels_params.values(), key=lambda x: x["font_size"]
        ),
    }
