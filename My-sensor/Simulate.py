# -*- coding: utf-8 -*-
"""
author@diedang

runs the entire consensus filter and visualizes results
"""
import sys

from Environment import *
from Network import *
from Node import *

import numpy as np
import matplotlib.pyplot as plt


class Simulate:
    """
    Class members

    environment: Environment()
    Object that handles the environment where the nodes are

    network: Network()
    This node is a member of the network
    used to find information about the network

    info : list
    [target_reading, target_location, network_average, network_std, max_node_reading, min_node_reading]
    Information about the network at each time step

    default_consensus_method: string
    What nodes will use to fuse readings

    alternate_comm: float
    If not None, the network will set the communication radius to this value every 10 cycles to create a dynamic network
    """
    def __init__(self, max_range, num_nodes=10, communication_radius=1.7, default_consensus_method="MaxDegree",
                 target_position_name="StationaryCenter", target_reading_name="Constant50", alternate_com=None):
        """
        Area will be square, target will be in the center

        :param max_range: numeric; The boundary of the environment
        :param num_nodes:  int; how many nodes to put into the network
        :param communication_radius:
        :param default_consensus_method:
        :param target_position_name:
        :param target_reading_name:
        :param alternate_com:
        """

        print("Using consensus method: ", default_consensus_method)

        self.network = None

        # nodes will use this as their consensus method unless another is specified at creation time
        self.default_consensus_method = default_consensus_method

        # set the target position function
        # stays in the middle
        if target_position_name == "StationaryCenter":
            target_position_function = lambda time_step: np.full((R_space,), max_range / 2.0)

        # Not know
        else:

            raise ValueError

        # set the target reading function
        # stays at 50.0
        if target_reading_name == "Constant50":
            target_reading_function = lambda time_step: np.full((R_space,), 50.0)

        # sin wave
        elif target_reading_name == "SinWave":

            target_reading_function = lambda time_step: np.full((T_space,), 2 * np.sin((1/2.0) * time_step))

        else:
            raise ValueError

        # Create the environment
        # use a constant position and reading for the target
        self.environment = Environment(target_position_function, target_reading_function,
                                       communication_radius=communication_radius)

        # make a network
        self.make_network(max_range, num_nodes=num_nodes)

        # get the nodes to track
        self.max_node, self.min_node = self.network.get_interest_nodes()

        # holds the network average and standard deviation at each time step
        self.info = []

        # the alternate communication radius
        self.communication_radius = communication_radius
        self.alternate_comm = alternate_com

    def make_network(self, max_range, retry_max=10, num_nodes=10):
        """
        make a network, ensuring that it is connected
        :param max_range:
        :param retry_max: int
        The maximum number of times to create a new network if they keep ending up disconnected
        Throws exception after too many failures
        :param num_nodes:
        :return:
        """
        # Redo if the network is disconnected
        retry_count = 0
        network_connected = False
        while retry_count < retry_max and not network_connected:

            # Create the network
            self.network = Network()

            # Randomly generate 10 nodes with positions around the target
            random_nodes = np.random.rand(num_nodes, R_space) * max_range

            # place the nodes into the environment and network
            for node_index, node_position in enumerate(random_nodes):

                # name is just the index as string
                node_name = str(node_index)

                # Add to environment
                self.environment.add_node(node_name, node_position)

                # create the node, use default values
                new_node = Node(self.environment, self.network, node_name,
                                consensus_method=self.default_consensus_method)

                # Add to the network
                self.network.add_node(node_name, new_node)

            # get the connected flag
            network_connected = self.network.check_connected()

            # Increment counter
            retry_count += 1

        # throw exception
        if not network_connected:
            raise RuntimeError

    def run(self, iterations=1000):

        # for dynamic network
        use_alt = True

        for time_step in range(iterations):

            # Switch the communication radius every 10 cycles, if alt is set
            if self.alternate_comm is not None:

                if time_step % 10 == 0:
                    # flip the toggle
                    use_alt = not use_alt

                    # set the communication radius in the environment
                    if use_alt:
                        self.environment.set_communication_radius(self.alternate_comm)
                    else:
                        self.environment.set_communication_radius(self.communication_radius)

            # Have the network update all of the readings
            avg, std = self.network.get_network_reading()

            # log the info
            self.info.append([self.environment.get_target_reading(), self.environment.get_target_position(),
                             avg, std, self.network.get_node_reading(self.max_node),
                              self.network.get_node_reading(self.min_node)])

            # advance the environment
            self.environment.advance()

    def visualize(self):
        """
        shows information about the network through mat plot lib
        shows position of nodes and location of the object being sensed
        :return:
        """
        # Figure 1 will be the locations of nodes and the tracked object
        plt.figure(1)

        # Set the title
        plt.title("Node and Target Positions, Normal Communication Radius")

        # Set the x and y axis names
        plt.xlabel("X location")
        plt.ylabel("Y location")

        self.environment.set_communication_radius(self.communication_radius)

        # Plot the neighbors of each node
        edges = self.network.make_graph()

        # Make a line for each neighbor
        for edge in edges:
            # Unpack the node names
            first_node, second_node = edge.split("-")

            # Get the coordinates of each node
            first_coordinates = self.environment.get_node_position(first_node)
            second_coordinates = self.environment.get_node_position(second_node)

            # Make a line
            plt.plot([first_coordinates[0], second_coordinates[0]], [first_coordinates[1], second_coordinates[1]],
                     'bs-', markersize=0.0)

        # Mark the interest nodes
        max_location = self.environment.get_node_position(self.max_node)
        plt.plot(max_location[0], max_location[1], 'c*', markersize=20.0, label="Max Node")

        min_location = self.environment.get_node_position(self.min_node)
        plt.plot(min_location[0], min_location[1], 'm*', markersize=20.0, label="Min Node")

        # Add the locations of every node in the graph
        # Uses the true positions in the environment
        node_positions_x = []
        node_positions_y = []
        for node_name in self.network.node_names():
            # Get the position of the node
            node_position = self.environment.get_node_position(node_name)

            # Add it to the list
            node_positions_x.append(node_position[0])
            node_positions_y.append(node_position[1])

        # Plot points
        plt.plot(node_positions_x, node_positions_y, 'ko', label="Nodes")

        # Plot the target location
        # Use the starting position, target is stationary for now
        target_position = self.environment.get_target_position()
        plt.plot(target_position[0], target_position[1], 'r*', markersize=20.0, label="Target")

        # Set the legend
        plt.legend(loc="best")

        # Figure 3 will be the other network configuration, if the network is dynamic
        if self.alternate_comm is not None:
            plt.figure(3)

            # Set the title
            plt.title("Node and Target Positions, Alternate Communication Radius")

            # Set the x and y axis names
            plt.xlabel("X location")
            plt.ylabel("Y location")

            self.environment.set_communication_radius(self.alternate_comm)

            # Plot the neighbors of each node
            edges = self.network.make_graph()

            # Make a line for each neighbor
            for edge in edges:
                # Unpack the node names
                first_node, second_node = edge.split("-")

                # Get the coordinates of each node
                first_coordinates = self.environment.get_node_position(first_node)
                second_coordinates = self.environment.get_node_position(second_node)

                # Make a line
                plt.plot([first_coordinates[0], second_coordinates[0]], [first_coordinates[1], second_coordinates[1]],
                         'bs-', markersize=0.0)

            # Mark the interest nodes
            max_location = self.environment.get_node_position(self.max_node)
            plt.plot(max_location[0], max_location[1], 'c*', markersize=20.0, label="Max Node")

            min_location = self.environment.get_node_position(self.min_node)
            plt.plot(min_location[0], min_location[1], 'm*', markersize=20.0, label="Min Node")

            # Add the locations of every node in the graph
            # Uses the true positions in the environment
            node_positions_x = []
            node_positions_y = []
            for node_name in self.network.node_names():
                # Get the position of the node
                node_position = self.environment.get_node_position(node_name)

                # Add it to the list
                node_positions_x.append(node_position[0])
                node_positions_y.append(node_position[1])

            # Plot points
            plt.plot(node_positions_x, node_positions_y, 'ko', label="Nodes")

            # Plot the target location
            # Use the starting position, target is stationary for now
            target_position = self.environment.get_target_position()
            plt.plot(target_position[0], target_position[1], 'r*', markersize=20.0, label="Target")

            # Set the legend
            plt.legend(loc="best")

        # Plot the network prediction on another figure
        plt.figure(2)

        plt.title("Network predictions")

        plt.xlabel("Time")
        plt.ylabel("Prediction")

        # Get the target signal, network average, and interest node predictions
        target_signal = []
        network_prediction = []
        max_prediction = []
        min_prediction = []
        for item in self.info:
            # Target
            target_signal.append(item[0])

            # Network average
            network_prediction.append(item[2])

            # Max prediction
            max_prediction.append(item[4])

            # Min prediction
            min_prediction.append(item[5])

        # Network average
        plt.plot(network_prediction, 'b-', label="Network Average Prediction")

        # Max
        plt.plot(max_prediction, 'c-', label="Max Node Prediction")

        # Min
        plt.plot(min_prediction, 'm-', label="Min Node Prediction")

        # Target
        plt.plot(target_signal, 'r--', label="Target Signal")

        # Set the legend
        plt.legend(loc="best")

        print("Average of last 5 network predictions: ", np.average(network_prediction[-5:], axis=0), "\n\n")
        print("Displaying positions of nodes and the target")
        print("Displaying network output")
        print("Exit window to continue")

        # Show the graph
        plt.show()


if __name__ == "__main__":

    if len(sys.argv) > 1:
        # Get the fusion method
        consensus_method = sys.argv[1]

    else:

        consensus_method = "MaxDegree"

    # Seed the random function for reproducibility
    np.random.seed(50)

    sim = Simulate(3, default_consensus_method=consensus_method, target_reading_name="SinWave")

    num_iterations = 100

    if consensus_method == "WeightDesign2":
        num_iterations = 1000

    sim.run(num_iterations)

    sim.visualize()
