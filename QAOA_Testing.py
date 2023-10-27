import networkx as nx
import numpy as np
from QAOA_Cost_Function import CostFunction
from QAOA_Scaffolding import QAOAScaffolding
from Helper_Functions import getBestMaxcut


v = 16
d = 3
l = 1

n = 10

testing = 1
classicAverageAR = 0
qaoaAverageAR = [0] * testing


for i in range(0, n):
    graph = nx.random_graphs.random_regular_graph(d, v, seed=i)
    cost = CostFunction('maxcut', graph)
    bestCut = getBestMaxcut(cost, v)
    classicCut = nx.algorithms.approximation.one_exchange(graph)[0]
   
    classicAverageAR += (-classicCut / bestCut) / n


    scaff = QAOAScaffolding(v, 'maxcut', graph)
    scaff.build(layers=l, mixerType='classic', initType='x_high_eigenstate', shots=1000)
    res = scaff.minimizeExectation('constant', 'scipy', saveHistory=True, measurementStrategy='average_expectation')
    

    qaoaCut = scaff.getExpectation(res.x, 'best_expectation')

    qaoaAverageAR[0] += (qaoaCut / bestCut) / n



print("Classsic Average:", classicAverageAR)
print("QAOA Average:", qaoaAverageAR[0])



