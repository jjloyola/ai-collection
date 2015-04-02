""" Main to test functionality, gather statistics """

from puzzle import puzzle, h1, h2, h3, h4
from puzzleUtilities import printState, checkIfSolvable
from search import astar_search, breadth_first_search

import sys # to get command-line arguments
import time # to count time of execution
import getopt # to parse command-line arguments
from __builtin__ import exit

startTime = time.time()


try:
    opts, args = getopt.getopt(sys.argv[1:],"s:i:r:h:")
except getopt.GetoptError:
    print 'puzzleMain.py -i <inputFile> -h <heuristic> OR puzzleMain.py -s <size> -r <steps> -h <heuristic>' 
    #<size> := NxN - 1, <inputFile> := inputState.txt, <heuristic> := {0,...,5}, steps := {0,...99999999}
    sys.exit(2)

steps = -1    
for opt, arg in opts:
    if opt == '-i':
        inputFile = arg
        """ (size := NxN - 1, wantTextInput, wantDifficulty, steps)"""
        p = puzzle(None, True, inputFile, False, None)
    elif opt == '-s':
        size = int(arg)
    elif opt == '-r':
        steps = int(arg)
        """ (size := NxN - 1, wantTextInput, wantDifficulty, steps)"""
        p = puzzle(size, False, None, True, steps)
    elif opt == '-h':
        heuristic = int(arg)



print "\n___Initial State___"
printState(p.initial)
print
print "\n___Goal State___"
printState(p.goal)
print

   

if steps == -1 : #only check if the initial state is solvable when input from text file is considered
    if not checkIfSolvable(p.initial, p.n) :
        print "GIVEN PUZZLE IS NOT SOLVABLE"
        exit()
    
if heuristic == 0 :
    solution = breadth_first_search(p)
elif heuristic == 1 :
    solution = astar_search(p, lambda x : h1(x, p.goal))
elif heuristic == 2 :
    solution = astar_search(p, lambda x : h2(x, p.goal))
elif heuristic == 3 :
    solution = astar_search(p, lambda x : h3(x, p.goal))
elif heuristic == 4 :
    solution = astar_search(p, lambda x : h4(x, p.goal))


solution = solution.solution()
# print solution



print "Actions made : ", len(solution)
print "Time elapsed :  %.5f" % (time.time() - startTime)

















