from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

class Mixer:

    circuit = {}

    def __init__(self, numQubits, layers=1, mixerType='classic'):
        self.numQubits = numQubits
        self.mixerType = mixerType
        self.layers = layers

    def build(self):
        self.circuit = {}

        for l in range(0, self.layers):
            if (self.mixerType == 'classic'):
                circuitDetails = self.__buildClassic(l)
                self.circuit[l] = circuitDetails
            elif (self.mixerType == "ma_classic"):
                circuitDetails = self.__buildMAClassic(l)
                self.circuit[l] = circuitDetails

        return True
    
    def getCircuitAtLayer(self, l):
        return self.circuit[l]
    
    def getAllCircuits(self):
        return self.circuit

    
    def __buildClassic(self, l):
        theta = Parameter('mix_cl_' + str(l))

        qc = QuantumCircuit(self.numQubits)
        for qubit in range(0, self.numQubits):
            qc.rx(2 * theta, qubit)

        return (qc, [theta])
    
    def __buildMAClassic(self, l):
        theta = [Parameter('mix_cl_' + str(l) + "_" + str(i)) for i in range(0, self.numQubits)]

        qc = QuantumCircuit(self.numQubits)
        for qubit in range(0, self.numQubits):
            qc.rx(2 * theta[qubit], qubit)

        return (qc, theta)


    