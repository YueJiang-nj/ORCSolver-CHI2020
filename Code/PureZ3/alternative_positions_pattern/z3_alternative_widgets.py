from z3 import *
from tkinter import *
from PIL import Image, ImageTk
# import tkFont
import time
from random import randint


# AAAA
# C

# and

# A C
# A
# A
# A

# whether we want to show the window
show_window = 0

# widths and heights
button_width = 80
button_height = 80
button_width_max = button_width + 20
button_width_min = button_width - 20
button_height_max = button_height + 20
button_height_min = button_height - 20

# number of buttons in the toolbars
num_top = 80
total = 100
num_top = randint(5, total-5)
# num_left = total - num_top
num_top = 10

# create the window
if show_window:
    root = Tk()
    root.title("Canvas Layout")

# store all the widgets
widgets = []
photos = []

# add widgets
if show_window:
    for j in range(num_top):
        image = Image.open("../../images/1.png")
        widgets.append([Label(root), "../../images/" + str(j+1) + ".png"])
        image = image.resize((button_width, button_height), Image.ANTIALIAS)
        photos.append(ImageTk.PhotoImage(image))
        widgets[j][0].configure(image=photos[-1], bg="gray85")

    image = Image.open("../../images/" + "text.jpg")
    widgets.append([Label(root), "../../images/" + "text.jpg"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[num_top][0].configure(image=photos[-1], bg="gray85")


def position_constraints(o, h, w, left, right, top, bottom, n, horizonal, b1, b2, b3, b4):

    # every widget must be in the window
    boundary = [And(w[0][0] == b1, h[0][0] == b3)]
    for i in range(n):
        boundary += [And (w[i][1] <= b2, h[i][1] <= b4)]

    # position constraints (widgets cannot be outside of the window and every 
    # widget can only be to the right of the previous widget or at the 
    # beginning of the next row)
    position = []
    if horizonal:
        for i in range(1, n):
            orh = (h[i][0] == h[0][1] + 5*3)
            andh = (h[i][0] >= h[0][1] + 5*3)
            for j in range(1, i):
                orh = Or (orh, (h[i][0] == h[j][1]+5*3))
                andh = And (andh, (h[i][0] >= h[j][1]+5*3))
            position += [Or (And(w[i][0] == w[i-1][1]+5*3, h[i][0] == h[i-1][0]), And (w[i][0] == left, andh, orh))]
            o.add_soft(w[i][0] == w[i-1][1]+ 5*3, max(150000-100*i, 100))
            o.add_soft(h[i][1] == h[i-1][1], 1000)
    else:
        for i in range(1, n):
            orw = (w[i][0] == w[0][1] + 5*3)
            andw = (w[i][0] >= w[0][1] + 5*3)
            for j in range(1, i):
                orw = Or (orw, (w[i][0] == w[j][1]+5*3))
                andw = And (andw, (w[i][0] >= w[j][1]+5*3))
            position += [Or (And(h[i][0] == h[i-1][1]+5*3, w[i][0] == w[i-1][0]), And (h[i][0] == top, andw, orw))]
            o.add_soft(h[i][0] == h[i-1][1]+ 5*3, max(150000-100*i, 100))
            o.add_soft(w[i][1] == w[i-1][1], 1000)
    o.add(boundary + position)

    # add boundary constraints
    boundary = [And (b1 == left, b2 == right, b3 == top, b4 == bottom)]
    o.add(boundary)


def top_tool(button_width, button_height, num_top, window_width, window_height):
    
    # creates Optimize object (for the layout, top toolbar, left toolbar)
    o = Optimize()
    top_toolbar = Optimize()
    left_toolbar = Optimize()

    # defines the size of the window
    if show_window:
        root.geometry(str(window_width) + "x" + str(window_height))

    # add variables for the widths and heights of widgets
    w = [[Int('w_%s_%s' % (i+1, j+1)) for j in range(2)] for i in range(2)]   # width
    h = [[Int("h_%s_%s" % (i+1, j+1)) for j in range(2)] for i in range(2)]   # height

    # add variables for boundaries to z3 
    b1 = Int('b1')    # left
    b2 = Int('b2')    # right
    b3 = Int('b3')    # top
    b4 = Int('b4')    # bottom

    position_constraints(o, h, w, 5*3, window_width-5*3, 5*3, window_height-5*3, 2, True, b1, b2, b3, b4)

    # width constraints and height constraints
    constraints = []
    constraints += [Or(And(w[0][1] - w[0][0] == b2 - b1, h[0][1] - h[0][0] == button_height,   # top toolbar
                           w[1][1] - w[1][0] == b2 - b1, h[1][1] - h[1][0] == b4 - b3 - button_height - 5*3,
                           b2 - b1 >= (button_width + 5*3) * num_top - 5*3))] 

    o.add(constraints)


    # gets optimized model
    if (o.check() == sat):
        m = o.model()
        
        # top toolbar (horizonal flow layout)
        top_toolbar_l = int(m[w[0][0]].as_string())
        top_toolbar_r = int(m[w[0][1]].as_string())
        top_toolbar_t = int(m[h[0][0]].as_string())
        top_toolbar_b = int(m[h[0][1]].as_string())

        # add variables for the widths and heights of widgets
        top_w = [[Int('w_%s_%s' % (i+1, j+1)) for j in range(2)] for i in range(num_top)]   # width
        top_h = [[Int("h_%s_%s" % (i+1, j+1)) for j in range(2)] for i in range(num_top)]   # height

        # add position constraints
        position_constraints(top_toolbar, top_h, top_w, top_toolbar_l, top_toolbar_r, top_toolbar_t, top_toolbar_b, num_top, True, b1, b2, b3, b4)
        
        # width constraints and height constraints
        width = []
        height = []

        # constraints for each button in the top toolbar
        for i in range(num_top):
            width += [top_w[i][1] - top_w[i][0] <= button_width_max]
            height += [top_h[i][1] - top_h[i][0] <= button_height_max]
            width += [top_w[i][1] - top_w[i][0] >= button_width_min]
            height += [top_h[i][1] - top_h[i][0] >= button_height_min]
            top_toolbar.add_soft(top_w[i][1] - top_w[i][0] == button_width, 1000)
            top_toolbar.add_soft(top_h[i][1] - top_h[i][0] == button_height, 1000)
        top_toolbar.add(width + height)

        # get optimized top toolbar
        if (top_toolbar.check() == sat):
            top_m = top_toolbar.model()
            for i in range(num_top):
                widget_width = int(top_m[top_w[i][1]].as_string()) - int(top_m[top_w[i][0]].as_string())
                widget_height = int(top_m[top_h[i][1]].as_string()) - int(top_m[top_h[i][0]].as_string())
                if show_window:
                    widgets[i][0].place(x=top_m[top_w[i][0]], y=top_m[top_h[i][0]], width=widget_width, height=widget_height)
        else:
            print("no solution for the toolbar")

        widget_width = int(m[w[1][1]].as_string()) - int(m[w[1][0]].as_string())
        widget_height = int(m[h[1][1]].as_string()) - int(m[h[1][0]].as_string())
        if show_window:
            widgets[-1][0].place(x=m[w[1][0]], y=m[h[1][0]], width=widget_width, height=widget_height)
    else:
        # print "No solution!"
        return False

    if show_window:
        mainloop()

def left_tool(button_width, button_height, num_top, window_width, window_height):
    
    # creates Optimize object (for the layout, top toolbar, left toolbar)
    o = Optimize()
    top_toolbar = Optimize()
    left_toolbar = Optimize()

    # defines the size of the window
    if show_window:
        root.geometry(str(window_width) + "x" + str(window_height))

    # add variables for boundaries to z3 
    b1 = Int('b1')    # left
    b2 = Int('b2')    # right
    b3 = Int('b3')    # top
    b4 = Int('b4')    # bottom

    # add variables for the widths and heights of widgets
    top_w = [[Int('w_%s_%s' % (i+1, j+1)) for j in range(2)] for i in range(num_top)]   # width
    top_h = [[Int("h_%s_%s" % (i+1, j+1)) for j in range(2)] for i in range(num_top)]   # height

    # add position constraints
    position_constraints(top_toolbar, top_h, top_w, 5*3, window_width-5*3, 5*3, window_height-5*3, num_top, False, b1, b2, b3, b4)
    
    # width constraints and height constraints
    width = []
    height = []

    # constraints for each button in the top toolbar
    for i in range(num_top):
        width += [top_w[i][1] - top_w[i][0] <= button_width_max]
        height += [top_h[i][1] - top_h[i][0] <= button_height_max]
        width += [top_w[i][1] - top_w[i][0] >= button_width_min]
        height += [top_h[i][1] - top_h[i][0] >= button_height_min]
        top_toolbar.add_soft(top_w[i][1] - top_w[i][0] == button_width, 1000)
        top_toolbar.add_soft(top_h[i][1] - top_h[i][0] == button_height, 1000)
    top_toolbar.add(width + height)

    # get optimized top toolbar
    if (top_toolbar.check() == sat):
        top_m = top_toolbar.model()
        for i in range(num_top):
            widget_width = int(top_m[top_w[i][1]].as_string()) - int(top_m[top_w[i][0]].as_string())
            widget_height = int(top_m[top_h[i][1]].as_string()) - int(top_m[top_h[i][0]].as_string())
            if show_window:
                widgets[i][0].place(x=top_m[top_w[i][0]], y=top_m[top_h[i][0]], width=widget_width, height=widget_height)
        if show_window:
            widgets[-1][0].place(x=int(top_m[top_w[-1][1]].as_string()) + 5*3, y=5*3, width=window_width - (int(top_m[top_w[-1][1]].as_string()) + 2*5*3), height=window_height-2*5*3)
    else:
        print("no solution for the toolbar")

    if show_window:
        mainloop()
    
window_width = 2000
window_height = 50 * 100
window_width = randint(int((button_width) * num_top/10), int((button_width) * num_top/2))
window_height = randint(int((button_height) + (button_height) * num_top/2), int((button_height)*10 + (button_height) * num_top/2))

# run the solver
start = time.time()
if not top_tool(button_width, button_height, num_top, window_width, window_height):
    left_tool(button_width, button_height, num_top, window_width, window_height)

# compute the time it takes
print("Time: " + str(time.time() - start))



     






