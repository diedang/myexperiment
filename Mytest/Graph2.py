# encoding:utf-8
import networkx as nx
import matplotlib.pyplot as plt
import community

class Graph(object):

    def __init__(self, ):
        self.G = self.init_graph()

    @staticmethod
    def init_graph():
        graph = nx.Graph()
        with open("./data/data2.in") as f:
            for line in f.readlines():
                tmp_input = line.strip('\n').split(' ')
                graph.add_node(int(tmp_input[0]), id=[], value=[])
                graph.nodes[int(tmp_input[0])]['id'] = int(tmp_input[0])
                graph.nodes[int(tmp_input[0])]['value'].append(float(tmp_input[1]))
                for num in range(2, len(tmp_input)):
                    graph.add_edge(int(tmp_input[0]), int(tmp_input[num]), weight = 1)

        for i, t in graph.edges():
            s = abs(graph.nodes[i]['value'][0]-graph.nodes[t]['value'][0])
            if s <= 0.001:
                x = 100
            else:
                x = abs(1.0/s)
            graph.edges[i,t]['weight'] = int(x)
        # graph.add_node(0, id = [], value = [], minvalue = [], maxvalue = [])
        # edges = graph.edges()
        #
        # bernoulli_flips = np.random.binomial(n=1, p=.5, size=len(edges))
        # for index, flag in enumerate(bernoulli_flips):
        #     edge = edges[index]
        #     if flag == 1:
        #         graph.edge[edge[0]][edge[1]]['state'] = 0
        #     else:
        #         graph.edge[edge[0]][edge[1]]['state'] = 1
        return graph

    def get_neighbors_values(self, node, iter_time):
        neighbors_values = []
        for k, v in self.G.edges(node):
            neighbors_values.append(self.G.nodes[v]['value'][iter_time])
        return neighbors_values

    def show_network_graph(self):
        node_labels = nx.get_node_attributes(self.G, 'id')
        pos = nx.random_layout(self.G)
        nx.draw_networkx_labels(self.G, pos, node_labels=node_labels)
        nx.draw(self.G, pos)
        plt.show()


if __name__ == '__main__':
    ss = Graph()
    part = community.best_partition(ss.G, weight= 'weight')
    print(part)
    print(part[10])
    ss.show_network_graph()
