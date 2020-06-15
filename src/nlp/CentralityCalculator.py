import networkx as nx
import numpy as np
from scipy.sparse.csgraph import floyd_warshall

from src.nlp.util import norm_to_one


class CentralityCalculator:
    """
    Provides several algorithms that calculate the centrality of an adjacency matrix
    """

    def __init__(self, nodes: list, edges: dict):
        """
        :param nodes: list of node names
        :param edges: dictionary in form of { 'source node': 'target node' } that indicates a connection
                      between two nodes.
                      May also contain edge weights: { 'source node': { 'target node': weight }}
        """
        self.damping = 0.85  # damping coefficient
        self.min_diff = 1e-8  # convergence threshold
        self.steps = 1000  # iteration steps
        self.nodes = set(nodes)
        self.edge_weights = edges
        self.node_pairs = [[n1, n2] for n1 in self.nodes for n2 in list(self.edge_weights[n1])]
        self.node_ids = {node: i for i, node in enumerate(nodes)}

    def _adjacency_matrix(self, normalized: bool = False, weighted: bool = False) -> np.array:
        """
        Builds the adjacency matrix.

        :param normalized: indicates if the matrix should be normalized
        :param weighted: indicates if edge weights (if available) should be used instead of `1`
        :return: adjacency matrix
        """
        # Build matrix
        node_size = len(self.nodes)
        g = np.zeros((node_size, node_size), dtype='float')
        for node1, node2 in self.node_pairs:
            i, j = self.node_ids[node1], self.node_ids[node2]
            if weighted and isinstance(self.edge_weights[node1], dict):
                # if available, use edge weight instead of '1' in matrix
                g[j][i] = self.edge_weights[node1][node2]
            else:
                g[i][j] = 1

        if normalized:
            # Normalize matrix by column
            norm = np.sum(g, axis=0)
            g = np.divide(g, norm, where=norm != 0)  # ignores the 0 element in norm

        return g

    def _node_weight_from_vector(self, vector: np.array) -> dict:
        """
        Maps the values of the vector to a node.

        :param vector: centrality vector
        :return: { node: value } dictionary
        """
        node_weight = dict()
        for word, index in self.node_ids.items():
            node_weight[word] = vector[index]

        return node_weight

    def _nx_centrality(self, centrality_function, norm=True) -> dict:
        """
        Transforms an adjacency matrix into a NetworkX Graph and calls the given centrality algorithm with it.

        :param centrality_function: centrality function that takes a NetworkX Graph and returns a dictionary.
        :param norm: Flag that indicates if the resulting numbers should be normed to 1
        :return: { node: value } dictionary with centrality values
        """
        g = self._adjacency_matrix()
        gnx = nx.from_numpy_matrix(g)
        result = np.array(list(centrality_function(gnx).values()))
        if norm:
            result = norm_to_one(result)

        return self._node_weight_from_vector(result)

    def text_rank(self) -> dict:
        """
        Calculates the TextRank (PageRank) for the nodes.
        The value indicates the importance of a node in the network.

        See https://towardsdatascience.com/textrank-for-keyword-extraction-by-python-c0bae21bcec0 for reference.

        :return: { node: text_rank } dictionary that maps a node to its calculated TextRank value
        """
        g = self._adjacency_matrix(normalized=True)
        product = np.array([1] * len(self.nodes))

        previous_pr = 0
        for _ in range(self.steps):
            product = (1 - self.damping) + self.damping * np.dot(g, product)
            if abs(previous_pr - sum(product)) >= self.min_diff:
                previous_pr = sum(product)
            else:
                break

        normed = norm_to_one(product)
        # Get weight for each node
        return self._node_weight_from_vector(normed)

    def text_rank_nx(self) -> dict:
        """
        NetworkX implementation of the PageRank algorithm.

        :return: { node: value } dictionary that maps a node to its calculated TextRank value
        """
        return self._nx_centrality(nx.pagerank_numpy)

    def eigenvector(self) -> dict:
        """
        Calculates the Eigenvector for the nodes.
        The value indicates the influence of a node in the network.
        See https://en.wikipedia.org/wiki/Eigenvector_centrality

        :return: { node: value } dictionary that maps a node to its calculated eigenvector value
        """
        g = self._adjacency_matrix(normalized=True)
        product = np.array([1] * len(self.nodes))

        previous_pr = 0
        for _ in range(self.steps):
            product = np.dot(g, product)
            if abs(previous_pr - sum(product)) >= self.min_diff:
                previous_pr = sum(product)
            else:
                break

        normed = norm_to_one(product)
        # Get weight for each node
        return self._node_weight_from_vector(normed)

    def eigenvector_nx(self) -> dict:
        """
        NetworkX implementation of the eigenvector centrality algorithm.

        :return: { node: value } dictionary that maps a node to its calculated eigenvector value
        """
        return self._nx_centrality(nx.eigenvector_centrality_numpy)

    def katz_centrality(self, alpha=0.1) -> dict:
        """
        Calculates the KatzRank for the nodes.
        The value indicates the relative degree of influence of a node in the network.

        See https://en.wikipedia.org/wiki/Katz_centrality

        :param alpha: Attenuation factor. Each path or connection between a pair of nodes is assigned
                      a weight determined by alpha and the distance between nodes as alpha^d.
        :return: { node: value } dictionary that maps a node to its calculated katz rank value
        """

        size = len(self.nodes)
        transposed = self._adjacency_matrix().T
        b = np.array([1] * size)
        centrality = np.linalg.solve(np.eye(size, size) - (alpha * transposed), b)
        centrality = norm_to_one(centrality)
        return self._node_weight_from_vector(centrality)

    def katz_centrality_nx(self) -> dict:
        """
        NetworkX implementation of the Katz centrality algorithm.

        :return: { node: value } dictionary that maps a node to its calculated katz rank value
        """
        return self._nx_centrality(nx.katz_centrality)

    def degree(self) -> dict:
        """
        Calculates the Degree centrality for the nodes.

        :return: { node: value } dictionary that maps a node to it's calculated closeness value
        """
        g = self._adjacency_matrix()
        g_sum = g.sum(axis=0) / (len(self.nodes) - 1)

        return self._node_weight_from_vector(g_sum)

    def harmonic(self) -> dict:
        """
        Calculates the normalized harmonic centrality for the nodes.

        Using the following formula:

        sum(1 / distance from node to all other nodes excluding itself) / (number of nodes - 1)

        :return: { node: value } dictionary that maps a node to it's calculated harmonic degree value
        """

        g = self._adjacency_matrix()
        dist = np.array(floyd_warshall(g))
        dist[dist == 0] = np.inf
        norm = (1 / dist)
        result = np.sum(norm, axis=0) / (len(g) - 1)

        return self._node_weight_from_vector(result)

    def closeness(self) -> dict:
        """
        Calculates the normalized closeness centrality for the nodes.

        Using the following formula:

        (number of nodes - 1) / sum(distance from node to all other nodes)

        :return: { node: value } dictionary that maps a node to it's calculated closeness value
        """

        g = self._adjacency_matrix()
        dist = floyd_warshall(g)
        result = (len(g) - 1) / np.sum(dist, axis=0)

        return self._node_weight_from_vector(result)

    def betweenness_nx(self) -> dict:
        """
        NetworkX implementation of the betweenness centrality algorithm.

        :return: { node: value } dictionary that maps a node to it's calculated betweenness value
        """
        return self._nx_centrality(nx.betweenness_centrality)
