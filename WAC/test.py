#encoding:utf-8

import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import time


class Network_alg(object):

    def __init__(self, vertex_num = 10, network_file = None, vertex_vlue_file = None,vertex_dei_file = None,adjMatrix = None):
        '''
        :param vertex_num:
        :param network_file:
        :param vertex_vlue_file:
        :param adjMatrix:
        '''
        self.adjMatrix = self.init_network(vertex_num,network_file) if not adjMatrix else adjMatrix.copy()
        self.G = self.init_graph(self.adjMatrix)
        self.init_vertex_value(self.G, vertex_vlue_file)
        self.init_vertex_dei(self.G, vertex_dei_file)
        self.malicious_node = [6]


    @staticmethod
    def init_network(vertex_num = 10, file_name = None):
        '''

        :param vertex_num:
        :param file_name:
        :return:local_adjMatrix
        '''
        local_adjMatrix = None
        if not file_name:
            pass
        else:
            with open(file_name,'r') as fd:
                for line in fd.readlines():
                    tt =  line.split(' ')

                    if len(tt) == 1:
                        vv = int(tt[0])
                        local_adjMatrix = np.zeros([vv,vv],dtype=np.int)
                        continue

                    for i in range(1,len(tt)):
                        local_adjMatrix[int(tt[0])-1][int(tt[i])-1] = 1
        return local_adjMatrix

    @staticmethod
    def init_graph(local_adjMatrix):
        '''
        :param local_adjMatrix:
        :return:
        '''
        local_G = nx.Graph()
        for i in range(local_adjMatrix.shape[0]):
            for j in range(local_adjMatrix.shape[1]):
                if local_adjMatrix[i][j] != 0:
                    local_G.add_edge(i + 1, j + 1)
        return local_G

    @staticmethod
    def init_vertex_value(local_G, file_name=None):
        '''

        :param local_G:
        :param file_name:
        :return:
        '''

        if not isinstance(local_G, nx.Graph):
            return False

        if not file_name:
            pass
        else:
            with open(file_name,'r') as fd:
                for line in fd.readlines():
                    tt = line.split(' ')
                    local_G.nodes[int(tt[0])]['value'] = [float(tt[1])]
        return True

    @staticmethod
    def init_vertex_dei(local_G, file_name = None):
        '''

        :param local_G:
        :param file_name:
        :return:
        '''
        if not isinstance(local_G, nx.Graph):
            return False

        if not file_name:
            for v in local_G.nodes():
                local_G.nodes[v]['dei'] = []
                local_G.nodes[v]['dei1'] = []
                local_G.nodes[v]['dei2'] = []
        else:
            with open(file_name, 'r') as fd:
                for line in fd.readlines():
                    dd = line.split(' ')
                    local_G.nodes[int(dd[0])]['dei'] = [float(dd[1])]
        return True


    @staticmethod
    def write_adjMatrix_to_file():
        pass

    def set_malicious_node(self,):
        pass


    def get_neighbors_values(self, node, iter_time):
        neighbors_values = []
        for k, v in self.G.edges(node):
            neighbors_values.append(self.G.nodes[v]['value'][iter_time])
        return neighbors_values

    def get_dei(self, node,iter_time):
        deierta = []
        x = 0
        for k, v in self.G.edges(node):
            if x < abs(self.G.nodes[node]['value'][iter_time]-self.G.nodes[v]['value'][iter_time]):
                x = abs(self.G.nodes[node]['value'][iter_time]-self.G.nodes[v]['value'][iter_time])
        deierta.append(x)
        return deierta


    def show_network(self):
        plt.figure(time.time())
        for v in self.G.nodes():
            self.G.nodes[v]['state'] = str(v)

        node_labels = nx.get_node_attributes(self.G, 'state')
        pos = nx.spring_layout(self.G)
        nx.draw_networkx_labels(self.G, pos, node_labels = node_labels)
        nx.draw(self.G, pos)
        plt.savefig('picture/networkgraph.png')
        plt.close()






