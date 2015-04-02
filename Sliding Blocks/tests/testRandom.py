from slidingBlocks import *
from search import *
from slidingBlocksGenerator import *
import time
import sys

 
 
size = (5, 5)
steps = 100
  
randomGrid = generateSlidingBlockGrid(size, steps)
  
printState(randomGrid)

