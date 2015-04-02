from itertools import combinations_with_replacement, permutations
import operator
from globals import alreadyAssignedVariables

def printGrid(grid):
    print '=================================================='
    print '              Printing Grid'
    print '=================================================='
    for row in grid:
        for tuple in row:
            if len(tuple[1]) == 2:
                print tuple[0], tuple[1], '  ',
            else:
                print tuple[0], tuple[1], ' ',
        print
    print
    print
        
def printDomains(domains):
    print '=================================================='
    print '               Printing Domains'
    print '=================================================='
    for key in domains:
        print key, ' ---> ', domains[key]
    print
    print
        
        
def printVariables(variables):
    print '=================================================='
    print '               Printing Variables (',len(variables),')'
    print '=================================================='
    for var in variables:
        print var
    print
    print
        
def printNeighbors(neighbors):
    print '=================================================='
    print '               Printing Neighbors'
    print '=================================================='
    for key in neighbors:
        print key, ' ---> ', neighbors[key]
    print
    print

def printDictionary(dictionary, dictName):
    print '=================================================='
    print '               ', dictName, ' (', len(dictionary), ')'
    print '=================================================='
    for key in dictionary:
        print key, ' ---> ', dictionary[key]
    print
    print
    
def printSolution(solution):
    print '=================================================='
    print '               SOLUTION'
    print '=================================================='
    if solution != None:
        for key in solution:
            print key, " --> ", solution[key]
    else:
        print "No solution found"


def getSumCombinations(variableNo, targetSum):
    ret = set()
    for combo in permutations(range(1,10),variableNo):
        if sum(combo) == targetSum or targetSum == True:
            ret.add(combo)
    return ret

def checkCombination(cageName, combination):
    global alreadyAssignedVariables
    offset = -1
    for index in range(2, len(cageName) - 2, 4):
        offset += 1
        variableName = 'X' + cageName[index] + cageName[index + 1]
        if variableName in alreadyAssignedVariables and alreadyAssignedVariables[variableName] != combination[offset]:
            return False
    
    return True
    
    
def get_truth(val1, relate, val2):
    ops = {'>': operator.gt,
           '<': operator.lt,
           '>=': operator.ge,
           '<=': operator.le,
           '=': operator.eq}
    return ops[relate](val1, val2)