from tkinter import *
import math
from queue import PriorityQueue
def rgbtohex(r,g,b):
    return f'#{r:01x}{g:02x}{b:02x}'

WIN = Tk()
WIN.title("PathFinding Visualiser By Anthony Ouch")
LENGTH = 30
WIN.configure(background=rgbtohex(25,73,114))
class Spot:
    def __init__(self, y, x, win):
        self.win = win
        self.y = y
        self.x = x
        self.colour = "white"
        self.neighbours = []
        self.width = 2
        self.button = Button(win, width = self.width)
    def get_pos(self):
        return self.row, self.col
    def is_closed(self):
        return self.colour == "red"
    def make_closed(self):
        self.colour = "red"
    def is_opened(self):
        return self.colour == "green"
    def make_opened(self):
        self.colour = "green"
    def is_barrier(self):
        return self.colour == "black"
    def make_barrier(self):
        self.colour = "black"
    def is_end(self):
        return self.colour == "blue"
    def make_end(self):
        self.colour = "blue"
    def is_start(self):
        return self.colour == "orange"
    def make_start(self):
        self.colour = "orange"
    def reset(self):
        self.colour = "white"
    def draw(self, win):
        self.button.grid(row=self.y, column=self.x)
    def update_neighbours(self):
        pass
    def __lt__(self, other):
        return False

def h(p1, p2):
    y1,x1 = p1
    y2,x2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grids(rows, win):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, win)
            grid[i].append(spot)
            spot.draw(win)
    return grid

def make_side_buttons(rows, win):
    startnode_button = Button(win, width=10, text="Choose Start \nNode", font=("Arial", 20))
    startnode_button.grid(row=3, column=rows + 1, rowspan=4, padx=10, ipadx=10)
    endnode_button = Button(win, width=10, text="Choose End \nNode", font=("Arial", 20))
    endnode_button.grid(row=7, column=rows + 1, rowspan=4, padx=10, ipadx=10)
    wallnode_button = Button(win, width=10, text="Place \nObstacles", font=("Arial", 20))
    wallnode_button.grid(row=11, column=rows + 1, rowspan=4, padx=10, ipadx=10)
    start_button = Button(win, width=10, text="Visualise \nPath", font=("Arial", 20))
    start_button.grid(row=15, column=rows + 1, rowspan=4, ipadx=10)
    clear_button = Button(win, width=9, text="Clear", font=("Arial", 23))
    clear_button.grid(row=19, column=rows + 1, rowspan=4, ipadx=10, ipady=12)
    main_menu_button = Button(win, width=10, text=" Main \nMenu", font=("Arial", 20))
    main_menu_button.grid(row=23, column=rows + 1, rowspan=4, padx=10, ipadx=10)




def draw(rows, win):
    make_grids(rows, win)
    make_side_buttons(rows, win)

draw(LENGTH, WIN)


WIN.mainloop()
