from csp import *
import globals
from killerSudokuUtilities import *
from collections import defaultdict
import globals

def killerSudoku_constraint(A, a, B, b):
    globals.constraintChecks += 1
    
    if A[0] == 'C' and B[0] == 'C':
        operant = globals.cageRelationships[(A, B)]
            
        if (get_truth(sum(a), operant, sum(b))):
            return True
        else:
            return False
    elif A[0] == 'C':    
        offset = -1
        for index in range(2, len(A) - 2, 4):
            offset += 1
            if A[index] == B[1] and A[index + 1] == B[2]:
                return (int(a[offset]) == int(b))
    elif B[0] == 'C':
        offset = -1
        for index in range(2, len(B) - 2, 4):
            offset += 1
            if B[index] == A[1] and B[index + 1] == A[2]:
                return (int(b[offset]) == int(a))
    else:
        return (a != b)

class KillerSudoku(CSP):
    """
    A Killer Sudoku Problem.
    """
    
    def __init__(self, inputFilename):
        """
        Build a Killer Sudoku problem from a text file representing the grid:
            The digits 1-9 denote a filled cell, '.' or '0' an empty one
            each digit or '.' is followed by a cage identifier in the form of CX, where X is the ID of the cage
            
            After the 9x9 grid the sums of each cage are displayed.
            
            Internally, the grid will be represented as a tuple of tuples each containing a tumple (number, blockID).
        
        Variables: Ordinary variables are represented as Xij, where i,j : row,column
                   Dual variables are represented as C<11>...<ij>...<99>, where ij is in the variable's name iff Xij 
                   is inside the cage being tested by this dual variable.
                   
        Domains: Ordinary variables take values from {1,...,9}
                 Dual variables take values from {((0,...,0),...,(x1,...,xn)}
                 
        Constraints: Amongst ordinary variables there is only different_value_contraint
                     Between a dual variable and an ordinary variable we have the constraint that 
                     the ordinary variable has the same value as it has inside the given tuple of the dual variable. 
        
        Greater than Killer Sudoku Representation:
            In the second half of the input file, next to each cageID we can comparisons with other cages as well.
        
        """        
        
        # Get grid from input and represent it.
        grid = ()
        with open(inputFilename) as f:
            # Loop until you find empty line.
            i = 1
            while True:
                gridLine = ()
                line = f.readline()
                if not line.strip():
                    break
                line = line.split()
                j = 1
                for group in line:
                    number = group[0] # {1,....,9}
                    if number != '.':
                        globals.alreadyAssignedVariables['X'+str(i)+str(j)] = int(number)
                    cageID = group[1:] # {'C' + '{1,....,N}'}
                    tuple = (number, cageID)
                    gridLine += (tuple, )
                    j += 1
                grid += (gridLine, )
                i += 1
            self.grid = grid
#             printGrid(grid)

            # Get block sums and relations and put them in two dictionaries: 
            #      1) blockID -> sum.     2) blockID -> list(relations)
            cageID_map = dict()
            cageRel_map = defaultdict(list)
            
            for line in f.readlines():
                line = line.strip('\n')
                if not line.strip():
                    break
                line = line.split(':')
                for arg in line[1].split(','):
                    cageID_map[str(line[0])] = True
                    if arg == '':
                        break
                    elif arg[0] in ('=<>'):
                        cageRel_map[str(line[0])].append(arg)
                    else:
                        cageID_map[str(line[0])] = int(arg)
                
        
            self.cageID_map = cageID_map
            self.cageRel_map = cageRel_map
#             printDictionary(cageID_map, "BlockID -> Sum")
#             printDictionary(cageRel_map, "BlockID -> Relations")
            
            
        
        self.generateVariables()
        
        self.domains = dict([(var, '123456789') for var in self.variables])
        self.removeAlreadyAssignedDomainValues()        
        
        self.generateNeighbors()
        
        self.generateDualVariablesAndDomains()
        
        self.addRelationConstraint()
        
