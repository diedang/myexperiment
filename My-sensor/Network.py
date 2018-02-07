# -*- coding: utf-8 -*-
"""
author@diednag

A network of sensor nodes
"""
from Node import *

import scipy
import numpy as np


class Network:

    """
    Class members

    nodes: dictionary : (node_name, node_object)
    edges: list: "first_name-second_name"
    max_node: string: the name of the node with the most neighbors
    min_node: string: the name of the node with the fewest neighbors

    """
    def __init__(self):

        # create the node dictionary
        self.nodes = {}

        # holds the edges in the network
        self.edges = []

        # Interest nodes
        self.max_node = "0"
        self.min_node = "0"

    def update_all_readings(self):
        """
        runs the network to get the reading of the nodes
        :return:
        """

        # update the reading of all nodes
        for node_name in self.nodes:

            # update the readings of all nodes
            self.nodes[node_name].reading()

        # once all nodes have updated, they can be stabilized
        for node_name in self.nodes:

            self.nodes[node_name].stabilize()

    def get_network_reading(self):
        """
        Uses the readings from all nodes to report the mean and standard deviation of all nodes
        :return: network_avg, network_std
        """

        # update the readings for all nodes
        self.update_all_readings()

        # get the current readings from all nodes
        node_readings = []
        for node_name in self.nodes:

            node_readings.append(self.nodes[node_name].stable_reading)

        node_readings = np.array(node_readings)

        # get the average
        network_avg = scipy.average(node_readings)

        # get the standard deviation
        network_std = scipy.std(node_readings)

        return network_avg, network_std

    def add_node(self, node_name, node_object):
        """

        :param node_name: string, the unique name of the node
        :param node_object:
        :return:
        """
        self.nodes[node_name] = node_object

    def node_names(self):
        """
        Generator that returns the names of all nodes in the network
        :return:
        """

        for node_name in self.nodes.keys():

            yield node_name

    def get_network_average_position(self):
        """

        gets average position of all nodes in the network
        :return: numpy array: shape(R_space)
        """
        # the total number of nodes in the network
        num_nodes = self.total_nodes()

        # get the location of all nodes
        all_nodes = np.empty((num_nodes, R_space))
        for index, item in enumerate(self.nodes.values()):

            all_nodes[index] = item.get_position()

        # get the sum of all of the positions along space dim and divide by the number of nodes
        average_position = np.sum(all_nodes, axis=0) / num_nodes

        return average_position

    def get_node_reading(self, node_name):
        """

        :param node_name:
        :return: the stable reading of a node
        """
        return self.nodes[node_name].stable_reading

    def get_node_degree(self, node_name):
        """

        :param node_name:
        :return: the degree of a node
        """

        return self.nodes[node_name].get_degree()

    def update_neighbors(self):

        for node in self.nodes.values():

            node.acquire_neighbors()

    def make_graph(self):
        """

        Makes an undirected graph from the nodes and their neighbors
        :return: a list of all edges
        """
        # update the neighbors in the graph
        self.update_neighbors()

        # Go through each node and get their neighbors
        self.edges = []
        for node_name in self.nodes:

            # get the neighbors
            node_neighbors = self.nodes[node_name].neighbors

            # go through neighbors
            for neighbor_name in node_neighbors:

                # Make the edge key
                edge_key = "-".join(sorted([node_name, neighbor_name]))

                # Add it to the edge list if it is not already present
                if edge_key not in self.edges:

                    self.edges.append(edge_key)

        return self.edges

    def check_connected(self, update=True):
        """
        checks to make sure that the network is connected
        :param update: bool ; if true, neighbors will be updated before checking
        :return: Bool
        """
        # update if needed
        if update:

            self.update_neighbors()

        # go through each node checking that each degree id greater than 0
        for node in self.nodes:

            # only one node needs to be disconnected to fail
            if len(self.nodes[node].neighbors) < 1:
                return False

        return True

    def total_nodes(self):

        return len(self.nodes)

    def get_interest_nodes(self):
        """
        get the nodes with the lowest and highest number of neighbors

        :return: string, string; names of the lowest, highest
        """
        # go through each node in the network to find the min and max degrees
        max_value = 0
        min_value = len(self.nodes)
        for name in self.nodes:

            # check for new max
            if self.nodes[name].get_degree() >= max_value:

                max_value = self.nodes[name].get_degree()

                self.max_node = name

            # check for new min
            elif self.nodes[name].get_degree() <= min_value:

                min_value = self.nodes[name].get_degree()

                self.min_node = name

        return self.max_node, self.min_node
