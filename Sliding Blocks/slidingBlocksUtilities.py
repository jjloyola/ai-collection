'''
Created on Nov 15, 2014

@author: Orestis Melkonian
'''

from sets import Set
import random

""" 
Prints the given state of the sliding blocks game.
"""
def printState(state):
    sizeX = getSize(state)[0]
    
    line = ' '
    for _ in range(sizeX):
        line += '_____'

    print line 
    
    for row in state:
        print '|',
        for element in row:
            if element < 10:
                print element, ' |',
            else:
                print element, '|',
        print
        print line
        
"""
Calculates the size of a given state.
Returns the tuple (rows, columns), where the state is a grid [rows X columns]
"""
def getSize(state):
    rows = 0
    columns = 0
    
    for row in state:
        rows += 1
        if rows == 1:
            for _ in row:
                columns += 1
            
    
    return (rows, columns)
    


"""
Returns the number of blocks contained in the given state.
"""
def getBlockNumber(state):
    
    numberSet = Set()
    
    
    for row in state:
        for element in row:
            if element not in numberSet and element != 0:
                numberSet.add(element)
    
    
    return len(numberSet)
    

"""
Calculates the dimentions of the block with the given {blockNo}.
Returns a tuple (sizeX, sizeY).
"""
def getBlockSize(blockNo, state): 
    
    sizeX = 0
    sizeY = 0
    
    yFlag = False
    
    # Calculate sizeX
    for i in state:
        for j in i:
            if j == blockNo:
                sizeY += 1
                yFlag = True
        if yFlag:
            break
    
    # Calculate sizeY
    for i in state:
        for j in i:
            if j == blockNo:
                sizeX += 1
                break
    
    return (sizeX, sizeY)
                

"""
Returns a list containing the symbols representing all the blocks of the grid.
"""
def getBlockSymbolsList(state):
    symbols = Set()
    
    for i in state:
        for j in i:
            if j != 0 and j not in symbols:
                symbols.add(j)
    
    return list(symbols)




"""
Returns all valid actions available at the given state.
"""     
def getValidActions(state):
    
    validActions = []
    
    # Get valid actions for every block number/symbol.
    for symbol in getBlockSymbolsList(state):
        # Check 'up'
        if checkIfValid((symbol ,'up'), state):
            validActions.append((symbol, 'up'))
        # Check 'down'
        if checkIfValid((symbol ,'down'), state):
            validActions.append((symbol, 'down'))
        # Check 'left'
        if checkIfValid((symbol ,'left'), state):
            validActions.append((symbol, 'left'))
        # Check 'right'
        if checkIfValid((symbol ,'right'), state):
            validActions.append((symbol, 'right'))
            
    return validActions
    
    
    
"""
Returns True, if the given action in the given state is valid.
"""
def checkIfValid(action, state):
    # For every occurence of the block number/symbol, check if any direction is possible.
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == action[0]:
                if action[1] == 'up':
                    if i == 0:
                        return False
                    if state[i - 1][j] != 0 and state[i - 1][j] != action[0]:
                        return False 
                if action[1] == 'down':
                    if i == len(state) - 1:
                        return False
                    if state[i + 1][j] != 0 and state[i + 1][j] != action[0]:
                        return False
                if action[1] == 'left':
                    if j == 0:
                        return False
                    if state[i][j - 1] != 0 and state[i][j - 1] != action[0]:
                        return False
                if action[1] == 'right': 
                    if j == len(state[i]) - 1:
                        return False
                    if state[i][j + 1] != 0 and state[i][j + 1] != action[0]:
                        return False
                    
                    
    return True

"""
Selects randomly more than half of the symbols given.
"""
def selectMoreThanHalfRandomly(symbols):
    half = len(symbols)/2 + random.randint(0, len(symbols)/2)
    symbols = set(symbols)
    
    
    for _ in range(half):
        symbols.discard(random.choice(list(symbols)))
        
    return list(symbols)

"""
Selects randomly half of the symbols given.
"""
def selectHalfRandomly(symbols):
    half = len(symbols)/2
    symbols = set(symbols)
    
    
    for _ in range(half):
        symbols.discard(random.choice(list(symbols)))
        
    return list(symbols)

"""
Converts a non-goal block(yellow) to spaces.
"""
def convertToSpace(state, blockSymbol):
    state = convertTupleToList(state)
    
    for i in range(len(state)):
        for j in range(len(state[i])):
            if state[i][j] == blockSymbol:
                state[i][j] = 0
                
    return convertListToTuple(state)


"""
Crops the grid to only the area containing the final goal block(red block)
Returns the cropped grid.
"""
def cropGoalPosition(state):
    goalBlockDimentions = getBlockSize(1, state)
    croppedState = ()
    
    for i in range(len(state) - goalBlockDimentions[0], len(state)):
        temp = ()
        for j in range(0, goalBlockDimentions[1]):
            temp += (state[i][j], )
        croppedState += (temp, )
        
    return croppedState

"""
Calculate Manhattan Distance to leftmost-down corner.
Returns the distance.
"""
def calculateManhattanDistance(state, position):
    x = position[0]
    y = position[1]
    
     
    return abs((len(state) - 1 ) - x) + y  
    

"""
Returns the leftmost-down corner of the block with symbol {symbol}.
"""    
def getLeftmosDownCornerPositionOfBlock(state, symbol):
    
    for i in range(len(state)):
        for j in range(len(state[i])):
            # Get a tile containing the given symbol
            if state[i][j] == symbol:
                # Walk to the lowest row
                for k in range(i, len(state)):
                    if state[k][j] != symbol:
                        k -= 1
                        break
        
                for l in reversed(range(j + 1)):
                    if state[k][l] != symbol:
                        l += 1
                        break
                
                return (k, l)
    

"""
Swaps two values in the grid. 
"""
def swawValuesInGrid(state, position1, position2):
    pos1x = position1[0]
    pos1y = position1[1]
    
    pos2x = position2[0]
    pos2y = position2[1]
    
    temp = state[pos2x][pos2y]
    
    arrayState = convertTupleToList(state)
    
    arrayState[pos2x][pos2y] = arrayState[pos1x][pos1y]
    arrayState[pos1x][pos1y] = temp
    
    return convertListToTuple(arrayState)
    
    
def getDistanceOutOfGoalBlock(state, position):
    (blockX, blockY) = getBlockSize(1, state)
    
    # Get distance from lowest left corner of the non-goal block. 
    (x, y) = getLeftmosDownCornerPositionOfBlock(state, state[position[0]][position[1]])
    
    
    distanceX = x - len(state) + 1 + blockX
    distanceY = blockY - y

    
    return min(distanceX, distanceY)
    
    
def isNotInGoalBlock(state, position):
    (x, y) = position
    (blockX, blockY) = getBlockSize(1, state)
    
    if x < len(state) - 1 - blockX and y > blockY:
        return True
    
    
def convertTupleToList(tuple1) :
    ret = []
    for i in tuple1 :
        ret.append(list(i))
    return ret;

def convertListToTuple(list1) :
    ret = ()
    for i in list1 :
        ret += (tuple(i), )
    return ret;

def getInitialStateFromText(inputText) :
    initialState = ()
    
    for line in inputText :
        initialState += (tuple([int(s) for s in line.split() if s.isdigit()]), )
    
    return initialState






