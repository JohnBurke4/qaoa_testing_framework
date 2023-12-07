import random
import os

def getClauses(filename):
    numOfVars = 0
    numOfClauses = 0
    clauses = []
    location = os.path.abspath("3SatProblems/" + filename)
    f = open(location, "r")
    for line in f.readlines():
        if (line[0] == "c"):
            continue
        
        sp = line.split(" ")
        if (len(sp) < 3):
            continue
        sp = [x for x in sp if x != ""]
        if (sp[0] == "p"):
            numOfVars = int(sp[2])
        else:
            currClause = ["X"] * numOfVars
            for i in range(0, 3):
                currChar = sp[i]
                isNegative = False
                if ('-' in currChar):
                    isNegative = True
                    
                    currChar = int(currChar) * -1
                
                currChar = int(currChar)-1
                if (isNegative):
                    currClause[currChar] = "1"
                else:
                    currClause[currChar] = "0"

            clauses.append(currClause)
    return (clauses, numOfVars)

                


        

clauses, numOfVars = getClauses("UUF50.218.1000/uuf50-01.cnf")

def getMaxDifferentLiterals(clauses):
    groups3 = {}
    groups2 = {}
    groups1 = {}
    for c in clauses:
        loc = [i for i in range(0, len(c)) if c[i] != "X"]
        loc = tuple(loc)

        loc2 = [(loc[0], loc[1]), (loc[0], loc[2]), (loc[1], loc[2])]
        for l in loc2:
            if (l in groups2):
                groups2[l] += 1
            else:
                groups2[l] = 1

        for l in loc[0:1]:
            if (l in groups1):
                groups1[l] += 1
            else:
                groups1[l] = 1



        if (loc in groups3):
            groups3[loc] += 1
        else:
            groups3[loc] = 1
    print(len(groups1.keys()))
    print(groups1.values())

# getMaxDifferentLiterals(clauses)
clauses.sort()

        


def getValidSolutions(guess, clause):
    validSolutions = []
    indexes = []
    for i in range(0, len(clause)):
        v1 = guess[i]
        v2 = clause[i]
        if (v1 != "X" and v2 != "X"):
            if (v1 != v2):
                return [guess]
            
        if (v1 == "X" and v2 != "X"):
            indexes.append((i, v2))
    
    
    vals = []  
    if (len(indexes) == 0):
        return []
    for i in range(0, 2**len(indexes)):
        binary = "{0:b}".format(i)
        binary = "0" * (len(indexes) - len(binary)) + binary
        vals += [binary]
        
    badVal = ""
    for v in indexes:
        # print("V:", v)
        badVal += v[1]
        
    # print("Vals:", vals)
    # print(badVal)
    vals.remove(badVal)
    for i in vals:
        guessCopy = guess.copy()
        for j in range(0, len(indexes)):
            guessCopy[indexes[j][0]] = i[j]
            
        validSolutions.append(guessCopy)
        
    # print("Valid:", validSolutions)
        
    return validSolutions

def getValidSolutionsCount(guess, clause):
    validSolutions = []
    indexes = []
    for i in range(0, len(clause)):
        v1 = guess[i]
        v2 = clause[i]
        if (v1 != "X" and v2 != "X"):
            if (v1 != v2):
                return 1
            
        if (v1 == "X" and v2 != "X"):
            indexes.append((i, v2))
    
    
    
    if (len(indexes) == 0):
        return 0
    
        
    return 2**len(indexes) - 1





maxSize = 0
maxSolSize = 0
n = numOfVars
avNumOfSolutions = 0
startNumber = 10
c = len(clauses)
minStack = 10000
for i in range(0, 1):
    startNumber = i
    if (i % 10 == 0):
        print(i)
    
    
    
        
#     # clauses.sort(reverse=True)
#     # for c in clauses:
#     #     print(c)

    guesses = [["X"] * numOfVars]
    
    maxStack = 0
    
    
    clausesCopy = clauses.copy()
    tooBig = False
    removedClauses = []

    # for c in clauses:
    #     print(c)
    

    for j in range(0, 3):
        clause = clauses[j]
        bestClause = 0
        maxSizeIncrease = 20
        bestGuesses = []
        # for k in range(0, len(clausesCopy)): 
        #     newGuesses = 0
        #     clause = clausesCopy[k]
        #     for guess in guesses:
        #         newGuesses += getValidSolutionsCount(guess, clause)
                
        #     sizeIncrease = newGuesses / len(guesses)
        #     if (maxSizeIncrease > sizeIncrease):
        #         maxSizeIncrease = sizeIncrease
        #         bestClause = k
        #     if (sizeIncrease < 1):
        #         bestClause = k
        #         break
        # if (j == 0):
        #     bestClause = startNumber
        # if (len(clausesCopy) > 0):
        #     clause =  clausesCopy[bestClause]
        #     removedClauses.append(clause)
        for guess in guesses:
            bestGuesses += getValidSolutions(guess, clause)
            # del clausesCopy[bestClause]

        for c in bestGuesses:
            print(c)
        # print(bestGuesses)
            
        guesses = bestGuesses
        print(len(guesses))
        
        if (len(guesses) > maxStack):
            maxStack = len(guesses)
        if (len(guesses) > maxSize):
            maxSize = len(guesses)
        if (len(guesses) == 0):
            print("Finished")
            for c in removedClauses:
                print(c)
            break
            
        # if (len(guesses) > 2000):
        #     # print("Stack too big, skipping")
        #     tooBig = True
        #     break
        
    if (maxStack < minStack):
        minStack = maxStack      
        # print(len(guesses))
    if (len(guesses) > maxSolSize):
        maxSolSize = len(guesses)
    avNumOfSolutions += len(guesses)
    
    # print(guesses)
    if (not tooBig):
        print("Max Stack:", maxStack)
        
        totalSolSize = 0
        for guess in guesses:
            num2s = len([x for x in guess if x =="X"])
            totalSolSize += 2**num2s
        print("Num Of Sols:", totalSolSize)
        print("---------")
    
print("Max Stack Size:", maxSize)
print("Min Stack Size:", minStack)
print("Max Sol Size:", maxSolSize)
print("Average Sol Size:", avNumOfSolutions/100)


