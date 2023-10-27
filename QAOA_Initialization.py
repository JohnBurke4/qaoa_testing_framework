from qiskit import QuantumCircuit


class QAOAInit:

    circuit = {}

    def __init__(self, numQubits, layers=1, initType='x_high_eigenstate'):
        self.numQubits = numQubits
        self.initType = initType
        self.layers = layers

    def build(self):
        self.circuit = {}

        for l in range(0, self.layers):
            if (self.initType == 'x_low_eigenstate'):
                circuitDetails = self.__buildXLowEigenstate(l)
                self.circuit[l] = circuitDetails
            elif (self.initType == 'x_high_eigenstate'):
                circuitDetails = self.__buildXHighEigenstate(l)
                self.circuit[l] = circuitDetails

        return True
    
    def getCircuitAtLayer(self, l):
        return self.circuit[l]
    
    def getAllCircuits(self):
        return self.circuit

    
    def __buildXLowEigenstate(self, l):

        qc = QuantumCircuit(self.numQubits)
        qc.x(range(0, self.numQubits))
        qc.h(range(0, self.numQubits))

        return (qc, [])
    
    def __buildXHighEigenstate(self, l):

        qc = QuantumCircuit(self.numQubits)
        qc.h(range(0, self.numQubits))

        return (qc, [])

