from z3 import *
from tkinter import *
from PIL import Image, ImageTk
import time
from random import randint

# whether we want to show the window
show_window = 1

# create windows
root = Tk()
root.title("Canvas Layout")
property_panel = Tk()
property_panel.title("Property Panel")
time_panel = Tk()
time_panel.title("Time")

time_frame = Frame(time_panel)
time_frame.pack(side=TOP)
Label(time_frame, text="Time: ", font = "Times 30").pack(side=LEFT)
time_result = Entry(time_frame, font = "Helvetica 30")
time_result.config(width=10)
time_result.insert(0, "")
time_result.pack(side=LEFT)

# widths and heights
button_width = 80
button_height = 80
button_width_max = button_width + 20
button_width_min = button_width - 2
button_height_max = button_height + 20
button_height_min = button_height - 2
window_width = None
window_height = None

# number of buttons in the toolbars
total = 100
num_top = randint(5, total-5)
num_left = total - num_top

# store all the widgets
widgets = []
photos = []

# whether connected or not
option = None

# whether the window size is changed
resize_window = False

# add widgets
for j in range(num_top):
    if show_window:
        image3 = Image.open("../../images/" + str(j%10+1) + ".png")
    widgets.append([Label(root), "../../images/" + str(j%10+1) + ".png"])
    if show_window:
        image3 = image3.resize((button_width,button_height), Image.ANTIALIAS)
        photos.append(ImageTk.PhotoImage(image3))
        widgets[j][0].configure(image=photos[-1], bg="gray85")

for j in range(num_top, num_top + num_left):
    if show_window:
        image3 = Image.open("../../images/color" + str(j+1-num_top)*2 + ".png")
    widgets.append([Label(root), "../../images/color" + str(j+1-num_top)*2 + ".png"])
    if show_window:
        image3 = image3.resize((button_width,button_height), Image.ANTIALIAS)
        photos.append(ImageTk.PhotoImage(image3))
        widgets[j][0].configure(image=photos[-1], bg="gray85")

image3 = Image.open("../../images/" + "text.jpg")
widgets.append([Label(root), "../../images/" + "text.jpg"])
# image3 = image3.resize((button_width,button_height), Image.ANTIALIAS)
photos.append(ImageTk.PhotoImage(image3))
widgets[num_top + num_left][0].configure(image=photos[-1], bg="gray85")


# callback for mouse click
def mouse_click(event):  

    global resize_window

    # get the position of the mouse
    locationx = root.winfo_pointerx() - root.winfo_rootx()
    locationy = root.winfo_pointery() - root.winfo_rooty()

    resize_window = False

    # locate the mouse
    if abs(locationx - window_width) < 50 and abs(locationy - window_height) < 50:
        print("window!")
        resize_window = True

step = 0
# callback for mouse release
def mouse_release(event):

    global window_width, window_height, root

    # get the mouse position
    currentx = root.winfo_pointerx() - root.winfo_rootx()
    currenty = root.winfo_pointery() - root.winfo_rooty()

   
    # clears up the window
    for frame in root.winfo_children():
        frame.grid_forget()

    # resize the window
    if resize_window == True:
        window_width = currentx
        window_height = currenty

        global step
        if step == 0:
            window_width = 560
            window_height = 640
        elif step == 1:
            window_width = 640
            window_height = 560
        elif step == 2:
            window_width = 800
            window_height = 640
        step += 1

        print(window_width, window_height)
        root.geometry(str(window_width) + "x" + str(window_height))

        print(option)
        if option == "connected":
            connected()
        elif option == "unconnected":
            unconnected()

# add mouse click functions
root.bind("<Button-1>", mouse_click)
root.bind("<ButtonRelease-1>", mouse_release)

