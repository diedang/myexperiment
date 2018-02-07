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



    @staticmethod
    def init_graph(vertex_num):
        random_list = list(itertools.product(range(0, 101, 14), range(0, 101, 14)))
        x = random.sample(random_list, vertex_num)
        local_G = nx.DiGraph()
        for it in range(0, 50):
            local_G.add_node(it)
            local_G.nodes[it]['id'] = it
            local_G.nodes[it]['coord'] = x[it]
            local_G.nodes[it]['state'] = [random.randint(1, 10)]

        for i in range(0, 50):
            for j in range(0, 50):
                d = math.sqrt(math.pow(local_G.nodes[i]['coord'][0] - local_G.nodes[j]['coord'][0], 2) + math.pow(
                    local_G.nodes[i]['coord'][1] - local_G.nodes[j]['coord'][1], 2))
                if 0 < d and d <= 15:
                    local_G.add_edge(i, j, weight = d)
        return local_G

    def get_neighbors_values(self,node,iter_time):
        neighbors_values = []
        for k,v in  self.G.edges(node):
            neighbors_values.append(self.G.nodes[v]['state'][iter_time])
        return neighbors_values

    def show_network_graph(self):
        plt.figure(1)
        node_labels = nx.get_node_attributes(self.G, 'id')
        x = []
        for i in range(0,50):
            x.append(self.G.nodes[i]['coord'])
        pos = x
        nx.draw_networkx_labels(self.G,pos, node_labels=node_labels)
        nx.draw(self.G, pos, node_size=100, node_color = 'yellow')
        plt.savefig('doc/network_graph.png')
        plt.show()

if __name__ == '__main__':
    ss = Network_alg(vertex_num=50)
    ss.show_network_graph()



# n = 50
# random_list = list(itertools.product(range(0,101,14),range(0,101,14)))
# x = random.sample(random_list,n)
# G = nx.Graph()
# for it in range(0,50):
#     G.add_node(it)
#     G.nodes[it]['id'] = it
#     G.nodes[it]['coord']  = x[it]
#     G.nodes[it]['state'] = random.randint(1,10)
#
# for i in range(0,50):
#     for j in range(0,50):
#         d = math.sqrt(math.pow(G.nodes[i]['coord'][0]-G.nodes[j]['coord'][0],2)+math.pow(G.nodes[i]['coord'][1]-G.nodes[j]['coord'][1],2))
#         if 0<d and d<=15:
#             G.add_edge(i,j)
#
#
# plt.figure(1)
# node_labels = nx.get_node_attributes(G,'id')
# pos = x
# nx.draw_networkx_labels(G, pos, node_labels = node_labels )
# nx.draw(G,pos,node_size = 100)
# plt.show()
