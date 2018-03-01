# encoding:utf-8
import networkx as nx
import matplotlib.pyplot as plt


class Network(object):
    def __init__(self, ):
        self.G = self.init_graph()

    @staticmethod
    def init_graph():
        graph = nx.DiGraph()
        with open("./data/data.in") as f:
            for line in f.readlines():
                tmp_input = line.strip('\n').split(' ')
                graph.add_node(int(tmp_input[0]), id=[], value=[], h_value=[], alpha=[], beta=[],
                               h_alpha=[], h_beta=[])
                graph.nodes[int(tmp_input[0])]['id'] = int(tmp_input[0])
                # graph.nodes[int(tmp_input[0])]['value'].append(tmp_input[2])
                # graph.nodes[int(tmp_input[0])]['h_value'].append(tmp_input[2])
                graph.nodes[int(tmp_input[0])]['alpha'] = float(tmp_input[1])
                graph.nodes[int(tmp_input[0])]['beta'] = float(tmp_input[2])
                graph.nodes[int(tmp_input[0])]['h_alpha'] = 1
                graph.nodes[int(tmp_input[0])]['h_beta'] = 0
                for num in range(3, len(tmp_input)):
                    graph.add_edge(int(tmp_input[0]), int(tmp_input[num]), state=1)
        return graph

    def get_neighbors_values(self, node, iter_time):
        neighbors_values = []
        for k, v in self.G.edges(node):
            neighbors_values.append(self.G.nodes[v]['value'][iter_time])
        return neighbors_values

    def show_network_graph(self):
        plt.figure(1)
        node_labels = nx.get_node_attributes(self.G, 'id')
        pos = nx.spring_layout(self.G)
        nx.draw_networkx_labels(self.G, pos, node_labels=node_labels)
        nx.draw(self.G, pos)
        plt.show()


if __name__ == '__main__':
    ss = Network()
    ss.show_network_graph()
