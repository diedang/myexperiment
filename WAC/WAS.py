#encoding:utf-8
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time


class Network_alg(object):

    def __init__(self,vertex_num = 10, network_file = None,vertex_value_file = None, adjMatrix = None,DeMatrix = None, VaMatrix = None):

        self.adjMatrix = self.init_Network_adj(vertex_num, network_file) if not adjMatrix else adjMatrix.copy()
        self.DeMatrix = self.init_Network_De(vertex_num, network_file) if not DeMatrix else DeMatrix.copy()
        self.VaMatrix = self.init_Network_Va(vertex_num, vertex_value_file) if not VaMatrix else VaMatrix.copy()
        self.G = self.init_graph(self.adjMatrix)
        self.init_vertex_value(self.G, vertex_value_file)

    @staticmethod
    def init_Network_adj(vetex_num = 10, file_name = None):
        '''

        :param vetex_num:
        :param file_name:
        :return:
        '''
        local_adjMatrix = None
        if not file_name:
            pass
        else:
            with open(file_name, 'r') as fd:
                x = 0
                for line in fd.readlines():
                    t = line.split(' ')
                    x += 1
                    if x == 1:
                        v = int(t[0])
                        local_adjMatrix = np.zeros([v, v], dtype = np.int)
                        continue
                    else:
                        for i in range(1,len(t)):
                            local_adjMatrix[int(t[0])-1][int(t[i])-1] =1
        return local_adjMatrix

    @staticmethod
    def init_Network_De(vetex_num=10, file_name=None):
        '''

        :param vetex_num:
        :param file_name:
        :return:
        '''
        local_DeMatrix = None
        if not file_name:
            pass
        else:
            with open(file_name, 'r') as fd:
                x = 0
                for line in fd.readlines():
                    t = line.split(' ')
                    x += 1
                    if x == 1:
                        v = int(t[0])
                        local_DeMatrix = np.zeros([v, v], dtype=np.int)
                        continue
                    else:
                        local_DeMatrix[x - 2][x - 2] = len(t) - 1
        return local_DeMatrix

    @staticmethod
    def init_Network_Va(vetex_num=10, file_name=None):
        '''

        :param vetex_num:
        :param file_name:
        :return:
        '''
        local_VaMatrix = np.zeros([10, 1],dtype=np.float)
        if not file_name:
            pass
        else:
            with open(file_name, 'r') as fd:
                x = 0
                for line in fd.readlines():
                    t = line.split(' ')
                    local_VaMatrix[x,0] = float(t[1])
                    x += 1
        return local_VaMatrix

    @staticmethod
    def init_graph(local_adjMatrix):
        '''
        :param local_adjMatrix:
        :return:
        '''
        local_G = nx.DiGraph()
        for i in range(local_adjMatrix.shape[0]):
            for j in range(local_adjMatrix.shape[1]):
                if local_adjMatrix[i][j] != 0:
                    local_G.add_edge(i+1, j+1)
        return local_G

    @staticmethod
    def init_vertex_value(local_G, file_name = None):
        '''
        :param local_G:
        :param file_name:
        :return:
        '''
        if not isinstance(local_G, nx.Graph):
            return  False

        for v in local_G.nodes():
            local_G.nodes[v]['lan'] = []
            local_G.nodes[v]['lan1'] = []
            local_G.nodes[v]['lan2'] = []

        with open(file_name, 'r') as fd:
            for line in fd.readlines():
                z = line.split(' ')
                local_G.nodes[int(z[0])]['value'] = [float(z[1])]

        return True


    def get_neighbors_values(self):
        pass

    def show_network(self):
        plt.figure(time.time())
        for v in self.G.nodes():
            self.G.nodes[v]['state'] = str(v)

        node_labels = nx.get_node_attributes(self.G, 'state')
        pos = nx.spring_layout(self.G)
        nx.draw_networkx_labels(self.G, pos, node_labels = node_labels)
        nx.draw(self.G, pos)
        plt.savefig('picture/graph.png')
        plt.close()