class SDC_alg(Network_alg):

    def __init__(self, vertex_num = 10, network_file = None,vertex_dei_file = None, vertex_value_file = None):
        '''

        :param vertex_num:
        :param network_file:
        :param vertex_value_file:
        '''
        super(SDC_alg, self).__init__(vertex_num, network_file, vertex_value_file, vertex_dei_file)



    def standard_consensus_alg(self,v,iter_time):

        neighbors_values = self.get_neighbors_values(v, iter_time)
        self.G.nodes[v]['dei'].append(self.get_dei(v,iter_time)[0])
       # dei1 = self.G.nodes[v]['dei'][0]
        c = np.mat([2, 1, 3, 1, 0, 1, 0.5, 2, 0.3, 1])
        I = np.mat([[1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 1, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 1, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]])
        L = np.mat([[2, -1, -1, 0, 0, 0, 0, 0, 0, 0],
                    [-1, 2, 0, -1, 0, 0, 0, 0, 0, 0],
                    [-1, 0, 3, -1, -1, 0, 0, 0, 0, 0],
                    [0, -1, -1, 4, -1, -1, 0, 0, 0, 0],
                    [0, 0, -1, -1, 4, -1, 0, 0, -1, 0],
                    [0, 0, 0, -1, -1, 4, -1, -1, 0, 0],
                    [0, 0, 0, 0, 0, -1, 2, -1, 0, 0],
                    [0, 0, 0, 0, 0, -1, -1, 3, 0, -1],
                    [0, 0, 0, 0, -1, 0, 0, 0, 2, -1],
                    [0, 0, 0, 0, 0, 0, 0, -1, -1, 2]])
        #print neighbors_values
        neighbors_num = len(neighbors_values)
        #print neighbors_num
        nei_val = 0
        dei1 = 0
        #init_dei =

        print '第%d次迭代,节点%d' % (iter_time, v)

        for it in range(neighbors_num):
            nei_val = neighbors_values[it] + nei_val
            dei1 = dei1 + abs(self.G.nodes[v]['value'][iter_time]-neighbors_values[it])
        self.G.nodes[v]['dei1'].append(dei1)
        print '它的值为%s' % (self.G.nodes[v]['value'][iter_time])

        if iter_time == 0:
            self.G.nodes[v]['dei2'].append(self.G.nodes[v]['dei'][iter_time])
        else:
            self.G.nodes[v]['dei2'].append((self.G.nodes[v]['dei1'][iter_time] / self.G.nodes[v]['dei1'][iter_time-1])* (self.G.nodes[v]['dei2'][iter_time-1]))
        print '阈值为%f' % (self.G.nodes[v]['dei2'][iter_time])
        if iter_time > 0:
            if self.G.nodes[v]['dei2'][iter_time] > self.G.nodes[v]['dei2'][iter_time-1]:
                print '%d is a malicious_node' % v
        x1 = 0

        x = np.multiply(I - (1.0 / (iter_time+1)) * L,  c)
        for i in range(10):
             x1 = x[v-1,i]+x1

        print x1
        times = iter_time + 1
        if v in self.malicious_node:
            self.G.nodes[v]['value'].append(
                (self.G.nodes[v]['value'][iter_time] * (times - neighbors_num)) / times + nei_val / times + 1.0/(iter_time+1)*x1*self.G.nodes[v]['dei2'][iter_time])
        else:
            self.G.nodes[v]['value'].append(
                (self.G.nodes[v]['value'][iter_time] * (times - neighbors_num)) / times + nei_val / times)
        # if v in self.malicious_node:
        #     self.G.nodes[v]['value'].append((self.G.nodes[v]['value'][iter_time] * (6.0 - neighbors_num)) / 6.0 + nei_val / 6.0 + 1.0/(iter_time+1)*x1*self.G.nodes[v]['dei2'][iter_time])
        # else:
        #     self.G.nodes[v]['value'].append((self.G.nodes[v]['value'][iter_time] * (6.0 - neighbors_num)) / 6.0 + nei_val / 6.0  )


        # if v == 10 :
        #     t = [0,0,0,0,0,0,0,0,0,0]
        #     for i in range(1,11):
        #         t[i-1] = c[0,i-1] * self.G.nodes[i]['dei2'][iter_time]
        #         print t
        #
        #     x1 = np.multiply(I - (1.0 / (iter_time + 1)) * L,t)
        #     x2 = 0
        #     for ii in range(10):
        #         for io in range(10):
        #             x2 = x1[ii,io]+ x2
        #         print x2
        #         self.G.nodes[ii+1]['value'][iter_time] = self.G.nodes[ii+1]['value'][iter_time] + x2
        #         x2 = 0




    def run_standard_consensus_alg(self, iter_time):
        for it in range(iter_time):
            for v in self.G.nodes():
                self.standard_consensus_alg(v, it)

        print 'ok standard'
        self.show_network()
        self.show_consensus(iter_time)

    def show_consensus(self, iter_time):
        x = range(iter_time+1)

        plt.figure(time.time())
        plt.title('standard')
        for n in self.G.nodes():
            plt.plot(x,self.G.nodes[n]['value'], label = u'node%d' % n )
        plt.legend(loc = 1)
        y_ticks = np.arange(3, 13, 1)
        plt.yticks(y_ticks)
        plt.savefig('picture/result1.png')
        plt.show()




def main():
    test = SDC_alg(vertex_num=10,network_file='data.in',vertex_value_file='value.in')
    #test.set_malicious_node({6:1})
    test.run_standard_consensus_alg(100)




if __name__ == '__main__':
    main()