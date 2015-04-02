from puzzle import *
from search import *
from puzzleGenerator import *
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



print "Generating various sizes puzzles..."
for base in range(3, 9):
    size = base*base - 1
    
    for _ in range(50):   
        # Write generated state to input text file.
        gen = puzzleGenerator(size)
        steps = random.randint(1, 50)
        state = gen.generateNStepsState(steps)

        inputText = open("inputState.txt", "w")
        for row in state:
            for j in row:
                inputText.write(str(j) + ' ')
            inputText.write('\n')
            
        inputText.close()
         
        RunCmd(['python', 'run_No_Gen.py', str(1)], 300).Run()
        
        
        output = result   
        
        result = '--'
        
        explored = int(getExploredNodes(output))
        actions = int(getActionNo(output))
        time = float(getTime(output))
         
        if actions == 0 or explored == 0:
            continue
        
        # Files in format size_{size}-actions_{actions}.txt
        fileName = 'states/' + str(size) + '_puzzle' + '/actions_' + str(actions) + '.txt'
    
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