class WACS_alg(Network_alg):

    def __init__(self, vertex_num = 10, network_file = None, vertex_value_file = None):
        '''

        :param vertex_num:
        :param network_file:
        :param vertex_value_file:
        '''

        super(WACS_alg, self).__init__(vertex_num, network_file, vertex_value_file)


    def standard_consensus_alg(self, iter_time):
        L = self.DeMatrix - self.adjMatrix
        I = np.eye(10)
        c = np.mat([2, 1, 3, 1, 0, 1, 0.5, 2, 0.3, 1])
        lanm = np.zeros([10,1],dtype = float)

        for i in range(1,11):
            node_lan = 0
            node_lan1 = 0
            node_lan2 = 0
            neighbors_value = []
            for k, v in self.G.in_edges(i):
                neighbors_value.append(self.G.nodes[k]['value'][iter_time])
            neighobrs_num = len(neighbors_value)
            if iter_time == 0:
                for it in range(neighobrs_num):
                    node_lan1 = node_lan1 + abs(self.G.nodes[i]['value'][iter_time] - neighbors_value[it])
                    if node_lan < abs(  self.G.nodes[i]['value'][iter_time] - neighbors_value[it]):
                        node_lan = abs(self.G.nodes[i]['value'][iter_time] - neighbors_value[it])
                self.G.nodes[i]['lan'].append(node_lan)
                self.G.nodes[i]['lan1'].append(node_lan1)
                self.G.nodes[i]['lan2'].append(node_lan)
                lanm[i-1,0] = node_lan
            else:
                for it in range(neighobrs_num):
                    node_lan1 = node_lan1 + abs(self.G.nodes[i]['value'][iter_time] - neighbors_value[it])
                    if node_lan2 < abs(self.G.nodes[i]['value'][iter_time] - neighbors_value[it]):
                        node_lan2 = abs(self.G.nodes[i]['value'][iter_time] - neighbors_value[it])
                if self.G.nodes[i]['lan1'][iter_time-1] == 0:
                    node_lan = 0
                else:
                    node_lan = (node_lan1*1.0 / self.G.nodes[i]['lan1'][iter_time-1])*self.G.nodes[i]['lan'][iter_time-1]
                lanm[i-1,0] = node_lan
                self.G.nodes[i]['lan'].append(node_lan)
                self.G.nodes[i]['lan1'].append(node_lan1)
                self.G.nodes[i]['lan2'].append(node_lan2)

        k = np.zeros([10,1],dtype=float)
        if iter_time > 0:
            for i in range(1,11):
                for j in range(1,11):
                    if abs(self.G.nodes[i]['value'][iter_time]-self.G.nodes[j]['value'][iter_time]) > self.G.nodes[i]['lan'][iter_time-1]:
                        if L[i-1,j-1] != 0:
                            L[i-1,j-1] = 0
                            L[i-1,i-1] = L[i-1, i-1]-1


        # for i in range(10):
        #     k[i,0] = L[i,5]*lanm[5,0]
        k[5,0] = lanm[5,0]

        print k

        e = 1.0 / (iter_time + 1)


        # self.VaMatrix = np.dot(I - e * L, self.VaMatrix)-1.0/2*e*np.multiply(np.dot(I - e * L, c.T), k)

        self.VaMatrix = np.dot(I - 1.0/5 * L, self.VaMatrix) - 1.0/2*e*np.multiply(np.dot(I - e * L, c.T), k)
        #数据篡改
        self.VaMatrix[3,0] = 13
        # print (np.dot(I - e * L, c.T)*lanm[5,0])

        for i in range(1,11):
            self.G.nodes[i]['value'].append(self.VaMatrix[i-1,0])
        # print self.VaMatrix

    def run_standard_consensus_alg(self, iter_time):
        for i in range(iter_time):
            self.standard_consensus_alg(i)

        self.show_network()
        self.show_consensus(iter_time)

    def show_consensus(self, iter_time):
        x = range(iter_time + 1)
        plt.figure(time.time())
        plt.title('standard')
        for n in self.G.nodes():
            plt.plot(x, self.G.nodes[n]['value'], label=u'node%d' % n)
        plt.legend(loc=1)
        y_ticks = np.arange(3, 13, 1)
        plt.yticks(y_ticks)
        plt.savefig('picture/result1.png')
        plt.show()


def main():
    test = WACS_alg(vertex_num=10, network_file='data.in', vertex_value_file='value.in')
    test.run_standard_consensus_alg(100)



if __name__ == '__main__':
    main()