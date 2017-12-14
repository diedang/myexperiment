# encoding：utf-8
import time

from Graph import Graph
import matplotlib.pyplot as plt


class Lcp(Graph):

    def __init__(self, ):
        super(Lcp, self).__init__()

    def consensus_alg(self, v, iter_time):
        if v == 5 or v == 6:
            if iter_time == 0:
                self.G.node[v]['value'].append(0)
            else:
                self.G.node[v]['value'].append(self.G.node[v]['value'][iter_time] + 0.1)
        else:
            neighbors = self.G.neighbors(v)
            neighbor_values = self.get_neighbors_values(v, iter_time)
            neighbor_values.append(self.G.node[v]['value'][iter_time])
            weighted_sum = self.G.node[v]['value'][iter_time] * (1.0/(len(neighbor_values)))
            for j in neighbors:
                t = 1.0 / (len(neighbor_values))
                weighted_sum += t * self.G.node[j]['value'][iter_time]
            self.G.node[v]['value'].append(weighted_sum)

    def run_consensus_alg(self, iter_time):
        for it in range(iter_time):
            for v in self.G.nodes():
                self.consensus_alg(v, it)

        self.show_network_graph()
        self.show_consensus(iter_time)

    def show_consensus(self, iter_time):
        x = range(iter_time + 1)
        plt.figure(time.time())
        plt.title('W_msr')
        plt.xlabel('time')
        plt.ylabel('values')

        for i in self.G.nodes():
            plt.plot(x, self.G.nodes[i]['value'], label=u'node%d' % i)
        plt.legend(loc=1)
        plt.show()


if __name__ == '__main__':
    test = Lcp()
    test.run_consensus_alg(200)
