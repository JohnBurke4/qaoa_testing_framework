import networkx as nx
import numpy as np
from QAOA_Cost_Function import CostFunction
from QAOA_Scaffolding import QAOAScaffolding
from Helper_Functions import getBestMaxcut, custom_graphs, ry_simulator, greedyMaxcutSolver
import matplotlib.pyplot as plt


v = 12
d = 5
l = 1

n = 1


testing = 1
classicAverageAR = 0
greedyAverageAR = 0
qaoaAverageAR = [0] * testing

AverageAR1 = 0
AverageAR2 = 0

allProbBoosts = []
allAR = []
xAxis = []

for j in range(3, 4,  1):
    xAxis.append(j)
    AvProbBoost = 0
    AverageAR1 = 0
    nP = n
    for i in range(1, n+1):
        # v = j
        graph = nx.random_graphs.random_regular_graph(d, v, seed=3)

        # graph = nx.random_graphs.erdos_renyi_graph(v, 0.7, seed=i)
        
        # graph = custom_graphs()
        cost = CostFunction('maxcut', graph)
        bestCut, bestP = getBestMaxcut(cost, v)
        # print(bestP)
        if (bestCut == 0):
            nP -=1
            continue
        print(bestCut, len(graph.edges))
        classicCut = nx.algorithms.approximation.one_exchange(graph)[0]

        edges = len(graph.edges())
        

        scaff = QAOAScaffolding(v, 'ry_maxcut', graph)
        scaff.build(layers=l, mixerType='none', initType='x_high_eigenstate', shots=10000)
        # print(scaff.circuit.circuit.decompose())
        res1 = scaff.minimizeExectation('constant', 'ry_custom', saveHistory=False, measurementStrategy='average_expectation', graph=graph)

        # print(res1.x)
        # res2 = scaff.minimizeExectation('constant', 'y_custom_2', saveHistory=False, measurementStrategy='average_expectation')
        x = res1.x
        print(x)
        # best1 , probBoost= scaff.getExpectation(x, "best_expectation", goal=bestCut, randomGuess=len(bestP)/2**v)
        # print(probBoost)

        
        # print(scaff.getExpectation(x, "best_expectation"))
        # best2 = scaff.getExpectation(res2.x, "best_expectation")
        # x = [np.pi/2, np.pi/2, 0, 0, np.pi/2, 0, np.pi/2, 0, 0]

        # best = scaff.getExpectation(res.x, "best_expectation")
        # print(best)

        print((res1.fun), bestCut, i)
        # print((res2.fun), bestCut, i)
        # # print(best2, res2.fun)
        # print(bestCut, -classicCut)

        # classicAverageAR += (-classicCut) / bestCut / n
        AverageAR1 += (res1.fun) / bestCut
        # AvProbBoost += probBoost
    # AverageAR2 += (best2) / bestCut / n
    
    AvProbBoost = AvProbBoost / nP
    AverageAR1 = AverageAR1 / nP
    # print(AvProbBoost, j, AverageAR1)
    allAR.append(AverageAR1)
    # allProbBoosts.append(-np.log2(AvProbBoost))


    


    




# print(count)

# plt.plot(xAxis, allAR)
# plt.plot(xAxis, allProbBoosts)
# plt.show()
# print("AR 2 :", AverageAR2)
# print("Classic AR:", YAverageAR)



