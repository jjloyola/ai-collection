""" Provides a graphical user interface for solving the N-puzzle. """

from Tkinter import  *
import ttk
import time

from puzzleUtilities import *
from puzzle import *
from search import *

         
        
    
p = puzzle(8, False, None, True, 10)
solution = astar_search(p, lambda x : h1(x, p.goal))

state = p.initial
states = []
states.append(state)

for i in solution.solution():
    state = p.result(state, i)
    states.append(state)

size = getSizeFromState(states[0])

style = ttk.Style()
style.configure("BW.TLabel", padding=(size/4), width=1, font='serif 10', relief="groove",
background="#000", foreground="#fff")


root = Tk()
frame = Frame(root)
frame.pack()

bottomframe = Frame(root)
bottomframe.pack( side = BOTTOM )

redbutton = Button(frame, text="Red", fg="red")
redbutton.pack( side = LEFT)

greenbutton = Button(frame, text="Brown", fg="brown")
greenbutton.pack( side = LEFT )

bluebutton = Button(frame, text="Blue", fg="blue")
bluebutton.pack( side = LEFT )

blackbutton = Button(bottomframe, text="Black", fg="black")
blackbutton.pack( side = BOTTOM)

root.mainloop()

# ttk.Label(frame, text=' ORESTIS ', style="BW.TLabel").grid(row=0,column=0,padx=10,pady=10,ipadx=10,ipady=10)   


# for state in states:
#     time.sleep(1)
#     for i in range(len(state)):
#         for j in range(len(state[i])):
#             ttk.Label(frame, text='  ' + str(state[i][j]), style="BW.TLabel").grid(row=i,column=j,padx=10,pady=10,ipadx=10,ipady=10)
#     
#     for w in frame.children.values():
#         w.destroy()
    
