import time

from Graph import Network_alg
import matplotlib.pyplot as plt

class LCP(Network_alg):

    def __init__(self, vertex_num = 14):

        super(LCP, self).__init__(vertex_num)


    def consensus_alg(self,v,iter_time):
        if v == 14:
            if iter_time == 0:
                self.G.node[v]['value'].append(0)
            else:
                self.G.node[v]['value'].append(self.G.node[v]['value'][iter_time] + 0.01)
        else:
            neighbors = self.G.neighbors(v)
            neighbor_values = self.get_neighbors_values(v,iter_time)
            neighbor_values.append(self.G.node[v]['value'][iter_time])
            weighted_sum = self.G.node[v]['value'][iter_time] * (1.0/(len(neighbor_values)))
            for j in neighbors:
                t = 1.0 / (len(neighbor_values))
                weighted_sum += t * self.G.node[j]['value'][iter_time]
            self.G.node[v]['value'].append(weighted_sum)


    def run_consensus_alg(self,iter_time):
        for it in range(iter_time):
            for v in self.G.nodes():
                self.consensus_alg(v,it)

        self.show_network_graph()
        self.show_consensus(iter_time)


    def show_consensus(self, iter_time):
        x = range(iter_time)
        plt.figure(time.time())
        plt.title('LCP')
        plt.xlabel('time')
        plt.ylabel('values')

        x_axis = range(201)
        handle1 = 1
        handle2 = 2
        for i in range(1,15):
            if i == 14:
                handle1, = plt.plot(x_axis, self.G.node[i]['value'])
            else:
                handle2, = plt.plot(x_axis, self.G.node[i]['value'])
        plt.legend(handles=[handle1, handle2], labels=['Malicious', 'Normal'], loc="best")
        plt.show()




if __name__ == '__main__':
    test = LCP(vertex_num=14)
    test.run_consensus_alg(200)