# encoding:utf-8
import time

from Graph import Graph
import matplotlib.pyplot as plt


class Wmsr(Graph):

    def __init__(self, ):

        super(Wmsr, self).__init__()

    def get_real_neighbor_values(self, v, iter_time, cur_value, f):
        neighbor_values = self.get_neighbors_values(v, iter_time)
        neighbor_values.append(self.G.node[v]['value'][iter_time])
        neighbor_values.sort()

        index_front = 0
        while index_front < f:
            if neighbor_values[index_front] < cur_value:
                index_front += 1
            else:
                break

        index = 0
        index_end = len(neighbor_values)-1
        while index < f:
            if neighbor_values[index_end] > cur_value:
                index_end -= 1
                index += 1
            else:
                break
        return neighbor_values[index_front:index_end + 1]

    def consensus_alg(self, v, iter_time):
        if v == 5 or v == 6:
            if iter_time == 0:
                self.G.node[v]['value'].append(0)
            else:
                self.G.node[v]['value'].append(self.G.node[v]['value'][iter_time] + 0.01)
        else:
            cur_value = self.G.node[v]['value'][iter_time]
            neighbor_values = self.get_real_neighbor_values(v=v, iter_time=iter_time, cur_value=cur_value, f=2)
            weighted_sum = 0
            for j in neighbor_values:
                t = 1.0 / (len(neighbor_values))
                weighted_sum += t * j
            self.G.node[v]['value'].append(weighted_sum)
        print(self.G.node[v]['value'][iter_time])

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
    test = Wmsr()
    test.run_consensus_alg(200)
