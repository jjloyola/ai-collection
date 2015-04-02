from slidingBlocks import *
from search import *
from slidingBlocksGenerator import *
import time
import re # using Regex for extracting numbers out of printss
import subprocess as sub # For calling run_A_Star and keeping prints in file for statistic evaluation
import threading

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

# Create dictionary for getting valid actions.
grid_map = dict([((3,3),  (6,8,9,10,11)),
                 ((3,4),  (5,6,8,12)),
                 ((4,3),  (10,12,16,20,23)),
                 ((4,4),  (15,20,22,25,38)),
                 ((4,5),  (22,29,33,37,42)),
                 ((5,4), (19,37,38,43,48)),
                 ((5,5), (12,18,30,35,51)),
                 ((5,6), (15,19,20,21,22)),
                 ((6,5), (10,12,15,24,31)),
                 ((6,6), (11,13,14,16,17)),
                 ((6,7),  (15,18,27)),
                 ((7,6),  (14,17,20,22)),
                 ((7,7),  (12,18,29)),
                 ((7,8),  (13,14)),
                 ((8,7),  (20,25,29)),
                 ((8,8),  (22,29))])


for size1 in (7,8,9):
    for size2offset in (-1, 0, 1):
        
        size = (size1, size1 + size2offset)
        
        
        for actions in grid_map[size]:
    
            fileName = "states/size_" + str(size[0]) + "x" + str(size[1]) + "/actions_" + str(actions) + ".txt"
            
            # Get previously generated state and copy it to "inputState.txt" for run_No_Gen.py to use.
            with open(fileName) as f:
                lines = f.readlines()
                with open("inputState.txt", "w") as f1:  
                    for i in range(0, size[0]):
                        f1.write(lines[i])
            f.close() 
            f1.close()
            
            for heuristic in reversed(range(1,5)):        
                 
                RunCmd(['python', 'run_No_Gen.py', str(heuristic)], 300).Run()
                
                
                output = result   
                print output
                result = '--'
                
                explored = int(getExploredNodes(output))
                actionsToSolution = int(getActionNo(output))
                time = float(getTime(output))
                
                    
                 
                print 'Writing to file.'
                print '- Heuristic: ', heuristic
                
                # Files in format h{heuristic}-{difficulty}-{size}.txt
                fileName = "heuristic_evaluation/size_" + str(size[0]) + "x" + str(size[1]) + "/actions_" + str(actions) + ".txt"    
                
                file = open(fileName, "a")
                
                file.write("\n----Heuristic: " + str(heuristic) + "-----\n")    
                file.write("Explored nodes: ")
                file.write(str(explored))
                file.write('\n')
                file.write("Actions to solution: ")
                file.write(str(actionsToSolution))
                file.write('\n')
                file.write("Time elapsed: ")
                file.write(str(time))
                file.write('\n')
                
                file.close()

exit()

    