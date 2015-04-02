from slidingBlocks import *
from slidingBlocksUtilities import *
from search import *
from slidingBlocksGenerator import *
import time
import sys


arg = sys.argv

heuristicNo = int(arg[1])

# Get state from input file
inputFile = open("inputState.txt", "r")
state = getInitialStateFromText(inputFile)
inputFile.close()

sb = SlidingBlock(state)

startTime = time.time()

if heuristicNo == 0:
    search = breadth_first_search(sb)
if heuristicNo == 1:
    search = astar_search(sb, lambda x : h1(x))
if heuristicNo == 2:
    search = astar_search(sb, lambda x : h2(x))
if heuristicNo == 3:
    search = astar_search(sb, lambda x : h3(x))
if heuristicNo == 4:
    search = astar_search(sb, lambda x : h4(x))
    
if search != None and search.solution():
    print 'Actions to solution: ', len(search.solution())
    print "Time elapsed :  %.3f" % (time.time() - startTime)