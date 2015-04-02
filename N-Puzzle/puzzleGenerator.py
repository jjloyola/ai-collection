""" Used to generate random initial and goal states. """

import random # For using randrange()
from math import sqrt
from puzzleUtilities import getSpacePosition, getValidActions, swapValuesInPuzzle


class puzzleGenerator() :
    def __init__(self, n) :
        """ Sets the size of the puzzle, which is the number of different digits not counting the space"""       
                                         
        self.n = n
        self.initial = self.generateInitialState()
        self.goal = self.generateStandardGoalState()


    def generateInitialState(self) :
        n = self.n
        tupleSize = int(sqrt(n + 1))
        
        initialState = ()
        randomSet = [0]
                
        for i in range(1, n + 1) :
            randomSet.append(i) # Here randomSet = [1, 2, ... , n]


        while randomSet : # while it is not empty
            random_elements = []
            for i in range(1, tupleSize + 1) :
                random_elem = random.choice(randomSet)
                randomSet.remove(random_elem)
                random_elements.append(random_elem)
                

            initialState += (tuple(random_elements), )
            random_elements = []

        return initialState

    def generateGoalState(self) :
        n = self.n
        tupleSize = int(sqrt(n + 1))
        
        goalState = ()
        randomSet = [0]
                
        for i in range(1, n + 1) :
            randomSet.append(i) # Here randomSet = [1, 2, ... , n]


        while randomSet : # while it is not empty
            random_elements = []
            for i in range(1, tupleSize + 1) :
                random_elem = random.choice(randomSet)
                randomSet.remove(random_elem)
                random_elements.append(random_elem)
                

            goalState += (tuple(random_elements), )
            random_elements = []

        return goalState        


    def generateStandardGoalState(self) :
        n = self.n
        tupleSize = int(sqrt(n + 1))
        
        goalState = ()

        count = 0

        for count in range(1, n + 1, tupleSize) :
            tempCount = count
            temp = ()
            
            for _ in range(0, tupleSize - 1) :
                temp += (tempCount, )
                tempCount += 1

            if tempCount != n + 1 :
                temp += (tempCount, )
            else :
                temp += (0, )

            goalState += (temp, )

        return goalState



    def generateNStepsState(self, n) :
        state = self.goal
        lastAction = ""
        for _ in range(0, n) :
            (state, lastAction) = makeRandomMove(state, self.n, lastAction)
            

        return state 


def makeRandomMove(state, n, lastAction) : 
    spacePos = getSpacePosition(state)
    validActions = getValidActions(spacePos, n)
    action = random.choice(validActions)
    
    # Do not go to previous position just yet.
    while True:
        if lastAction == "up":
            if action == "down":
                validActions.remove(action)
                action = random.choice(validActions)
            else:
                break
        elif lastAction == "down":
            if action == "up":
                validActions.remove(action)
                action = random.choice(validActions)
            else:
                break
        elif lastAction == "left":
            if action == "right":
                validActions.remove(action)
                action = random.choice(validActions)
            else:
                break
        elif lastAction == "right":
            if action == "left":
                validActions.remove(action)
                action = random.choice(validActions)
            else:
                break
        else:
            break

    lastAction = action
    
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
    return (retState, lastAction)







