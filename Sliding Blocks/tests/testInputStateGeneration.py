from slidingBlocks import *
from search import *
from slidingBlocksGenerator import *
import time
import sys

for size in range(2, 10):
    print "size: ", size
    # Write generated state to input text file.
    state = generateSlidingBlockGrid((size, size), 1000)
    printState(state)
    
    inputText = open("../input_states/inputState" + str(size) + ".txt", "w")
    for row in state:
        for j in row:
            inputText.write(str(j) + ' ')
        inputText.write('\n')

    inputText.close()
    print "wrote to input_states/inputState" + str(size) + ".txt"
