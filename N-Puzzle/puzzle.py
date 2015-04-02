"""N-Puzzle problem"""

from search import Problem
from puzzleGenerator import puzzleGenerator  # Needed to generate random initial and goal state
from puzzleUtilities import getSpacePosition, getValuePosition, getValidActions, swapValuesInPuzzle, getInitialStateFromText, getSizeFromState

class puzzle(Problem) :
    """Subclass of search.Problem"""
    
    def __init__(self, size, wantTextInput, inputFile, wantDifficulty, steps) :
        """Sets initial state and goal.
        States are representated as a 2D matrix
        filled with N-1 numbers and 1"""

                        
        if wantTextInput :
            self.startState = getInitialStateFromText(open(inputFile, 'r'))
            self.n = getSizeFromState(self.startState)
            gen = puzzleGenerator(self.n)
        elif wantDifficulty :
            gen = puzzleGenerator(size)
            self.n = size
            self.startState = gen.generateNStepsState(steps)
        else :
            gen = puzzleGenerator(size)
            self.n = size
            self.startState = gen.initial
        

        self.goalState = gen.goal  
                
        super(puzzle, self).__init__(self.startState, self.goalState)



# _______________________________________________________________

    def actions(self, state) :
        """Returns the actions that can be executed in the state"""
                
        return getValidActions(getSpacePosition(state), self.n)
# _______________________________________________________________

    def result(self, state, action) :
        """ The state as a result of given action on given state"""
                
        spacePosition = getSpacePosition(state)
        
        if action == "up" :
                targetPosition = [spacePosition[0] - 1, spacePosition[1]]
        elif action == "down" :
                targetPosition = [spacePosition[0] + 1, spacePosition[1]]
        elif action == "left" :
                targetPosition = [spacePosition[0], spacePosition[1] - 1]
        elif action == "right" :
                targetPosition = [spacePosition[0], spacePosition[1] + 1]
        else :
                print "ERROR: invalid action"


        retState = swapValuesInPuzzle(spacePosition, targetPosition, state)

        # printState(retState)
        # print

        return retState
    
    
# _________________HEURISTICS_________________________________


""" Manhattan Distance """
def h1(n, goalState) :
        state = n.state

        currentPosition = {}
        goalPosition = {}

        # Get current position of all elements on puzzle.
        for i in range(len(state)) :
                for j in range(len(state[i])) :
                        if state[i][j] != 0 :
                                currentPosition[state[i][j]] = [i, j] 
                                

        # Get goal position of all elements on puzzle.
        for i in range(len(goalState)) :
                for j in range(len(goalState[i])) :
                        if goalState[i][j] != 0 :
                                goalPosition[goalState[i][j]] = [i, j]
                                

        # Calculate manhattan distances.
        manhattanDistanceSum = 0;
        for i in range(1, getSizeFromState(state)+ 1) :  # will put N instead of 8
                x = currentPosition[i]
                y = goalPosition[i]
        
                manhattanDistanceSum += abs(x[0] - y[0]) + abs(x[1] - y[1]) 

        # Return heuristic estimation value.
        return manhattanDistanceSum;
        
""" Gashing mechanism """
def h2(n, goalState) :
        state = n.state

        count = 0
        
        while state != goalState :
                emptyPos = getSpacePosition(state)
                emptyGoalPos = getSpacePosition(goalState)
                if emptyPos != emptyGoalPos :
                    # Move right value in the position of the space
                    value = goalState[emptyPos[0]][emptyPos[1]]
                    rightValuePos = getValuePosition(state, value)
                    state = swapValuesInPuzzle(emptyPos, rightValuePos, state)
                else :
                    # Get wrong value position
                    wrongValuePos = []
                    for i in range(len(state)) :
                        for j in range(len(state[i])) :
                            if state[i][j] != 0 and state[i][j] != goalState[i][j] :
                                wrongValuePos = [i, j]
                                break
                    # Swap with empty position
                    state = swapValuesInPuzzle(emptyPos, wrongValuePos, state)

                count += 1

        return count

""" Misplaced Tiles """
def h3(n, goalState) :
    state = n.state
    
    count = 0
    
    for i in range(len(state)) :
        for j in range(len(state[i])) :
            if state[i][j] != 0 and state[i][j] != goalState[i][j] :
                count += 1
    
    return count

""" Out-of-row/column """
def h4(n, goalState) :
    state = n.state
    
    count = 0
    
    for i in range(len(state)) :
        for j in range(len(state[i])) :
            if state[i][j] != goalState[i][j] :
                rightValuePos = getValuePosition(goalState, state[i][j])
                if rightValuePos[0] != i :
                    count += 1
                if rightValuePos[1] != j :
                    count += 1

    return count;





