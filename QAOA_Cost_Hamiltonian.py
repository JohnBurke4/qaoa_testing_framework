from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

class CostHamiltonian:

    circuit = {}

    def __init__(self, numQubits, layers=1, costType='maxcut', problem=None):
        self.numQubits = numQubits
        self.costType = costType
        self.layers = layers
        self.problem = problem

    def build(self):
        self.circuit = {}

        for l in range(0, self.layers):
            if (self.costType == 'maxcut'):
                circuitDetails = self.__buildMaxcutLayer(self.problem, l)
                self.circuit[l] = circuitDetails

            elif (self.costType == 'ma_maxcut'):
                circuitDetails = self.__buildMAMaxcutLayer(self.problem, l)
                self.circuit[l] = circuitDetails

        return True
    
    def getCircuitAtLayer(self, l):
        return self.circuit[l]
    
    def getAllCircuits(self):
        return self.circuit

    
    def __buildMaxcutLayer(self, graph, l):
        theta = Parameter('cost_maxcut_' + str(l))

        qc = QuantumCircuit(self.numQubits)
        for edge in graph.edges():
            qc.rzz(theta, edge[0], edge[1])
        return (qc, [theta])
    
    def __buildMAMaxcutLayer(self, graph, l):
        theta = [Parameter('cost_maxcut_' + str(l) + "_" + str(i)) for i in range(0, len(graph.edges()))]

        qc = QuantumCircuit(self.numQubits)
        i = 0
        for edge in graph.edges():
            qc.rzz(theta[i], edge[0], edge[1])
            i+=1
        return (qc, theta)