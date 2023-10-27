
def getBestMaxcut(costFunction, v):
    bestCut = 0
    for i in range(0, 2**v):
        partition = bin(i)
        partition = partition[2:]
        partition = "0" * (v - len(partition)) + partition
        cut = costFunction.getCost(partition)
        if (cut < bestCut):
            bestCut = cut
    return bestCut

    