#         printVariables(self.variables)
#         printDomains(self.domains)
#         printNeighbors(self.neighbors)
        
        CSP.__init__(self, list(self.variables), self.domains, self.neighbors,
                     killerSudoku_constraint)
        
        
        
    def generateVariables(self):
        var = []
        for i in range(1, 10):
            for j in range(1, 10):
                var.append('X' + str(i) + str(j))
        
#         for key in globals.alreadyAssignedVariables:
#             var.remove(key)
        self.variables = var        
    
    def generateNeighbors(self):
        neighbors = {}
        
        for i in range(1, 10):
            for j in range(1, 10):
                temp = 'X' + str(i) + str(j)
                
                if i in (1,4,7) and j in (1,4,7):
                    neighbors[temp] = []
                
                # Calculate row constraints.
                for j2 in range(1, 10):
                    if j2 != j:
                        temp2 = 'X' + str(i) + str(j2)
                        neighbors[temp].append(temp2)
                
                # Calculate column constraints.
                for i2 in range(1, 10):
                    if i2 != i:
                        temp3 = 'X' + str(i2) + str(j)
                        neighbors[temp].append(temp3)
                        
                if i in (1,4,7) and j in (1,4,7): # if we examine first element of a block.  
                    variableNames = []
                    variableNames.append('X'+str(i)+str(j))      
                    # Calculate block constraints.
                    R3 = range(3)
                    for offsetI in R3:
                        for offsetJ in R3:
                            if offsetI + offsetJ != 0:
                                variableNames.append('X' + str(i + offsetI) + str(j + offsetJ))
                                
                    neighbors = self.addNeighborsFromBlock(variableNames, neighbors)
                  
        self.neighbors = neighbors
    
    
    """ Already assigned variables from input do not need to get other assignments. """
    def removeAlreadyAssignedDomainValues(self):
        grid = self.grid
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                element = grid[i][j][0]
                if element != '.':
                    self.domains['X'+str(i+1)+str(j+1)] = element
    
    
    """ Gets the names of variables of a block and their names and adds to everyone's neighbors all the others. """
    def addNeighborsFromBlock(self, variableNames, neighbors):
        for i in range(len(variableNames)):
            if i != 0:
                neighbors[variableNames[i]] = []
            for j in range(len(variableNames)):
                if i != j:
                    neighbors[variableNames[i]].append(variableNames[j])
                    
        return neighbors
    
    
    """  Generates dual block constraints concerning the sum of each block """
    def generateDualVariablesAndDomains(self):
        cageID_map = self.cageID_map
        grid = self.grid
        
        cageName_map = dict()
        
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                if grid[i][j][1] not in cageName_map:
                    cageName_map[grid[i][j][1]] = "C<"+str(i + 1)+str(j + 1)+">"
                else:
                    cageName_map[grid[i][j][1]] += ("<"+str(i + 1)+str(j + 1)+">")
        
        self.cageName_map = cageName_map
        
        for key in cageName_map:
            value = cageName_map[key]
            
            self.variables.append(value)
            self.domains[value] = []
            
            for combination in getSumCombinations(len(value.replace('C','').split('<')) - 1, cageID_map[key]):
                self.domains[value].append(combination)  #if checkCombination(value, combination):
            
            self.neighbors[value] = []
        
            for var in value.replace('C','').replace('>','').split('<'):
                if var != '':
                    self.neighbors[value].append("X" + var) 
                    self.neighbors["X" + var].append(value)  
        
    """ Needed only for greater-than-killer sudokus """
    def addRelationConstraint(self):
        cageRel_map = self.cageRel_map
        
        for (key, value) in cageRel_map.items():
            for relation in value:
                operant = relation[0]
                cage = relation[1:]
                cage1 = self.cageName_map[key]
                cage2 = self.cageName_map[cage]
                # Add relationship
                globals.cageRelationships[(cage1, cage2)] = operant
                # Add neighbor connection
                self.neighbors[cage1].append(cage2)
                self.neighbors[cage2].append(cage1)
                
    
        self.cageRelationships = globals.cageRelationships
#         printDictionary(self.cageRelationships, "RELATIONSHIPS")