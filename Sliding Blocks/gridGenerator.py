from slidingBlocks import *
from search import *
from slidingBlocksGenerator import *
import time
import re # using Regex for extracting numbers out of printss
import subprocess as sub # For calling run_A_Star and keeping prints in file for statistic evaluation
import threading
import os

global result
result = '--'

def getExploredNodes(output):
    if len(re.split('\n', output)) > 0:
        output = re.split('\n', output)[0]
    else:
        return 0
    if len(re.findall("(\d+)", output)) > 0:
        return re.findall("(\d+)", output)[0]
    else:
        return 0
def getActionNo(output):
    if len(re.split('\n', output)) > 1:
        output = re.split('\n', output)[1]
    else:
        return 0  
    if len(re.findall("(\d+)", output)) > 0:
        return re.findall("(\d+)", output)[0]
    else:
        return 0
def getTime(output):
    if len(re.split('\n', output)) > 2:
        output = re.split('\n', output)[2]
    else:
        return 0
    if len(re.findall("(\d+.\d+)", output)) > 0:
        return re.findall("(\d+.\d+)", output)[0]
    else:
        return 0.0






class RunCmd(threading.Thread):
    def __init__(self, cmd, timeout):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.timeout = timeout

    def run(self):
        global result
        self.p = sub.Popen(self.cmd, stdout=sub.PIPE)
        result = self.p.communicate()[0]
        self.p.wait()

    def Run(self):
        self.start()
        self.join(self.timeout)

        if self.is_alive():
            print 'too long'
            self.p.terminate()      #use self.p.kill() if process needs a kill -9
            self.join()



print "Generating various sizes grids..."
for size in range(7, 10):
    for size2 in range(size -1, size + 2):
        
        totalSize = (size, size2)
        sizeName = str(totalSize[0]) + 'x' + str(totalSize[1])
        
        for _ in range(50):   
            print "   Generating..."
            # Write generated state to input text file.
            state = generateSlidingBlockGrid(totalSize)
            inputText = open("inputState.txt", "w")
            for row in state:
                for j in row:
                    inputText.write(str(j) + ' ')
                inputText.write('\n')
                
            inputText.close()
            print "   Solving..." 
            RunCmd(['python', 'run_No_Gen.py', str(4)], 600).Run()
            
            
            
            output = result   
            
            result = '--'
            
            explored = int(getExploredNodes(output))
            actions = int(getActionNo(output))
            time = float(getTime(output))
             
            if actions == 0 and explored == 0:
                print "       Retrying"
                continue
            
            # Files in format size_{size}-actions_{actions}.txt
            fileName = 'states/size_' + sizeName + '/actions_' + str(actions) + '.txt'
        
            # Copy generated state into new generated file.
            print "    saving state in file with name: " + fileName 
            with open("inputState.txt") as f:
                with open(fileName, "a") as f1:    
                    for line in f:
                        f1.write(line)
                    f1.write('\n --------------------------- \n')
                    f.close() 
                
            inputText.close()

exit()
