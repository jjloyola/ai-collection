from puzzle import *
from puzzleGenerator import *
from search import *

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


for totalSize in range(3, 11):
    size = totalSize*totalSize - 1
    for steps in range(100, 1100, 100):
        
        # Write generated state to input text file.
        gen = puzzleGenerator(size)
        state = gen.generateNStepsState(size)
        inputText = open("inputState.txt", "w")
        for row in state:
            for j in row:
                inputText.write(str(j) + ' ')
            inputText.write('\n')
            
        inputText.close()
        
        for heuristic in range(1,5):
            
            # Files in format h{heuristic}-{steps}-{size}.txt
            fileName = 'generated_statistics/h'
            fileName += str(heuristic)
            fileName += '-'
            fileName += 'r'
            fileName += str(steps)
            fileName += '-'
            fileName += 's'
            fileName += str(size)
            fileName += '.txt'
            file = open(fileName, "a")
            
            """puzzleMain.py -s <size> -r <steps> -h <heuristic>"""
            RunCmd(['python', 'run_No_Gen.py', str(heuristic), str(size), str(steps)], 60).Run()

            output = result   

            result = '--'
            
            explored = int(getExploredNodes(output))
            actions = int(getActionNo(output))
            time = float(getTime(output))
                
                
            
            
            print 'Writing to file.'
            print '- Size: ', size
            print '- Steps: ', steps
            print '- Heuristic: ', heuristic
            
            
            file.write("\n----RUN 1-----\n")    
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


#________________________________________________________________________________________