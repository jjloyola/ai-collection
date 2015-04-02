from slidingBlocks import *
from time import *
from Tkinter import *
from ttk import Entry
from slidingBlocksGenerator import *
from re import search
import threading




""" Displays information about the current puzzle, e.g. size, number of blocks, number of random steps from goal state, etc... """
class StatusBar(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent, relief=RAISED, height=100)   
         
        self.parent = parent
        self.initUI()
        
    def initUI(self):
        global size, steps, heuristicNo
        
        sizeLabel = Label(self, text="Size:   " + str(size) + '       ', height=5)
        
        if heuristicNo == 1:
            heuristic = "Manhattan Distance"
        elif heuristicNo == 2:
            heuristic = "Manhattan Distance + Path Check"
        elif heuristicNo == 3:
            heuristic = "Manhattan Distance + Advanced Goal"
        elif heuristicNo == 4:
            heuristic = "Manhattan Distance + Advanced Goal + PathCheck"
        
        heuristicLabel = Label(self, text="Heuristic:   " + heuristic + '   ', height=5)
                 
        sizeLabel.pack(side=LEFT, fill=X)
        heuristicLabel.pack(side=RIGHT, fill=X)
        
        self.pack(side=BOTTOM, fill=X)
        
    
    
    
""" Accomodates all the buttons interfaced to the user, enabling him to control the run of the solution. """
class ControlPanel(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)   
         
        self.parent = parent
        
        self.initUI()
        
    def initUI(self):
        
        generate = Button(self, text="Generate", command=self.generate,height=5, width=45, relief=RAISED, overrelief=FLAT)
        generate.pack(side = LEFT)

        step = Button(self, text="Step", command=self.step, height=5, width=45, relief=RAISED, overrelief=FLAT)
        step.pack(side = LEFT)

        solve = Button(self, text="Solve", command=self.solve, height=5, width=45, relief=RAISED, overrelief=FLAT)
        solve.pack(side = RIGHT)

        self.pack(side=TOP, fill=X)
        
    def generate(self):
        print 'Generating...'
        global size, heuristicNo
        state = generateSlidingBlockGrid(size)
        print 'Solving...'

        global sb
        sb = SlidingBlock(state)
        
        
        global search
        
        global lastAction
        
        lastAction = None
        if heuristicNo == 1:
            search = astar_search(sb, lambda x : h1(x))
        elif heuristicNo == 2:
            search = astar_search(sb, lambda x : h2(x))
        elif heuristicNo == 3:
            search = astar_search(sb, lambda x : h3(x))
        elif heuristicNo == 4:
            search = astar_search(sb, lambda x : h4(x))
        
        if search == None:
            self.generate()
            return
        print "Actions to solution:", len(search.solution())
        
        if (len(search.solution())):
            lastAction = 0
        else:
            lastAction = None

        
        grid.reset(state)
        return
    
    def step(self):
        global lastAction, search, sb
        if lastAction != None:
            state = sb.result(grid.state, search.solution()[lastAction])
            lastAction += 1
            if (not lastAction < len(search.solution())):
                lastAction = None
                
            grid.reset(state)
            return True
        return False

    def solve(self):
        for i in range(len(search.solution())):
            self.after(i*500, self.step)
        return 
    
    
""" The grid of the puzzle. Essentially, the representation of the puzzle. """
class Grid(Frame):
    
 
 
    def __init__(self, parent, state):
        Frame.__init__(self, parent, relief=RAISED, background="black")   
        self.parent = parent
        
        self.state = state

        self.initUI()
        
    def initUI(self):
        self.COLORS  =['snow',  'red', 'orchid1', 'DarkOrange4', 'yellow2', 'SystemButtonText', 'purple4',
                       'SystemHighlight', 'honeydew2', 'SkyBlue4', 'turquoise3', 'SeaGreen3', 'DarkOliveGreen2','khaki4',
                       'DarkGoldenrod1', 'IndianRed4', 'DarkOrange1', 'LightPink2', 'MediumPurple2','magenta']
        
        for i in range(len(self.state)):
            self.rowconfigure(i, pad=3, weight=1)
            for j in range(len(self.state[i])):
                self.columnconfigure(j, pad=3, weight=1)                
                if (self.state[i][j] == 0):
                    temp = Label(self, background=self.COLORS[self.state[i][j]], foreground="black", width=5, height=5)
                else:
                    temp = Label(self, background=self.COLORS[self.state[i][j]], foreground="black", borderwidth=5, width=5, height=5)
                temp.grid(row=i, column=j, sticky=W+N+E+S, padx=0, pady=0)
        
        
        self.pack(fill=BOTH, expand=1)
        
    def reset(self, newState):
        self.state = newState
        
        for child in reversed(grid.grid_slaves()):
            child.destroy()
        
        for i in range(len(self.state)):
            self.rowconfigure(i, pad=3, weight=1)
            for j in range(len(self.state[i])):
                self.columnconfigure(j, pad=3, weight=1)                
                if (self.state[i][j] == 0):
                    temp = Label(self, background=self.COLORS[self.state[i][j]], border=1, foreground="black", borderwidth=2, width=5, height=5)
                else:
                    temp = Label(self, background=self.COLORS[self.state[i][j]], border=1, foreground="black", borderwidth=5, width=5, height=5)
                temp.grid(row=i, column=j, sticky=W+N+E+S, padx=0, pady=0)
        

def main():
    global heuristicNo, size, controlPanel, grid, statusBar
    
    arg = sys.argv

    size = (int(arg[2]), int(arg[2]))
    heuristicNo = int(arg[1])
    
    root = Tk()
    root.geometry("900x900+80+20")
    root.title("Sliding Blocks")

    lastAction = None
    search = None
    
    emptyState = generateGrid(size, 0)
    
    controlPanel = ControlPanel(root)
    grid = Grid(root, emptyState)
    statusBar = StatusBar(root)
    
    controlPanel.generate()
    
    
    
    root.mainloop()
    

if __name__ == '__main__':
    main()  
    
    
    
  
    
    
    
    

