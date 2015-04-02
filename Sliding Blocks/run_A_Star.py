from slidingBlocks import *
from search import *
from slidingBlocksGenerator import *
import time
import sys


"""
python run_A_Star.py <heuristicNo> <size>
"""
arg = sys.argv

heuristicNo = int(arg[1])
size = (int(arg[2]), int(arg[2]))


randomGrid = generateSlidingBlockGrid(size)
printState(randomGrid)
sb = SlidingBlock(randomGrid)

startTime = time.time()

if heuristicNo == 1:
    search = astar_search(sb, lambda x : h1(x))
if heuristicNo == 2:
    search = astar_search(sb, lambda x : h2(x))
if heuristicNo == 3:
    search = astar_search(sb, lambda x : h3(x))
if heuristicNo == 4:
    search = astar_search(sb, lambda x : h4(x))
    
if search != None:
    print 'Actions to solution: ', len(search.solution())
    print "Time elapsed :  %.3f" % (time.time() - startTime)
else:
    print "No solution found."

