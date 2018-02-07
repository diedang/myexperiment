import networkx as nx
import matplotlib.pyplot as plt
import community

G = nx.erdos_renyi_graph(30, 0.05)
part = community.best_partition(G)
print(part)

i =0
for it in G.nodes():
    i = i+1
    G.node[it]['state'] = i
node_labels = nx.get_node_attributes(G, 'state')
pos = nx.spring_layout(G)
nx.draw_networkx_labels(G, pos, node_labels=node_labels)
nx.draw(G,pos)
plt.show()