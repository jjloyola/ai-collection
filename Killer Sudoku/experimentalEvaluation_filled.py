from csp import *
from killerSudokuMain import runCSP
from killerSudoku import *
import sys

translateDict = {'mrv' : mrv,
              'fc' : forward_checking, 
              'mac': mac,
              'bt' : first_unassigned_variable,
              'none' : no_inference}

selectList = []
inferList = []

if len(sys.argv) == 3: # arguments given
    selectList.append(translateDict[sys.argv[1]])
    inferList.append(translateDict[sys.argv[2]])
else: # no arguments given
    selectList.append(first_unassigned_variable, mrv)
    inferList.append(no_inference, forward_checking, mac)
    
for difficulty in ("example","easier","easy","moderate","hard","extreme","outrageous","mind_bending","greater_outrageous","greater_mind_bending"):
    for selection in selectList:
        for infer in inferList:
            fileName = "killer_sudokus/" + difficulty + "_filled.txt"
            (timeElapsed, constraintsChecked, assignNo) = runCSP(fileName, selection, infer)
            
            with open("results/" + difficulty + "_filled.txt", 'a') as f:
                # Write header.
                if infer is no_inference:
                    f.write("------------------ BT")
                elif infer is mac:
                    f.write("------------------ MAC")
                else:
                    f.write("------------------ FC")
                    
                if selection is first_unassigned_variable:
                    f.write(" ------------------ \n")
                else:
                    f.write(" + MRV ---------- \n \n")
                    
                f.write("   Time Elapsed       : %0.5f" % timeElapsed + "\n")
                f.write("   Constrains Checked : " + str(constraintsChecked) + "\n")
                f.write("   Assignments made : " + str(assignNo) + "\n \n")
                
                f.close()
                print "Wrote to results/" + difficulty + "_filled.txt"