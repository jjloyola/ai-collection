from killerSudoku import KillerSudoku
from csp import *
import sys
import time
import globals

def runCSP(fileName, selection, infer):
    print
    print 'Running CSP'
    print ' - filename: ', fileName
    print ' - selection: ', selection.__name__
    print ' - infer: ', infer.__name__
    print
    
    startTime = time.time()
    
    ks = KillerSudoku(fileName)
     
    backtracking_search(ks, 
                        select_unassigned_variable=selection,  
                        inference=infer)
    
    timeElapsed = time.time() - startTime
    
    return (timeElapsed, globals.constraintChecks, ks.nassigns)