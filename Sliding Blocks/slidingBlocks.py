'''
Created on Nov 15, 2014

@author: Orestis Melkonian
'''
from lib2to3.pygram import Symbols

"""N-Puzzle problem"""

from search import Problem, astar_search
from slidingBlocksUtilities import *
import random


class SlidingBlock(Problem) :
    """Subclass of search.Problem"""
    
    def __init__(self, initialState) :
        """
        Sets initial state.
        - States are representated as a 2D matrix filled with discrete numbers.
        Where there are multiple same numbers a block of more than one position is defined.
        0: space
        1: block we need to get to the leftmost-bottom corner
        2...X: other blocks insisde the grid
        
        In fact, any discrete symbols can be used to represent the blocks, but 0 is necessary for space.
        
        - Actions are represented as a tuple (Number, 'Direction'), 
        where {Number} is the number identifier of a block
        and {'Direction'} is one of ['up', 'down', 'left', 'right']
        
        """

        self.initialState = initialState
                
        super(SlidingBlock, self).__init__(self.initialState)


# _______________________________________________________________
 
    def actions(self, state) :
        """Returns the actions that can be executed in the state"""
        return getValidActions(state)


# _______________________________________________________________
 
    def result(self, state, action) :
        """ The state as a result of given action on given state"""
                 
        blockNumber = action[0]
        direction = action[1]
        
        sizeX = getSize(state)[0]
        sizeY = getSize(state)[1]
        
        # Start from upper rows and move elements of the requested block upwards.
        if direction== "up" :
            for i in range(len(state)):
                for j in range(len(state[i])):
                    if state[i][j] == blockNumber:
                        state = swawValuesInGrid(state, (i, j), (i - 1, j))
        
        # Start from lower rows and move elements of the requested block downwards.
        elif direction== "down" :
            for i in reversed(range(len(state))):
                for j in range(len(state[i])):
                    if state[i][j] == blockNumber:
                        state = swawValuesInGrid(state, (i, j), (i + 1, j))
        
        # Start from lefmost columns and move elements of the requested block leftwards.    
        elif direction== "left" :
            for j in range(sizeY):
                for i in range(sizeX):
                    if state[i][j] == blockNumber:
                        state = swawValuesInGrid(state, (i, j), (i, j - 1))            
        
        # Start from rightmost columns and move elements of the requested block rightwards.
        elif direction== "right" :
            for j in reversed(range(sizeY)):
                for i in range(sizeX):
                    if state[i][j] == blockNumber:
                        state = swawValuesInGrid(state, (i, j), (i, j + 1))
        
        else :
                print "ERROR: invalid direction"
        
        return state;

    
# _______________________________________________________________

    def goal_test(self, state):
        """ Returns true if the state given is a goal state. """
        
        blockSize = getBlockSize(1, state)
#         print 'Block size of 1: ', blockSize
        
        for row in range(len(state) - blockSize[0], len(state)):
            for column in range(0, blockSize[1]):
                if (state[row][column] != 1):
                    return False
        
        return True
        
    
    
# _________________HEURISTICS_________________________________


""" MANHATTAN DISTANCE
        Manhattan Distance of the leftmost-down tile of the goalBlock to the leftmost-down corner of the whole grid. """
def h1(node):
    state = node.state
    
    ret = calculateManhattanDistance(state, getLeftmosDownCornerPositionOfBlock(state, 1))
    return ret 
        
    
""" MD + PATHCHECK 
        Manhattan Distance
                +
        Number of non-space(!=0) and non-goal(!=1) on the manhattan path from leftmost-down tile of the goalBlock to the leftmost-down corner of the grid. """
def h2(node):
    state = node.state
    
    total = 0
    
    symbols = Set()
    symbols.add(0)
    symbols.add(1)
    
    (x, y) = getLeftmosDownCornerPositionOfBlock(state, 1)
    
    for i in range(x, len(state)):
        if state[i][y] not in symbols:
            symbols.add(state[i][y])
            total += 1
    
    for j in reversed(range(y, 0)):
        if state[len(state)][j] not in symbols:
            symbols.add(state[len(state)][j])
            total += 1
        
    return total + h1(node)

""" MD + ADVANCED_GOALCHECK
        ManhattanDistance 
            +
        Distance of non-space(!=0) and non-goal(!=1) different symbols to move out of the goal block. """
def h3(node):
    state = node.state
 
     
    total = 0
    symbols = Set()
    symbols.add(0)
    symbols.add(1)
     
    (blockX, blockY) = getBlockSize(1, state)
     
    for i in range(len(state) - blockX, len(state)):
        for j in range(0, blockY):
            if state[i][j] not in symbols:
                total += getDistanceOutOfGoalBlock(state, (i, j))
                symbols.add(state[i][j])
                
    return total + h1(node)


""" MD + ADVANCED_GOALCHECK + PATHCHECK
        ManhattanDistance 
            +
        Distance of non-space(!=0) and non-goal(!=1) different symbols to move out of the goal block. """
def h4(node):
    state = node.state
    
    total = 0
    symbols = Set()
    symbols.add(0)
    symbols.add(1)
    
    
    (blockX, blockY) = getBlockSize(1, state)
    
    for i in range(len(state) - blockX, len(state)):
        for j in range(0, blockY):
            if state[i][j] not in symbols:
                total += getDistanceOutOfGoalBlock(state, (i, j))
                symbols.add(state[i][j])

            
    (x, y) = getLeftmosDownCornerPositionOfBlock(state, 1)
    
    for i in range(x, len(state)):
        if state[i][y] not in symbols:
            symbols.add(state[i][y])
            total += 1
    
    for j in reversed(range(y, 0)):
        if state[len(state)][j] not in symbols:
            symbols.add(state[len(state)][j])
            total += 1
            
        
    return total + h1(node)




    
    
    
        