def position_constraints(o, h, w, left, right, top, bottom, n, horizonal):

    # every widget must be in the window
    boundary = [And(w[0][0] == left, h[0][0] == top)]
    for i in range(n):
        boundary += [And (w[i][1] <= right, h[i][1] <= bottom)]

    # position constraints (widgets cannot be outside of the window and every 
    # widget can only be to the right of the previous widget or at the 
    # beginning of the next row)
    position = []
    if horizonal:
        for i in range(1, n):
            orh = (h[i][0] == h[0][1])
            andh = (h[i][0] >= h[0][1])
            for j in range(1, i):
                orh = Or (orh, (h[i][0] == h[j][1]))
                andh = And (andh, (h[i][0] >= h[j][1]))
            position += [Or (And(w[i][0] == w[i-1][1], h[i][0] == h[i-1][0]), And (w[i][0] == left, andh, orh))]
            o.add_soft(w[i][0] == w[i-1][1], max(15000000-100*i, 100))
            o.add_soft(h[i][1] == h[i-1][1], 1000)
    else:
        for i in range(1, n):
            orw = (w[i][0] == w[0][1])
            andw = (w[i][0] >= w[0][1])
            for j in range(1, i):
                orw = Or (orw, (w[i][0] == w[j][1]))
                andw = And (andw, (w[i][0] >= w[j][1]))
            position += [Or (And(h[i][0] == h[i-1][1], w[i][0] == w[i-1][0]), And (h[i][0] == top, andw, orw))]
            o.add_soft(h[i][0] == h[i-1][1], max(15000000-100*i, 100))
            o.add_soft(w[i][1] == w[i-1][1], 1000)
    o.add(boundary + position)


def connected():
    # BBAAAAAA
    # B
    # B C

    # and

    # AAAA
    # A
    # A
    # B
    # B C
    # B
    # B
    global window_width, window_height, option
    option = "connected"

    # window size
    size = 0
    size = -2
    size = 1
    size = 2
    if window_width == None and window_height == None:
        window_width = int((button_width) * (num_top+size)/4)  
        window_height = int((button_width)*4 + (button_height) * (num_left+size)/2)
        window_width = randint(int((top_button_width_pref) * num_top/10), int((top_button_width_pref) * num_top/2))
        window_height = randint(int((top_button_height_pref) + (left_button_height_pref) * num_left/2), int((top_button_height_pref)*10 + (left_button_height_pref) * num_left/2))

    # adjusted number of buttons in the toolbars
    adjusted_num_top = int(round(float(num_top) / (window_width / button_width))) \
                        * (window_width / button_width)
    adjusted_num_left = num_top + num_left - adjusted_num_top

    # creates Optimize object (for the layout, top toolbar, left toolbar)
    o = Optimize()

    start = time.time()

    # defines the size of the window
    if show_window:
        root.geometry(str(window_width) + "x" + str(window_height))

    # add variables for the widths and heights of widgets
    w = [[Int('w_%s_%s' % (i+1, j+1)) for j in range(2)] for i in range(3)]   # width
    h = [[Int("h_%s_%s" % (i+1, j+1)) for j in range(2)] for i in range(3)]   # height

    # add variables for the widths and heights of widgets
    top_w = [[Int('top_w_%s_%s' % (i+1, j+1)) for j in range(2)] for i in range(adjusted_num_top)]   # width
    top_h = [[Int("top_h_%s_%s" % (i+1, j+1)) for j in range(2)] for i in range(adjusted_num_top)]   # height

    # add variables for the widths and heights of widgets
    left_w = [[Int('left_w_%s_%s' % (i+1, j+1)) for j in range(2)] for i in range(adjusted_num_left)]   # width
    left_h = [[Int("left_h_%s_%s" % (i+1, j+1)) for j in range(2)] for i in range(adjusted_num_left)]   # height

    # add variables for boundaries to z3 
    b1 = Int('b1')    # left
    b2 = Int('b2')    # right
    b3 = Int('b3')    # top
    b4 = Int('b4')    # bottom
    o.add([b1 == 0, b2 == window_width, b3 == 0, b4 == window_height])

    # boundary constraints
    boundary = []
    boundary += [w[0][0] == b1, w[0][1] == b2, h[0][0] == b3, h[0][1] == top_h[-1][1]]
    boundary += [w[1][0] == b1, w[1][1] == left_w[-1][1], h[1][0] == h[0][1], h[1][1] == b4]
    boundary += [w[2][0] == w[1][1], w[2][1] == b2, h[2][0] == h[0][1], h[2][1] == b4]
    o.add(boundary)

    # add position constraints
    position_constraints(o, top_h, top_w, w[0][0], w[0][1], h[0][0], h[0][1], adjusted_num_top, True)
    
    # width constraints and height constraints
    width = []
    height = []

    # constraints for each button in the top toolbar
    for i in range(adjusted_num_top):
        width += [top_w[i][1] - top_w[i][0] <= button_width_max]
        height += [top_h[i][1] - top_h[i][0] <= button_height_max]
        width += [top_w[i][1] - top_w[i][0] >= button_width_min]
        height += [top_h[i][1] - top_h[i][0] >= button_height_min]
        o.add_soft(top_w[i][1] - top_w[i][0] == button_width, 1000)
        o.add_soft(top_h[i][1] - top_h[i][0] == button_height, 1000)
    o.add(width + height)

    # add position constraints
    position_constraints(o, left_h, left_w, w[1][0], w[1][1], h[1][0], h[1][1], adjusted_num_left, False)
    
    # width constraints and height constraints
    width = []
    height = []

    # constraints for each button in the left toolbar
    for i in range(adjusted_num_left):
        width += [left_w[i][1] - left_w[i][0] <= button_width_max]
        height += [left_h[i][1] - left_h[i][0] <= button_height_max]
        width += [left_w[i][1] - left_w[i][0] >= button_width_min]
        height += [left_h[i][1] - left_h[i][0] >= button_height_min]
        o.add_soft(left_w[i][1] - left_w[i][0] == button_width, 1000)
        o.add_soft(left_h[i][1] - left_h[i][0] == button_height, 1000)
    o.add(width + height)

    # get optimized model
    # Solve the system
    if (o.check() == sat):
        m = o.model()
        for i in range(adjusted_num_top):
            widget_width = int(m[top_w[i][1]].as_string()) - int(m[top_w[i][0]].as_string())
            widget_height = int(m[top_h[i][1]].as_string()) - int(m[top_h[i][0]].as_string())
            if show_window:
                widgets[i][0].place(x=m[top_w[i][0]], y=m[top_h[i][0]], width=widget_width, height=widget_height)
        for i in range(adjusted_num_left):
            widget_width = int(m[left_w[i][1]].as_string()) - int(m[left_w[i][0]].as_string())
            widget_height = int(m[left_h[i][1]].as_string()) - int(m[left_h[i][0]].as_string())
            if show_window:
                widgets[adjusted_num_top + i][0].place(x=m[left_w[i][0]], y=m[left_h[i][0]], width=widget_width, height=widget_height)
        widget_width = int(m[w[2][1]].as_string()) - int(m[w[2][0]].as_string())
        widget_height = int(m[h[2][1]].as_string()) - int(m[h[2][0]].as_string())
        if show_window:
            widgets[-1][0].place(x=m[w[2][0]], y=m[h[2][0]], width=widget_width, height=widget_height)
    else:
        print("no solution for layout")

    # compute the time it takes
    print("Time: " + str(time.time() - start))
    time_result.insert(0, str(time.time() - start))

    # show windows
    mainloop()


