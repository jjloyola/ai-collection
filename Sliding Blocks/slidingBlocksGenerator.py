
"""
Generates a random grid with the given size and number of non-goal blocks
derived {steps} steps from a random goal state.
 
Size is given as a tuple (X,Y).
"""
from slidingBlocksUtilities import convertTupleToList, getSize,convertListToTuple,\
    getValidActions, printState, getBlockSymbolsList,\
    getLeftmosDownCornerPositionOfBlock, getBlockSize
import random
from math import ceil, floor
from slidingBlocks import SlidingBlock


def generateSlidingBlockGrid(size):
    
    grid = None
    
    grid = convertTupleToList(generateGrid(size, 0))
    goalBlock = generateGoalBlock(size)
#     grid = insertGoalBlockInEmptyGrid(goalBlock, grid)
    grid = insertGoalBlockInStartPosition(goalBlock, grid) #{DIFFICULT}
    
    i = 2
    while getSpaceNumber(grid) > max(getSize(goalBlock)[0], getSize(goalBlock)[1]) + size[0]: #{DIFFICULT}
#     while getSpaceNumber(grid) > (size[0]+size[1]):   
        newBlock = generateNonGoalBlock(size, i)
        if getInsertPosition(newBlock, grid) != (-1, -1):
            grid = insertNonGoalBlock(newBlock, grid, i)
        else:
            continue
        
        i += 1            
    
#     grid = performNSteps(grid, steps)

    if not checkIfGoalTileIsInUpperLeftHalfgrid(grid):
        return generateSlidingBlockGrid(size)
    else:
        return grid



#_______________________RANDOM ACTIONS OPERATIONS____________________________________________
    
def performNSteps(grid, n):
    temp = SlidingBlock(grid)
    
    for _ in range(n):
        validActions = getValidActions(grid)
        
        
        tempBool = False
        # Consider moving the red block first.
        for action in validActions:
            if action[0] == 1 and action[1] != 'down' and action[1] != 'left':
                grid = temp.result(grid, action)
                tempBool = True
                break
        
        # Consider moving a yellow block down or left.
        if not tempBool:
            for action in validActions:
                if action[0] != 1 and (action[1] == 'down' or action[1] == 'left'):
                    grid = temp.result(grid, action)
                    tempBool = True
                    break
        
        if validActions != [] and not tempBool:
            action = random.choice(validActions)
            grid = temp.result(grid, action)
        
    return grid
    
    
def performNRandomSteps(grid, n):
    temp = SlidingBlock(grid)
    
    count = 0
    while True:
        count += 1
        validActions = getValidActions(grid)
        
        if validActions != []:
            action = random.choice(validActions)
            grid = temp.result(grid, action)
            
            if checkIfGoalTileIsInUpperLeftHalfgrid(grid):
                break
            else:
                if count > 1000:
                    for symbol in getBlockSymbolsList(grid):
                        if checkIfAnyTileIsInUpperLeftHalfgrid(grid, symbol):
                            grid = exchangeBlock(grid, 1, symbol)
                continue
                    
    
    return grid
     

    

#______________________________GENERATION OPERATIONS__________________________________________________
         
def generateNonGoalBlock(sizeOfState, symbol):
    offset = 1 + sizeOfState[0]/3
    blockX = random.randint(1, sizeOfState[0] - offset)
    blockY = random.randint(1, sizeOfState[1] - offset)
    
    sizeOfBlock = (blockX, blockY)
    
    return generateGrid(sizeOfBlock, symbol)

def generateGoalBlock(sizeOfState):
    offset = 1 + sizeOfState[0]/3
    blockX = random.randint(1, sizeOfState[0] - offset)
    blockY = random.randint(1, sizeOfState[1] - offset)
    
    sizeOfBlock = (blockX, blockY)
    
    return generateGrid(sizeOfBlock, 1)               
    
def generateGrid(size, symbol):
    grid = ()
    for _ in range(size[0]):
        temp = ()
        for _ in range(size[1]):
            temp += (symbol, )
        grid += (temp, )
        
    return grid


#______________________________CHECKING OPERATIONS_____________________________________

# Checking always from top leftmost corner of block    
def checkIfInsertionPossible(grid, block):
    (gridX, gridY) = getSize(grid)
    (blockX, blockY) = getSize(block)
    
    if insertNonGoalBlock(block, grid, 15) == (-1, -1):
        return False
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (grid[i][j] == 0):
                tempBool = True
                for k in range(blockX):
                    if i + k > gridX - 1:
                        tempBool = False
                        break
                    if grid[i + k][j] != 0:
                        tempBool = False
                        break
                    
                for l in range(blockY):
                    if j + l > gridY - 1:
                        tempBool = False
                        break
                    if grid[i][j + l] != 0:
                        tempBool = False
                        break
                
                if tempBool:
                    return True
    
    
    
    return False

def getInsertPosition(block, grid):
    (gridX, gridY) = getSize(grid)
    (blockX, blockY) = getSize(block)
    
    validPositions = []
    found = False
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (grid[i][j] == 0):
                tempBool = True
                for k in range(blockX):
                    for l in range(blockY):
                        if i + k > gridX - 1 or j + l > gridY - 1:
                            tempBool = False
                            break
                        if grid[i + k][j + l] != 0:
                            tempBool = False
                            break
                        
                if tempBool:
                    validPositions.append((i, j))
                    found = True
    
                        
    if found:
        return random.choice(validPositions)
    else:
        return (-1 ,-1)
    
    
