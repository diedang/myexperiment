# encoding:utf-8
import time

from Graph import Network
import matplotlib.pyplot as plt


class Wmsr(Network):

    def __init__(self,):

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
        if v == 14:
            if iter_time == 0:
                self.G.node[v]['value'].append(0)
            else:
                self.G.node[v]['value'].append(self.G.node[v]['value'][iter_time] + 0.01)
        else:
            cur_value = self.G.node[v]['value'][iter_time]
            neighbor_values = self.get_real_neighbor_values(v=v, iter_time=iter_time, cur_value=cur_value, f=1)
            weighted_sum = 0
            for j in neighbor_values:
                t = 1.0 / (len(neighbor_values))
                weighted_sum += t * j
            self.G.node[v]['value'].append(weighted_sum)

    def run_consensus_alg(self, iter_time):
        for it in range(iter_time):
            for v in self.G.nodes():
                self.consensus_alg(v, it)

        self.show_network_graph()
        self.show_consensus(iter_time)

    def show_consensus(self, iter_time):
        x_axis = range(iter_time+1)
        plt.figure(time.time())
        plt.title('w_msr')
        plt.xlabel('time')
        plt.ylabel('values')

        handle1 = 1
        handle2 = 2
        for i in range(1, 15):
            if i == 14:
                handle1, = plt.plot(x_axis, self.G.node[i]['value'])
            else:
                handle2, = plt.plot(x_axis, self.G.node[i]['value'])
        plt.legend(handles=[handle1, handle2], labels=['Malicious', 'Normal'], loc="best")
        plt.show()


if __name__ == '__main__':
    test = Wmsr()
    test.run_consensus_alg(200)