def unconnected():
    # % large:
    # % AAAAAA
    # % B
    # % B C
    # % B
    # % B
    # %
    # % small:
    # % AAA
    # % AAA
    # % BBC
    # % BB

    global window_width, window_height, option
    option = "unconnected"

    # creates Optimize object (for the layout, top toolbar, left toolbar)
    o = Optimize()

    start = time.time()

    # window size
    # large
    if window_width == None and window_height == None:
        # window_width = (button_width + 5*3) * num_top + 5*3
        # window_height = (button_height + 5*3) + (button_height + 5*3) * num_left + 5*3
    # small
        window_width = int((button_width) * num_top/4)  
        window_height = int((button_width)*4 + (button_height) * num_left/2)
        window_width = randint(int((top_button_width_pref) * num_top/10), int((top_button_width_pref) * num_top/2))
        window_height = randint(int((top_button_height_pref) + (left_button_height_pref) * num_left/2), int((top_button_height_pref)*10 + (left_button_height_pref) * num_left/2))


    # defines the size of the window
    if show_window:
        root.geometry(str(window_width) + "x" + str(window_height))

    # add variables for the widths and heights of widgets
    w = [[Int('w_%s_%s' % (i+1, j+1)) for j in range(2)] for i in range(3)]   # width
    h = [[Int("h_%s_%s" % (i+1, j+1)) for j in range(2)] for i in range(3)]   # height

    # add variables for the widths and heights of widgets
    top_w = [[Int('top_w_%s_%s' % (i+1, j+1)) for j in range(2)] for i in range(num_top)]   # width
    top_h = [[Int("top_h_%s_%s" % (i+1, j+1)) for j in range(2)] for i in range(num_top)]   # height

    # add variables for the widths and heights of widgets
    left_w = [[Int('left_w_%s_%s' % (i+1, j+1)) for j in range(2)] for i in range(num_left)]   # width
    left_h = [[Int("left_h_%s_%s" % (i+1, j+1)) for j in range(2)] for i in range(num_left)]   # height

    # add variables for boundaries to z3 
    b1 = Int('b1')    # left
    b2 = Int('b2')    # right
    b3 = Int('b3')    # top
    b4 = Int('b4')    # bottom
    o.add([b1 == 0, b2 == window_width, b3 == 0, b4 == window_height])

    # boundary constraints
    boundary = []
    boundary += [w[0][0] == b1, w[0][1] == b2, h[0][0] == b3, h[0][1] == top_h[-1][1]]
    boundary += [w[1][0] == b1, w[1][1] == left_w[-1][1], h[1][0] == h[0][1], h[1][1] == b4]
    boundary += [w[2][0] == w[1][1], w[2][1] == b2, h[2][0] == h[0][1], h[2][1] == b4]
    o.add(boundary)

    # add position constraints
    position_constraints(o, top_h, top_w, w[0][0], w[0][1], h[0][0], h[0][1], num_top, True)
    
    # width constraints and height constraints
    width = []
    height = []

    # constraints for each button in the top toolbar
    for i in range(num_top):
        width += [top_w[i][1] - top_w[i][0] <= button_width_max]
        height += [top_h[i][1] - top_h[i][0] <= button_height_max]
        width += [top_w[i][1] - top_w[i][0] >= button_width_min]
        height += [top_h[i][1] - top_h[i][0] >= button_height_min]
        o.add_soft(top_w[i][1] - top_w[i][0] == button_width, 1000)
        o.add_soft(top_h[i][1] - top_h[i][0] == button_height, 1000)
    o.add(width + height)

    # add position constraints
    position_constraints(o, left_h, left_w, w[1][0], w[1][1], h[1][0], h[1][1], num_left, False)
    
    # width constraints and height constraints
    width = []
    height = []

    # constraints for each button in the left toolbar
    for i in range(num_left):
        width += [left_w[i][1] - left_w[i][0] <= button_width_max]
        height += [left_h[i][1] - left_h[i][0] <= button_height_max]
        width += [left_w[i][1] - left_w[i][0] >= button_width_min]
        height += [left_h[i][1] - left_h[i][0] >= button_height_min]
        o.add_soft(left_w[i][1] - left_w[i][0] == button_width, 1000)
        o.add_soft(left_h[i][1] - left_h[i][0] == button_height, 1000)
    o.add(width + height)

    # get optimized left toolbar
    # get optimized top toolbar
    if (o.check() == sat):
        m = o.model()
        print(int(m[w[1][0]].as_string()), int(m[w[1][1]].as_string()), int(m[h[1][0]].as_string()), int(m[h[1][1]].as_string()))
        for i in range(num_top):
            print(int(m[top_w[i][0]].as_string()), int(m[top_w[i][1]].as_string()))
            widget_width = int(m[top_w[i][1]].as_string()) - int(m[top_w[i][0]].as_string())
            widget_height = int(m[top_h[i][1]].as_string()) - int(m[top_h[i][0]].as_string())
            if show_window:
                widgets[i][0].place(x=m[top_w[i][0]], y=m[top_h[i][0]], width=widget_width, height=widget_height)
        for i in range(num_left):
            print(int(m[left_w[i][0]].as_string()), int(m[left_w[i][1]].as_string()))
            widget_width = int(m[left_w[i][1]].as_string()) - int(m[left_w[i][0]].as_string())
            widget_height = int(m[left_h[i][1]].as_string()) - int(m[left_h[i][0]].as_string())
            if show_window:
                widgets[num_top + i][0].place(x=m[left_w[i][0]], y=m[left_h[i][0]], width=widget_width, height=widget_height)
        widget_width = int(m[w[2][1]].as_string()) - int(m[w[2][0]].as_string())
        widget_height = int(m[h[2][1]].as_string()) - int(m[h[2][0]].as_string())
        if show_window:
            widgets[-1][0].place(x=m[w[2][0]], y=m[h[2][0]], width=widget_width, height=widget_height)
    else:
        print("no solution for layout")

    # compute the time it takes
    print("Time: " + str(time.time() - start))
    time_result.insert(0, str(time.time() - start))

    # show windows
    mainloop()


v = IntVar()
v.set("1")
Radiobutton(property_panel, text="   Connected   ", variable=v, value=1, font=('Helvetica',(15)), command=connected).pack(anchor=W)
Radiobutton(property_panel, text="   Unconnected   ", variable=v, value=2, font=('Helvetica',(15)), command=unconnected).pack(anchor=W)

# show windows
mainloop()