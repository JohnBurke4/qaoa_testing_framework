import networkx as nx
import sys
sys.path.append(
    "/Users/johnburke/Desktop/QAOA Code/")

from qiskit import Aer, transpile
from scipy.optimize import minimize
from QAOA_Circuit import QAOACircuit
from QAOA_Cost_Function import CostFunction
import numpy as np

class Result:

    def __init__(self, fun, x, nfev):
        self.fun = fun
        self.x = x
        self.nfev = nfev

    def addHistory(self, history):
        self.history = history

class QAOAScaffolding:
    circuit = None
    simulator = None
    built = False

    def __init__(self, numQubits, problemType, problem):
        self.numQubits = numQubits
        self.problemType = problemType
        self.problem = problem

    def build(self, layers, mixerType, initType, shots):
        qc = QAOACircuit(self.numQubits, layers, mixerType, self.problem, self.problemType, initType)
        qc.build()
        self.layers = layers
        self.circuit = qc
        self.simulator = Aer.get_backend('qasm_simulator')
        self.shots = shots

        if ('maxcut' in self.problemType):
            cost = CostFunction(self.problemType, self.problem)
            self.costFunction = cost

        self.built = True

    def getExpectation(self, params, method = 'average_expectation'):
        qc = self.circuit.getCircuitWithParameters(params)
        
        qc = transpile(qc, backend=self.simulator)
        counts = self.simulator.run(qc, seed_simulator=10, shots=self.shots).result().get_counts()

        if method == 'best_expectation':
            return self.costFunction.getBestExpectation(counts)
        elif method == "most_common_expectation":
            return self.costFunction.getMostCommonExpectation(counts)
        

        return self.costFunction.getExpectation(counts)
    
    def minimizeExectation(self, initialParamsType = 'constant', minimizerType = 'scipy', customParameters = [], saveHistory = False, measurementStrategy = "average_expectation"):
         if (not self.built):
             print("Circuit not built")
             return False
         
         initialParams = []
         parameterCount = self.circuit.getNumberOfParameters()
         if (initialParamsType == 'constant'):
             initialParams = [1.0] * parameterCount
             

         elif (initialParamsType =='random'):
             initialParams = np.random.uniform(0.0, np.pi, parameterCount)

         elif (initialParamsType == 'custom'):
             initialParams = customParameters

         if (minimizerType == 'scipy'):
             return self.__scipyMinimize(initialParams, measurementStrategy)
         elif (minimizerType == 'brute_force'):
             return self.__bruteForceMinimize(parameterCount, saveHistory, measurementStrategy)
         elif (minimizerType == 'annealing'):
             return self.__annealingMinimize(initialParams, 1000, 1, saveHistory, measurementStrategy)
        
         
    
    def __scipyMinimize(self, initialParams, measurementStrategy = 'average_expectation'):
        res = minimize(self.getExpectation,
            initialParams,
            args=measurementStrategy,
            method='COBYLA')
        
        return res
    
    def __bruteForceMinimize(self, parameterCount, saveHistory = False, measurementStrategy = 'average_expectation'):
        possibleValues = 50
        values = np.linspace(0, np.pi / 2, possibleValues, endpoint=False)
        bestExpectation = 0
        bestParameters = []
        allValues = []
        
        for i in range(0, possibleValues ** parameterCount):
            parameters = [values[int(i / (possibleValues ** j)) % possibleValues] for j in range(0, parameterCount)]
            expectation = self.getExpectation(parameters, measurementStrategy)

            if (saveHistory):
                allValues.append((parameters, expectation))
            
            if (expectation < bestExpectation):
                bestExpectation = expectation
                bestParameters = parameters

        res = Result(bestExpectation, bestParameters, possibleValues ** parameterCount)

        if (saveHistory):
            res.addHistory(allValues)

        return res
    
    def __annealingMinimize(self, initialParams, temp, stepSize, saveHistory = False, measurementStrategy = 'average_expectation'):

        def temp_reduction(temp, alpha, type='linear', beta=1):
            if (type == 'linear'):
                return temp - alpha
            if (type == 'geometric'):
                return temp * alpha
            if (type == 'slow'):
                return (temp / (1 + beta * alpha))
        
        def perturb_params(params, curr_temp, max_temp):
            new_params = params.copy()
            max_terms_changed = int((curr_temp / max_temp)) * len(new_params)
            
            if (max_terms_changed <= 0):
                max_terms_changed = 1
                states_changed = max_terms_changed
            else:
                states_changed = np.random.randint(1, max_terms_changed)
            scale = (curr_temp / max_temp) * np.pi
            
            for i in range(states_changed):
                index = np.random.randint(0, len(new_params))
                new_params[index] = new_params[index] + np.random.uniform(-scale , scale)
            return np.array(new_params) % (np.pi / 2)
        
        curr_cost = self.getExpectation(initialParams, measurementStrategy)
        curr_temp = temp
        curr_params = initialParams
        niter = 0
        allValues = []
        while curr_temp > 1:
            niter += 1
            curr_temp = temp_reduction(curr_temp, stepSize)
            new_params = perturb_params(curr_params, curr_temp, temp)
            new_cost = self.getExpectation(new_params, measurementStrategy)

            if (saveHistory):
                allValues.append((new_params, new_cost))
            if (new_cost < curr_cost):
                curr_cost = new_cost
                curr_params = new_params
            else:
                cost_dif = (curr_cost - new_cost) * 1000
                prob = np.e ** (cost_dif / curr_temp)
                if (np.random.random() <= prob):
                    curr_cost = new_cost
                    curr_params = new_params

        res = Result(curr_cost, curr_params, niter)
        if (saveHistory):
            res.addHistory(allValues)

        return res



    
    




    
    
   


    

