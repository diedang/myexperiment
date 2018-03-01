import time

from Graph import Network
import matplotlib.pyplot as plt


class LCP(Network):

    def __init__(self, ):

        super(LCP, self).__init__()

    def consensus_alg(self, v, iter_time):
        new_value = self.G.node[v]['alpha'] * iter_time + self.G.node[v]['beta']
        self.G.node[v]['value'].append(new_value)
        if iter_time == 2 or iter_time == 3 or iter_time == 4:
            neighbors = self.G.neighbors(v)
            neighbor_values = self.get_neighbors_values(v, iter_time)
            neighbor_values.append(self.G.node[v]['value'][iter_time])
            for j in neighbors:
                t = (self.G.node[j]['value'][iter_time] - self.G.node[j]['value'][iter_time-1]) / (
                    self.G.node[v]['value'][iter_time] - self.G.node[v]['value'][iter_time-1])
                d = t * self.G.node[j]['h_alpha'] / self.G.node[v]['h_alpha']
                if d > 1:
                    self.G.node[v]['h_alpha'] = t * self.G.node[j]['h_alpha']
                    self.G.node[v]['h_beta'] = self.G.node[j]['h_value'][iter_time] - self.G.node[
                        v]['h_alpha'] * self.G.node[v]['value'][iter_time]
                elif d == 1:
                    self.G.node[v]['h_beta'] = max(self.G.node[v]['h_value'][iter_time], self.G.node[j]['h_value'][iter_time]
                                                   ) - self.G.node[v]['h_alpha'] * (self.G.node[v]['alpha'] * iter_time + self.G.node[v]['beta'])
        new_h_value = self.G.node[v]['h_alpha'] * (
                self.G.node[v]['alpha'] * iter_time + self.G.node[v]['beta']) + self.G.node[v]['h_beta']
        self.G.node[v]['h_value'].append(new_h_value)

    def run_consensus_alg(self, iter_time):
        for it in range(iter_time):
            for v in self.G.nodes():
                self.consensus_alg(v, it)

        self.show_network_graph()
        self.show_consensus(iter_time)

    def show_consensus(self, iter_time):
        x_axis = range(iter_time+1)
        plt.figure(time.time())
        plt.title('LCP')
        plt.xlabel('time')
        plt.ylabel('values')

        handle1 = 1
        handle2 = 2
        for i in range(1, 15):
            if i == 14:
                handle1, = plt.plot(x_axis, self.G.node[i]['h_value'])
            else:
                handle2, = plt.plot(x_axis, self.G.node[i]['h_value'])
        plt.legend(handles=[handle1, handle2], labels=['Malicious', 'Normal'], loc="best")
        plt.show()


if __name__ == '__main__':
    test = LCP()
    test.run_consensus_alg(200)
