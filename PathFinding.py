from tkinter import *
from queue import PriorityQueue
from tkinter import messagebox
from time import *
def rgbtohex(r,g,b):
    return f'#{r:01x}{g:02x}{b:02x}'

WIN = Tk()
WIN.title("PathFinding Visualiser By Anthony Ouch")
LENGTH = 30
WIN.configure(background=rgbtohex(25,73,114))

placing_nodestate = 0 # 1 represents start_node, 2 represents endnode, 3 represents wallnode, 4 means erase

grid = [['None' for _ in range(LENGTH)] for _ in range(LENGTH)]
started = False

class Spot:
    def __init__(self, y, x, win, total_rows):
        self.win = win
        self.y = y
        self.x = x
        self.total_rows = total_rows
        self.neighbours = []
        self.width = 2
        self.colour = "white"
        self.button = Button(win, width = self.width, command=self.changecolour, bg="white")
        self.button.selectable = True

    def changecolour(self):
        global start_count
        global end_count
        global started
        # only place node on empty spot
        self.get_colour()
        if self.colour == "white":
            if placing_nodestate == 1:
                if all(spot.get_colour() != "orange" for row in grid for spot in row) and not started:
                    self.make_start()
                    self.button.selectable = False

            elif placing_nodestate == 2:
                if all(spot.get_colour() != "blue" for row in grid for spot in row) and not started:
                    self.make_end()
                    self.button.selectable = False

            elif placing_nodestate == 3 and not started:
                self.make_barrier()

    def get_colour(self):
        self.colour = self.button["bg"]
        return self.button["bg"]

    def get_pos(self):
        return self.y, self.x

    def is_closed(self):
        self.colour = self.button["bg"]
        return self.colour == "red"

    def make_closed(self):
        self.colour = "red"
        self.button.configure(bg=self.colour)

    def is_opened(self):
        self.colour = self.button["bg"]
        return self.colour == "green"
    def make_opened(self):
        self.colour = "green"
        self.button.configure(bg=self.colour)

    def is_barrier(self):
        self.colour = self.button["bg"]
        return self.colour == "black"

    def make_barrier(self):
        self.colour = "black"
        self.button.configure(bg=self.colour)

    def is_end(self):
        self.colour = self.button["bg"]
        return self.colour == "blue"

    def make_end(self):
        self.colour = "blue"
        self.button.configure(bg=self.colour)

    def is_start(self):
        self.colour = self.button["bg"]
        return self.colour == "orange"

    def make_start(self):
        self.colour = "orange"
        self.button.configure(bg=self.colour)

    def make_path(self):
        self.colour = "purple"
        self.button.configure(bg=self.colour)


    def reset(self):
        self.colour = "white"
        self.button.selectable = True
        self.neighbours = []
        self.button.configure(bg=self.colour)

    def draw(self):
        self.button.grid(row=self.y, column=self.x)

    def update_neighbours(self):
        global grid
        if self.y < self.total_rows - 1 and not grid[self.y + 1][self.x].is_barrier():  # DOWN
            self.neighbours.append(grid[self.y + 1][self.x])

        if self.y > 0 and not grid[self.y - 1][self.x].is_barrier():  # UP
            self.neighbours.append(grid[self.y - 1][self.x])

        if self.x < self.total_rows - 1 and not grid[self.y][self.x + 1].is_barrier():  # RIGHT
            self.neighbours.append(grid[self.y][self.x + 1])

        if self.x > 0 and not grid[self.y][self.x - 1].is_barrier():  # LEFT
            self.neighbours.append(grid[self.y][self.x - 1])

    def __lt__(self, other):
        return False

def on_drag(event):
    """ function that allows the controller to drag squares to position the
    obstacles instead of individually cliking on it"""
    global placing_nodestate

    if placing_nodestate == 3:
        x, y = WIN.winfo_pointerxy()
        btn = WIN.winfo_containing(x, y)

        if btn and hasattr(btn, "selectable") and btn.selectable == True and not started:
            btn.config(bg="black")

