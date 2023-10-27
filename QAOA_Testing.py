import networkx as nx
import numpy as np
from QAOA_Cost_Function import CostFunction
from QAOA_Scaffolding import QAOAScaffolding
from Helper_Functions import getBestMaxcut


v = 16
d = 3
l = 1

n = 1

for i in range(0, n):
    graph = nx.random_graphs.random_regular_graph(d, v, seed=1)
    classic_cut = nx.algorithms.approximation.one_exchange(graph)

    cost = CostFunction('maxcut', graph)
    best_cut = getBestMaxcut(cost, v)


    scaff = QAOAScaffolding(v, 'maxcut', graph)
    scaff.build(layers=l, mixerType='classic', initType='x_high_eigenstate', shots=1000)
    res = scaff.minimizeExectation('constant', 'scipy', saveHistory=True, measurementStrategy='average_expectation')
    

    qaoa_best = scaff.getExpectation(res.x, 'best_expectation')

    print(qaoa_best)

