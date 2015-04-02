""" Utility functions used from the other scripts. """


import math # For using sqrt()


def getValidActions(spacePosition, n) :
    """ Returns the valid actions of the given space
    position and a N-puzzle"""
            
    validActions = []

    limit = math.sqrt(n+1)
                    
    # Up is valid
    if spacePosition[0] != 0 :
        validActions.append("up")
    # Down is valid
    if spacePosition[0] != limit - 1 :             
        validActions.append("down")
    # Left is valid
    if spacePosition[1] != 0 :
        validActions.append("left")
    # Right is valid
    if spacePosition[1] != limit - 1 :           
        validActions.append("right")

    return validActions


def getSpacePosition(state) :
    """ Returns the position of the space on the puzzle"""

    for i in range(len(state)) :
        for j in range(len(state[i])) :
            if state[i][j] == 0 :
                return [i, j]

    print "ERROR: didn't find space in getSpacePosition"
    exit

def getValuePosition(state, value) :
    """ Returns the position of the value given on the puzzle"""

    for i in range(len(state)) :
        for j in range(len(state[i])) :
            if state[i][j] == value :
                return [i, j]

    print "ERROR: didn't find value in getValuePosition"
    exit
        
def findEmptyPosition(array) :
    for i in range(len(array)) :
        if array[i] == 0 :
            return i;
    return None

def swapValuesInPuzzle(pos1, pos2, state) :
    """ Swaps the positions of two elements in the puzzle
    pos1,2 are in the form of [i, j]"""

    state = convertTupleToList(state)
    retState = state

    temp = retState[pos1[0]][pos1[1]]
    retState[pos1[0]][pos1[1]] = retState[pos2[0]][pos2[1]]
    retState[pos2[0]][pos2[1]] = temp
    
    return convertListToTuple(retState)

def calculateInversions(array) :
    inversions = 0
    for i in range(len(array)) :
        value = array[i]
        for j in range(i + 1, len(array)) :
            if array[j] < value and array[j] != 0:
                    inversions += 1
    return inversions

def checkIfSolvable(state, puzzleSize) :
    array = convertStateToArray(state)
    inversions = calculateInversions(array)
    gridWidth = int(math.sqrt(puzzleSize + 1))

    if gridWidth % 2 :
        return not (inversions % 2)
    else :
        emptyPos = getSpacePosition(state)
        if emptyPos[0] % 2 :
            return not (inversions % 2)
        else :
            return inversions % 2
                        
def convertStateToArray(state) :
    array = []
    for i in state :
        for j in i :
            array.append(j)
    return array

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
        
def printState(state) :
    for i in state :
        print i
               

def getSizeFromState(state) :
    count = 0
    for _ in state :
        count += 1
    return count*count - 1
                
def getInitialStateFromText(inputText) :
    initialState = ()
    
    for line in inputText :
        initialState += (tuple([int(s) for s in line.split() if s.isdigit()]), )
    
    return initialState     
    