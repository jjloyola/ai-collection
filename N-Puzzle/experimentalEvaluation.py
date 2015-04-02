from puzzle import *
from search import *
from puzzleGenerator import *
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
puzzle_map = dict([(8,  (5,7,9,11,13,15,17,19,21,23)),
                   (15, (10,12,14,16,18,20,22,24,26,28,30)),
                   (24, (19,21,23,25,27,29,31,33,35,40)),
                   (35, (19,21,23,25,27,30,33,36,41,45)),
                   (48, (20,25,30,34,36,38,40,42,45,47)),
                   (63, (20,25,31,33,35,37,39,41,44,46))])


for size in (15,24,35,48,63):
    for actions in puzzle_map[size]:
    
        fileName = "states/" + str(size) + "_puzzle/actions_" + str(actions) + ".txt"
        
        linesToRead = int(sqrt(size + 1))
        # Get previously generated state and copy it to "inputState.txt" for run_No_Gen.py to use.
        with open(fileName) as f:
            lines = f.readlines()
            with open("inputState.txt", "w") as f1:  
                for i in range(0, linesToRead):
                    f1.write(lines[i])
        f.close() 
        f1.close()
        
        for heuristic in range(1,5):        
             
            RunCmd(['python', 'run_No_Gen.py', str(heuristic)], 600).Run()
            
            
            output = result   
            result = '--'
            
            explored = int(getExploredNodes(output))
            actionsToSolution = int(getActionNo(output))
            time = float(getTime(output))
            
            if actionsToSolution != actions:
                print "DIFFERENT ACTIONS!!!"
                
            fileName = "heuristic_evaluation/" + str(size) + "_puzzle/actions_" + str(actions) + ".txt"    
            
            file = open(fileName, "a")
            
            file.write("\n----Heuristic: " + str(heuristic) + "-----\n")    
            file.write("Explored nodes: ")
            file.write(str(explored))
            file.write('\n')
            file.write("Actions to solution: ")
            file.write(str(actions))
            file.write('\n')
            file.write("Time elapsed: ")
            file.write(str(time))
            file.write('\n')
            
            file.close()

exit()

    