def getAverageBlockSize(grid):
    totalSizeX = 0
    totalSizeY = 0
    
    totalNo = 0
    for symbol in getBlockSymbolsList(grid):
        totalNo += 1
        (sizeX, sizeY) = (getBlockSize(symbol, grid))  
        totalSizeX += sizeX
        totalSizeY += sizeY
    
    return (totalSizeX/totalNo, totalSizeY/totalNo)
     
#________________________________INSERTION OPERATIONS___________________________

def insertNonGoalBlock(block, grid, symbol):
    (blockX, blockY) = getSize(block)
    # Get the position of the leftmost upper corner
    insertPos = getInsertPosition(block, grid)
   
    i = insertPos[0]
    j = insertPos[1]
    
    grid = convertTupleToList(grid)
    grid[i][j] = symbol
    
    
    # Fill it up
    for k in range(blockX):
        for l in range(blockY):
            if grid[i + k][j + l] == 0:
                grid[i + k][j + l] = symbol

                
    return convertListToTuple(grid)
    

def insertGoalBlockInEmptyGrid(goalBlock, emptyGrid):
    emptyGrid = convertTupleToList(emptyGrid)
    
    for i in range(len(emptyGrid) - getSize(goalBlock)[0], len(emptyGrid)):
        for j in range (0, getSize(goalBlock)[1]):
            emptyGrid[i][j] = 1
            
    return convertListToTuple(emptyGrid)

def insertGoalBlockInStartPosition(goalBlock, emptyGrid):
    emptyGrid = convertTupleToList(emptyGrid)
    
    goalSize = getSize(goalBlock)
    
    for i in range(0, goalSize[0]):
        for j in range (len(emptyGrid[i]) - goalSize[1], len(emptyGrid[i])):
            emptyGrid[i][j] = 1
            
    return convertListToTuple(emptyGrid)

def getSpaceNumber(grid):
    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                total += 1
                
    return total

def checkIfGoalTileIsInUpperLeftHalfgrid(grid):
    for i in range(0, int(floor(len(grid)/2))):
        for j in range(int(floor(len(grid)/2)), len(grid)):
            if grid[i][j] == 1:
                return True
        
    return False

def checkIfAnyTileIsInUpperLeftHalfgrid(grid, symbol):
    for i in range(0, int(floor(len(grid)/2))):
        for j in range(int(floor(len(grid)/2)), len(grid)):
            if grid[i][j] == symbol:
                return True
        
    return False
   
    

#_______________________________EXTEND OPERATIONS (NOT USED GENERALLY)_____________________________________

def extendBottom(grid, (x,y), blockY, symbol):
    grid = convertTupleToList(grid)
    for j in range(y, y + blockY):
        grid[x + 1][j] = symbol
    return convertListToTuple(grid)

def extendLeft(grid, (x,y), blockX, symbol):
    grid = convertTupleToList(grid)
    for i in range(x - blockX + 1, x + 1):
        grid[i][y - 1] = symbol
    return convertListToTuple(grid)

def extendTop(grid, (x,y), blockX, blockY, symbol):
    grid = convertTupleToList(grid)
    for j in range(y, y + blockY):
        grid[x - blockX][j] = symbol
    return convertListToTuple(grid)

def extendRight(grid, (x,y), blockX, blockY, symbol):
    grid = convertTupleToList(grid)
    for i in range(x - blockX + 1, x + 1):
        grid[i][y + blockY] = symbol
    return convertListToTuple(grid)



def extendBlock(grid, symbol):
    (x, y) = getLeftmosDownCornerPositionOfBlock(grid, symbol)
    (blockX, blockY) = getBlockSize(symbol, grid)
    
    # Check bottom side.
    if x + 1 < len(grid):
        tempBool = True
        for j in range(y, y + blockY):
            if grid[x + 1][j] != 0:
                tempBool = False
                break
        
        if tempBool:
            grid = extendBottom(grid, (x, y), blockY, symbol)
            return grid
                  
    # Check left side.
    if y - 1 >= 0:
        tempBool = True
        for i in range(x - blockX + 1, x + 1):
            if grid[i][y - 1] != 0:
                tempBool = False
                break
            
        if tempBool:
            grid = extendLeft(grid, (x, y), blockX, symbol)
            return grid
        
    # Check top side.
    if x - blockX >= 0:
        tempBool = True
        for j in range(y, y + blockY):
            if grid[x - blockX][j] != 0:
                tempBool = False
                break
            
        if tempBool:
            grid = extendTop(grid, (x, y), blockX, blockY, symbol)
            return grid
        
    
    # Check right side.
    if y + blockY < len(grid[0]):
        tempBool = True
        for i in range(x - blockX + 1, x + 1):
            if grid[i][y + blockY] != 0:
                tempBool = False
                break
    
        if tempBool:
            grid = extendRight(grid, (x, y), blockX, blockY, symbol)
            return grid
            
    
    return grid
    
def extendBlocks(grid, extends):
    symbols = getBlockSymbolsList(grid)
    for _ in range(extends):
        if symbols == []:
            break
        symbol = random.choice(symbols)
        grid = extendBlock(grid, symbol)
        symbols.remove(symbol)
        
    return grid
    
def exchangeBlock(grid, symbol1, symbol2):
    visitedPos = set()
    
    grid = convertTupleToList(grid)
    
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == symbol1:
                visitedPos.add((i, j))
                grid[i][j] = symbol2
        
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == symbol2 and (i, j) not in visitedPos:
                grid[i][j] = symbol1

    return convertListToTuple(grid)
    