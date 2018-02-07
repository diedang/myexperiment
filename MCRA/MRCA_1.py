#encoding:utf-8
import time

from Graph import Network_alg
import matplotlib.pyplot as plt

class MRCA_1(Network_alg):

    def __init__(self,vertex_num = 50):

        super(MRCA_1, self).__init__(vertex_num)

    def consensus_alg(self,v,iter_time):
        neighbors_values = self.get_neighbors_values(v,iter_time)
        neighbors_values.append(self.G.nodes[v]['state'][iter_time])
        neighbors_min_values = 10
        neighbors_max_values = 0
        for i in range(len(neighbors_values)):
            if neighbors_min_values > neighbors_values[i]:
                neighbors_min_values = neighbors_values[i]
            if neighbors_max_values < neighbors_values[i]:
                neighbors_max_values = neighbors_values[i]
        self.G.nodes[v]['state'].append((neighbors_max_values+neighbors_min_values)*1.0/2)



    def run_consensus_alg(self,iter_time):
        for it in range(iter_time):
            h = 10
            H = 0
            for v in self.G.nodes():
                self.consensus_alg(v,it)
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
        plt.title('MRCA without attacks')
        plt.plot(x, self.D)
        plt.legend()
        plt.savefig('doc/result1.png')
        plt.show()


def main():
    test = MRCA_1(vertex_num= 50)
    test.run_consensus_alg(300)

if __name__ == '__main__':
    main()