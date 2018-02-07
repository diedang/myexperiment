# -*- coding: utf-8 -*-
"""
author@diedang

The environment that the nodes are in
Nodes interact with this class to find their positions and sensor readings
"""
from scipy.spatial import distance


class Environment:
    """
    Class members

    nodes: dictionary: (node_name : position): holds information about nodes
    position: numpy array: shape(R_space,)

    target_function: function(numeric time_step)
    Gives the true position of the target as a function of time

    time_step: numeric
    The current time to evaluate
    """

    def __init__(self, target_position, target_reading, communication_radius=None, max_neighbors=None):
        """

        :param target_position: function(numeric time_step)
        Needs to give the position of the target being tracked as a function of time

        :param target_reading: function(numeric time_step)
        Needs to give the reading of the target being tracked as a function of time

        :param communication_radius: float
        Determines how far a node can communicate
        Defaults to None, means that the node can communicate with every  other node in network


        :param max_neighbors: int
        The maximum number of neighbors to accept, nodes closer have priority
        Defaults to None, means that every node in the communication_radius will be a neighbor
        """
        # Create the node dictionary
        self.nodes = {}

        # save the target position function
        self.target_position = target_position

        # save the reading position function
        self.target_reading = target_reading

        # set the node communication parameters
        self.communication_radius = communication_radius
        self.max_neighbors = max_neighbors

        # set the initial time to 0
        self.time_step = 0

    def advance(self, increment=1):

        # moves the environment ahead by the set amount
        self.time_step += increment

    def add_node(self, node_name, node_position):
        """
        Adds a node to the network at the specified position
        :param node_name: string
        The unique name of the node

        :param node_position: numpy array: shape(R_space,)
        The location of the node in the environment
        :return:
        """
        self.nodes[node_name] = node_position

    def get_node_position(self, node_name):
        """
        Returns the position of a node
        :param node_name: string
        the name of the node to get the position of
        :return: numpy array: shape(R_space)
        The position of the specified node
        """
        return self.nodes[node_name]

    def get_target_position(self):
        """
        returns the true position of the target
        :return: numpy array： shape(R_space,)
        """
        return self.get_target_position_at(self.time_step)

    def get_target_reading(self):
        """
        return the true reading of the target
        :return: numpy array:shape(T_space,)
        """
        return self.get_target_reading_at(self.time_step)

    def get_target_position_at(self, time_step):
        """
        Evaluates the position function at the specified time step
        :param time_step:
        :return: numpy array: shape(T_space)
        """
        return self.target_position(time_step)

    def get_target_reading_at(self, time_step):
        """
        Evaluates the reading function at the specified time step
        :param time_step:
        :return: numpy array: shape(T_space)
        """
        return self.target_reading(time_step)

    def set_communication_radius(self, new_communication_radius):

        # set the communication radius to the sent value
        self.communication_radius = new_communication_radius

    def get_node_neighbors(self, node_name):
        """
        Return the neighbors of the node
        :param node_name:
        :return: list[strings]
        The nodes that are the neighbors of the specified node
        """
        # get the location of the interest node
        node_position = self.nodes[node_name]

        # get the distances to every other node in the network
        names = []
        distances = []
        for name in self.nodes:

            # get the position
            position = self.nodes[name]

            # ignore if the node is the interest node
            if node_name != name:

                # get the distance between the nodes
                dist = distance.euclidean(node_position, position)

                # if the communication_radius is None, add the node
                if self.communication_radius is None:

                    # Add the node to the name list
                    names.append(name)

                    # Add the distance
                    distances.append(dist)
                # If communication_radius is sent and distance is within range, add the node to the lists
                elif dist <= self.communication_radius:

                    # Add the node to the name list
                    names.append(name)

                    # Add the distance
                    distances.append(dist)

        # Sort the name list by the distances
        closest = [n for (d, n) in sorted(zip(distances, names))]

        # If max_neighbors is sent, remove all items after the max
        if self.max_neighbors is not None:

            closest = closest[:self.max_neighbors]

        return closest
