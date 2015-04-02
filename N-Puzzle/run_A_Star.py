""" Main to test functionality, gather statistics """

from puzzle import puzzle, h1, h2, h3, h4
from search import astar_search, breadth_first_search

import sys # to get command-line arguments
import time # to count time of execution


startTime = time.time()

"""
python run_A_Star.py heuristicNo size steps
"""
arg = sys.argv

heuristic = int(arg[1])
size = int(arg[2])
steps = int(arg[3])
        

p = puzzle(size, False, None, True, steps)

    
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



print "Actions made : ", len(solution)
print "Time elapsed :  %.5f" % (time.time() - startTime)