def on_drag_erase(event):
    global placing_nodestate
    if placing_nodestate == 4:
        x, y = WIN.winfo_pointerxy()
        btn = WIN.winfo_containing(x, y)
        if btn and hasattr(btn, "selectable") and not started:
            btn.config(bg="white")

def h(p1, p2):
    y1,x1 = p1
    y2,x2 = p2
    return abs(x1 - x2) + abs(y1 - y2)


def make_grids(rows, win):
    global grid
    for i in range(rows):
        for j in range(rows):
            spot = Spot(i, j, win, LENGTH)
            grid[i][j] = spot
            spot.draw()

def place_startnode():
    global placing_nodestate
    placing_nodestate = 1

def place_endnode():
    global placing_nodestate
    placing_nodestate = 2

def place_wallnode():
    global placing_nodestate
    placing_nodestate = 3
    WIN.bind('<B1-Motion>', on_drag)

def erase_state():
    global placing_nodestate
    placing_nodestate = 4
    WIN.bind('<B1-Motion>', on_drag_erase)


def start():
    global started
    global grid
    started = True
    start_node = None
    end_node = None
    for row in grid:
        for spot in row:
            spot.update_neighbours()
            if spot.is_start():
                start_node = spot
            if spot.is_end():
                end_node = spot

    astar(start_node, end_node)


def reconstruct_path(came_from, current):

    while current in came_from:
        current = came_from[current]

        WIN.update()
        sleep(0.008)
        current.make_path()


def astar(start, end):
    global grid
    global WIN

    if start == None or end == None:
        messagebox.showinfo("Warning", "Missing start or end node")
        clear()
        return True

    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0

    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            reconstruct_path(came_from, current)
            #start.make_start()
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                came_from[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)

                    WIN.update()
                    sleep(0.008)
                    neighbour.make_opened()

        if current != start:
            WIN.update()
            sleep(0.008)
            current.make_closed()

def clear():
    global start_count
    global end_count
    global started
    started = False
    start_count = 0
    end_count = 0
    for rows in grid:
        for spot in rows:
            spot.reset()

def make_side_buttons(rows, win):
    startnode_button = Button(win, width=10, text="Choose Start \nNode", font=("Arial", 20), command=place_startnode)
    startnode_button.grid(row=1, column=rows + 1, rowspan=4, padx=10, ipadx=10)
    endnode_button = Button(win, width=10, text="Choose End \nNode", font=("Arial", 20), command=place_endnode)
    endnode_button.grid(row=5, column=rows + 1, rowspan=4, padx=10, ipadx=10)
    wallnode_button = Button(win, width=10, text="Place \nObstacles", font=("Arial", 20), command=place_wallnode)
    wallnode_button.grid(row=9, column=rows + 1, rowspan=4, padx=10, ipadx=10)
    start_button = Button(win, width=10, text="Visualise \nPath", font=("Arial", 20), command=start)
    start_button.grid(row=13, column=rows + 1, rowspan=4, ipadx=10)
    erase_button= Button(win, width=9, text="Erase", font=("Arial", 23), command=erase_state)
    erase_button.grid(row=17, column=rows + 1, rowspan=4, ipady=12, ipadx=10)
    clear_button = Button(win, width=9, text="Clear", font=("Arial", 23), command=clear)
    clear_button.grid(row=21, column=rows + 1, rowspan=4, ipadx=10, ipady=12)
    main_menu_button = Button(win, width=10, text=" Main \nMenu", font=("Arial", 20), state = "disabled")
    main_menu_button.grid(row=25, column=rows + 1, rowspan=4, padx=10, ipadx=10)

def draw(rows, win):
    make_grids(rows, win)
    make_side_buttons(rows, win)

def main(rows, win):
    make_grids(rows, win)
    draw(rows, win)

main(LENGTH, WIN)
WIN.mainloop()
