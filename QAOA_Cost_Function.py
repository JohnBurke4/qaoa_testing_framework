from qiskit import transpile

class CostFunction:

    def __init__(self, problemType, problem):
        self.problemType = problemType
        self.problem = problem

    def getCost(self, value):
        if ('maxcut' in self.problemType):
            return self.__getCostMaxcut(value)
        
        return 0
    
    def getExpectation(self, counts):
        avg = 0
        sum_count = 0
        for bit_string, count in counts.items():
            obj = self.getCost(bit_string)
            avg += obj * count
            sum_count += count
        return avg/sum_count
    
    def getBestExpectation(self, counts):
        return min([self.getCost(x) for x in counts.keys()])
    
    def getMostCommonExpectation(self, counts):
        return self.getCost(max(counts, key=counts.get))

    
    def getDesiredExpectation(self, counts):

        best = sorted(counts.keys(), key=lambda x: self.getCost(x))[0]
        print(best, self.getCost(best) * 1000 - counts[best])

        return self.getCost(best) * 1000 - counts[best]

 


    def __getCostMaxcut(self, partition):
        score = 0
    
        for edge in self.problem.edges():
            v1 = edge[0]
            v2 = edge[1]
            if partition[v1] != partition[v2]:
                score-=1

        return score
