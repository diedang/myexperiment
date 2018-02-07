#encoding:utf-8
import networkx as nx
import itertools
import random
import math
import matplotlib.pyplot as plt
import time

import numpy as np


class Network_alg(object):

    def __init__(self,vertex_num = 50,):
        self.G = self.init_graph(vertex_num)
        self.D = []
        self.malicious_node = []
        self.malicious_node1 = [1]
        self.malicious_node2 = [2,40]



    @staticmethod
    def init_graph(vertex_num):
        x = [(42, 98), (0, 56), (0, 70), (0, 84), (56, 56), (28, 84),(56, 28), (0, 28), (56, 84), (84, 70), (28, 14), (70, 42),(98, 28),
             (84, 28), (98, 14), (28, 98), (56, 0), (70, 84), (56, 42), (70, 70), (42, 0), (14, 42), (14, 14), (70, 98),(14, 28),
             (56, 14), (42, 28), (84, 42), (42, 14), (0, 98), (98, 98), (0, 0), (84, 14), (70, 56), (0, 14), (28, 42), (70, 28),(98, 70),
             (98, 56), (14, 98), (14, 56), (84, 56), (98, 84), (14, 70), (28, 56), (28, 28), (84, 84),(28, 70), (84, 0), (42, 42)]
        local_G = nx.Graph()
        for it in range(0, 50):
            local_G.add_node(it)
            local_G.nodes[it]['id'] = it
            local_G.nodes[it]['coord'] = x[it]
            local_G.nodes[it]['state'] = [random.randint(1, 10)]
            local_G.nodes[it]['neih'] = []
            local_G.nodes[it]['neihid'] = []
            local_G.nodes[it]['neiH'] = []
            local_G.nodes[it]['neiHid'] = []

        for i in range(0, 50):
            for j in range(0, 50):
                d = math.sqrt(math.pow(local_G.nodes[i]['coord'][0] - local_G.nodes[j]['coord'][0], 2) + math.pow(
                    local_G.nodes[i]['coord'][1] - local_G.nodes[j]['coord'][1], 2))
                if 0 < d and d <= 15:
                    local_G.add_edge(i, j)
                    local_G[i][j]['flag'] = 1
        return local_G

    def get_neighbors_values(self,node,iter_time):
        neighbors_values = []
        for k,v in  self.G.edges(node):
            if v in self.malicious_node1:
                pass
            else:
                neighbors_values.append(self.G.nodes[v]['state'][iter_time])
        return neighbors_values

    def get_neighbors_ids(self,node,iter_time):
        neighbors_ids = []
        for k,v in  self.G.edges(node):
            if v in self.malicious_node1:
                pass
            else:
                neighbors_ids.append(self.G.nodes[v]['id'])
        return neighbors_ids

    def show_network_graph(self):
        plt.figure(1)
        node_labels = nx.get_node_attributes(self.G, 'id')
        colors = []
        x = []
        for i in range(0,50):
            x.append(self.G.nodes[i]['coord'])
            if i in self.malicious_node1:
                colors.append('y')
            elif i in self.malicious_node2:
                colors.append('b')
            else:
                colors.append('r')

        pos = x
        nx.draw_networkx_labels(self.G,pos, node_labels=node_labels)
        nx.draw(self.G, pos, node_size=100, node_color = colors)
        plt.savefig('doc/network_graph4.png')
        plt.show()

if __name__ == '__main__':
    ss = Network_alg(vertex_num=50)
    ss.show_network_graph()