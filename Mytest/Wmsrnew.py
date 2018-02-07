# encoding:utf-8
import time

from Graph2 import Graph
import matplotlib.pyplot as plt
import community


class Wmsrnew(Graph):

    def __init__(self, ):

        super(Wmsrnew, self).__init__()

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
            if iter_time%4 == 0:
                self.G.node[v]['value'].append(4)
            else:
                self.G.node[v]['value'].append(8)

        else:
            cur_value = self.G.node[v]['value'][iter_time]
            neighbor_values = self.get_real_neighbor_values(v=v, iter_time=iter_time, cur_value=cur_value, f=2)
            weighted_sum = 0
            for j in neighbor_values:
                t = 1.0 / (len(neighbor_values))
                weighted_sum += t * j
            self.G.node[v]['value'].append(weighted_sum)
        # print(self.G.node[v]['value'][iter_time])

        if iter_time == 100:
            for i, t in self.G.edges():
                s = abs(self.G.nodes[i]['value'][100] - self.G.nodes[t]['value'][100])
                if s <= 0.01:
                    x = 100
                else:
                    x = abs(1.0 / s)
                self.G.edges[i, t]['weight'] = int(x)
            part = community.best_partition(test.G, weight='weight')
            local_dict = {}
            tt = []
            for i in part.keys():
                if part[i] in local_dict:
                    local_dict[part[i]].append(i)
                else:
                    local_dict[part[i]] = [i]
            for k in local_dict.keys():
                if len(local_dict[k]) > 1:
                    tt.append(k)
            for n in self.G.nodes():
                for m in self.G.nodes():
                    if n in local_dict[0] and m in local_dict[3]:
                        self.G.add_edge(n, m)


    def run_consensus_alg(self, iter_time):
        for it in range(iter_time):
            for v in self.G.nodes():
                self.consensus_alg(v, it)

        self.show_network_graph()
        self.show_consensus(200)

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
    test = Wmsrnew()
    test.run_consensus_alg(200)
    # for i, t in test.G.edges():
    #     s = abs(test.G.nodes[i]['value'][100] - test.G.nodes[t]['value'][100])
    #     if s <= 0.01:
    #         x = 100
    #     else:
    #         x = abs(1.0 / s)
    #     test.G.edges[i, t]['weight'] = int(x)
    # part = community.best_partition(test.G, weight='weight')
    # print(part)
    # local_dict = {}
    # tt = []
    # for i in part.keys():
    #     if part[i] in local_dict:
    #         local_dict[part[i]].append(i)
    #     else:
    #         local_dict[part[i]] = [i]
    # for k in local_dict.keys():
    #     if len(local_dict[k]) > 1:
    #         tt.append(k)
    # for n in test.G.nodes():
    #     for m in test.G.nodes():
    #         for s in range(len(tt)):
    #             if n in local_dict[tt[s]] and m not in local_dict[tt[s]]:
    #                     test.G.add_edge(n,m)
