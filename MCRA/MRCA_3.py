#encoding:utf-8
import random
import time

from Graph3 import Network_alg
import matplotlib.pyplot as plt

class MRCA_1(Network_alg):

    def __init__(self,vertex_num = 50):

        super(MRCA_1, self).__init__(vertex_num)

    def consensus_alg(self,v,iter_time):
        neighbors_values = self.get_neighbors_values(v,iter_time)
        neighbors_values.append(self.G.nodes[v]['state'][iter_time])
        neighbors_ids = self.get_neighbors_ids(v, iter_time)
        neighbors_ids.append(self.G.nodes[v]['id'])
        neighbors_min_values = 10
        neighbors_min_id = 0
        neighbors_max_values = 0
        neighbors_max_id = 0
        for i in range(len(neighbors_values)):
            if neighbors_min_values >= neighbors_values[i]:
                neighbors_min_values = neighbors_values[i]
                neighbors_min_id = neighbors_ids[i]
            if neighbors_max_values <= neighbors_values[i]:
                neighbors_max_values = neighbors_values[i]
                neighbors_max_id = neighbors_ids[i]

        if iter_time > 0:
            if v in self.malicious_node2 or v in self.malicious_node1:
                pass
            else:
                for ii in range(len(neighbors_ids)):
                    if self.G.nodes[v]['state'][iter_time] < self.G.nodes[neighbors_ids[ii]]['neih'][iter_time-1] or \
                                    self.G.nodes[v]['state'][iter_time] > self.G.nodes[neighbors_ids[ii]]['neiH'][iter_time - 1]:
                        if self.G.nodes[neighbors_ids[ii]]['state'][iter_time] < self.G.nodes[neighbors_ids[ii]]['neih'][iter_time-1] or \
                                        self.G.nodes[neighbors_ids[ii]]['state'][iter_time] > self.G.nodes[neighbors_ids[ii]]['neiH'][iter_time - 1]:
                            if v in self.malicious_node:
                                pass
                            else:
                                self.malicious_node.append(neighbors_ids[ii])
                                # for it in range(0,50):
                                #     if self.G.edges(neighbors_ids[ii]) != None and neighbors_ids[ii] != it:
                                #         print self.G.edges(neighbors_ids[ii])
                                #         print it
                                        # self.G.remove_edge(neighbors_ids[ii],it)
                                print '%d is a malicious node'%neighbors_ids[ii]
                                print iter_time



        if v in self.malicious_node1:
            self.G.nodes[v]['state'].append((neighbors_max_values+neighbors_min_values)*1.0/2 + 3)
        else:
            self.G.nodes[v]['state'].append((neighbors_max_values + neighbors_min_values) * 1.0 / 2)
        self.G.nodes[v]['neih'].append(neighbors_min_values)
        self.G.nodes[v]['neihid'].append(neighbors_min_id)
        self.G.nodes[v]['neiH'].append(neighbors_max_values)
        self.G.nodes[v]['neiHid'].append(neighbors_max_id)

        if v in self.malicious_node1:
            pass
        else:
            if self.G.nodes[v]['id'] == neighbors_min_id and neighbors_min_id != neighbors_max_id:
                if self.G.nodes[neighbors_min_id]['state'][iter_time] == self.G.nodes[v]['state'][iter_time] and \
                                self.G.nodes[v]['state'][iter_time+1] == (neighbors_max_values + neighbors_min_values) * 1.0 / 2:
                    pass
                else:
                    if v in self.malicious_node:
                        pass
                    else:
                        self.malicious_node.append(v)
                        print '%d is a malicious node' % v
                        print iter_time

            if self.G.nodes[v]['id'] == neighbors_max_id and neighbors_min_id != neighbors_max_id:
                if self.G.nodes[neighbors_max_id]['state'][iter_time] == self.G.nodes[v]['state'][iter_time] and \
                                self.G.nodes[v]['state'][iter_time + 1] == (
                            neighbors_max_values + neighbors_min_values) * 1.0 / 2:
                    pass
                else:
                    if v in self.malicious_node:
                        pass
                    else:
                        self.malicious_node.append(v)
                        print '%d is a malicious node' % v
                        print iter_time

            if self.G.nodes[v]['id'] != neighbors_min_id and self.G.nodes[v]['id'] != neighbors_max_id:
                if self.G.nodes[v]['state'][iter_time+1] == (neighbors_max_values + neighbors_min_values) * 1.0 / 2:
                    pass
                else:
                    if v in self.malicious_node:
                        pass
                    else:
                        self.malicious_node.append(v)
                        print '%d is a malicious node' % v
                        print iter_time


    def run_consensus_alg(self,iter_time):
        for it in range(iter_time):
            h = 10
            H = 0
            for v in self.G.nodes():
                self.consensus_alg(v,it)
                if v in self.malicious_node:
                    pass
                else:
                    if h >self.G.nodes[v]['state'][it]:
                        h = self.G.nodes[v]['state'][it]
                    if H < self.G.nodes[v]['state'][it]:
                        H = self.G.nodes[v]['state'][it]
            self.D.append(H-h)


        self.show_network_graph()
        self.show_consensus(iter_time)

    def show_consensus(self, iter_time):
        x = range(iter_time)
        plt.figure(time.time())
        plt.title('SDA with two attacks')
        plt.plot(x, self.D)
        plt.legend()
        plt.savefig('doc/result3.png')
        plt.show()


def main():
    test = MRCA_1(vertex_num= 50)
    test.run_consensus_alg(300)

if __name__ == '__main__':
    main()