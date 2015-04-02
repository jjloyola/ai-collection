from slidingBlocks import *
from slidingBlocksGenerator import *

for size in range(2, 10):
    sizeOfState = (size, size)
    print 'SIZE: ', sizeOfState
    printState(generateGoalBlock(sizeOfState))

