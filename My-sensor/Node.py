# -*- coding: utf-8 -*-
"""
author@diedang

A single node in the sensor network
R_space is the number of dimensions being worked in
"""

import numpy as np

T_space = 1
R_space = 2


class Node:
    """
    class members

    neighbors: list
    Holds the names of all neighboring nodes

    stable_reading: numpy array:shape(T_space)
    The reading from the last update, needed tp avoid race conditions

    unstable_reading: numpy arrayK:shape(T_space)
    The reading after running the consensus for this node, while other nodes are still updating
    """
    def __init__(self, environment, network, name, reading_noise=.01, range_s=1.6, consensus_method="MaxDegree"):
        """

        :param environment:Environment()
        Object that the node will use to find information about the environment

        :param network: Network()
        This node is a member of the network
        used to find information about the network

        :param name: string
        A unique name of this node

        :param reading_noise: float
        The noise of the reading as defined by cv in the project description

        :param range_s: float
        optimal sensing range

        :param consensus_method: string
        The name of the method to use to fuse readings form neighbors
        """
        # save the environment and network
        self.environment = environment
        self.network = network

        # save the name of this node
        self.name = name

        # save the reading parameters
        self.reading_noise = reading_noise
        self.rang_s = range_s

        # holds the neighbors of this node
        self.neighbors = []

        # holds the readings of every neighbor
        self.neighbor_readings = {}

        # the last reading that is valid, to avoid race conditions among node reports
        # use a noisy initial estimate of the target without any fusion
        self.stable_reading = np.random.normal(scale=30, size=(T_space,)) + self.environment.get_target_reading_at(0)

        # the value storing the consensus while the other nodes are updating
        self.unstable_reading = None

        # set which consensus method to use
        self.fuse_readings = self.consensus_methods[consensus_method]

    def max_degree(self):

        # go through each neighbor reading and accumulate the reading
        acc_reading = np.zeros(T_space)
        for neighbor_name in self.neighbor_readings:

            # get the value of the neighbor reading
            neighbor_value = self.neighbor_readings[neighbor_name]

            # set the weight for the reading
            weight = 1.0 / self.network.total_nodes()

            # add the reading based on the weight
            acc_reading += weight * neighbor_value

        # set the weight of this node  so that the weights all sum to 1
        self_weight = 1 - (self.get_degree() / float(self.network.total_nodes()))

        # add the weight of this node
        acc_reading += self_weight * self.get_sensor_reading()

        return acc_reading

    def metropolis(self):
        pass

    def design1(self):
        pass

    def design2(self):
        pass

    consensus_methods = {
        "WeightDesign1": design1,
        "WeightDesign2": design2,
        "MaxDegree": max_degree,
        "Metropolis": metropolis
    }

    def reading(self):
        """
        sets the unstable reading for this node, and returns it
        output is based on the consensus method chosen for the node
        :return:
        """
        # update the neighbor readings
        self.acquire_neighbor_readings()

        # use the set consensus method to get the reading
        self.unstable_reading = self.fuse_readings(self)

        # return the reading
        return self.unstable_reading

    def stabilize(self):
        """
        Once the network is done updating, the unstable reading becomes the new stable reading
        :return:
        """
        self.stable_reading = self.unstable_reading

    def get_position(self):

        return self.environment.get_node_position(self.name)

    def get_sensor_reading(self):
        """
        Gets the sensor reading of this node
        :return: numpy array： shape(R_space,)
        """

        # get the deviation for the noise term
        sigma = np.sqrt((np.linalg.norm(self.get_position() - self.network.get_network_average_position())
                         ** 2 + self.reading_noise) / (self.rang_s ** 2))

        # get the noise
        noise = np.random.normal(scale=sigma, size=(T_space,))

        # get the measurement from the environment and add the noise
        measurement = self.environment.get_target_reading() + noise

        return measurement

    def acquire_neighbors(self):
        """
        Acquires the neighbors of this node
        :return:
        """
        self.neighbors = self.environment.get_node_neighbors(self.name)

    def get_degree(self):
        """
        Gets the degree oof this node
        Does not update before checking
        :return:
        """
        return len(self.neighbors)

    def acquire_neighbor_readings(self):
        """
        Gets the reading from every neighbor
        :return:
        """
        # Clear current readings
        self.neighbor_readings = {}

        # Update the neighbors
        self.acquire_neighbors()

        # Go through each neighbor and get the reading
        for node in self.neighbors:

            self.neighbor_readings[node] = self.network.get_node_reading(node)
