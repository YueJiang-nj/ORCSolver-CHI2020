from z3 import *
from tkinter import *
from time import *
from PIL import Image, ImageTk
# import tkFont

# whether we want to show the window
show_window = 0

# number of widgets
N = 60

# widget need to be moved or resized 
widget_num = -1    

# mouse option
option = 0

# window size
# window_width = 460*3
window_width = 140 * N
window_height = 200*3
# window_width = randint(int((top_button_width_pref) * num_top/10), int((top_button_width_pref) * num_top/2))
# window_height = randint(int((top_button_height_pref) + (left_button_height_pref) * num_left/2), int((top_button_height_pref)*10 + (left_button_height_pref) * num_left/2))

# window_width = 200*3

# widget size
widget_width = []
widget_height = [] 
widget_left = []
widget_right = []
widget_top = []
widget_bottom = []
photos = []

# widget size
widget_size = 40

# record start time
start = time()

# create windows
root = Tk()
root.title("Canvas Layout")

# creates Optimize object
o = Optimize()

# store all the widgets
widgets = []

if show_window:
    image3 = Image.open("../../images/" + "star1.jpg")
widgets.append([Label(root), "../../images/" + "star1.jpg"])
if show_window:
    image3 = image3.resize((widget_size*3,widget_size*3), Image.ANTIALIAS)
    photo3 = ImageTk.PhotoImage(image3)
    widgets[0][0].configure(image=photo3, bg="gray85")
widgets[0].append("high")

if show_window:
    image3 = Image.open("../../images/" + "star2.jpg")
widgets.append([Label(root), "../../images/" + "star2.jpg"])
if show_window:
    image3 = image3.resize((widget_size*3,widget_size*3), Image.ANTIALIAS)
    photo3 = ImageTk.PhotoImage(image3)
    widgets[1][0].configure(image=photo3, bg="gray85")
widgets[1].append("medium")

if show_window:
    image3 = Image.open("../../images/" + "star3.jpg")
widgets.append([Label(root), "../../images/" + "star3.jpg"])
if show_window:
    image3 = image3.resize((widget_size*3,widget_size*3), Image.ANTIALIAS)
    photo3 = ImageTk.PhotoImage(image3)
    widgets[2][0].configure(image=photo3, bg="gray85")
widgets[2].append("low")

if show_window:
    image3 = Image.open("../../images/" + "star4.jpg")
widgets.append([Label(root), "../../images/" + "star4.jpg"])
if show_window:
    image3 = image3.resize((widget_size*3,widget_size*3), Image.ANTIALIAS)
    photo3 = ImageTk.PhotoImage(image3)
    widgets[3][0].configure(image=photo3, bg="gray85")
widgets[3].append("high")

if show_window:
    image3 = Image.open("../../images/" + "star5.jpg")
widgets.append([Label(root), "../../images/" + "star5.jpg"])
if show_window:
    image3 = image3.resize((widget_size*3,widget_size*3), Image.ANTIALIAS)
    photo3 = ImageTk.PhotoImage(image3)
    widgets[4][0].configure(image=photo3, bg="gray85")
widgets[4].append("high")

if show_window:
    image3 = Image.open("../../images/" + "star6.jpg")
widgets.append([Label(root), "../../images/" + "star6.jpg"])
if show_window:
    image3 = image3.resize((widget_size*3,widget_size*3), Image.ANTIALIAS)
    photo3 = ImageTk.PhotoImage(image3)
    widgets[5][0].configure(image=photo3, bg="gray85")
widgets[5].append("low")

if show_window:
    image3 = Image.open("../../images/" + "star7.jpg")
widgets.append([Label(root), "../../images/" + "star7.jpg"])
if show_window:
    image3 = image3.resize((widget_size*3,widget_size*3), Image.ANTIALIAS)
    photo3 = ImageTk.PhotoImage(image3)
    widgets[6][0].configure(image=photo3, bg="gray85")
widgets[6].append("low")

if show_window:
    image3 = Image.open("../../images/" + "star8.jpg")
widgets.append([Label(root), "../../images/" + "star8.jpg"])
if show_window:
    image3 = image3.resize((widget_size*3,widget_size*3), Image.ANTIALIAS)
    photo3 = ImageTk.PhotoImage(image3)
    widgets[7][0].configure(image=photo3, bg="gray85")
widgets[7].append("medium")

if show_window:
    image3 = Image.open("../../images/" + "star9.jpg")
widgets.append([Label(root), "../../images/" + "star9.jpg"])
if show_window:
    image3 = image3.resize((widget_size*3,widget_size*3), Image.ANTIALIAS)
    photo3 = ImageTk.PhotoImage(image3)
    widgets[8][0].configure(image=photo3, bg="gray85")
widgets[8].append("high")

if show_window:
    image3 = Image.open("../../images/" + "star10.jpg")
widgets.append([Label(root), "../../images/" + "star10.jpg"])
if show_window:
    image3 = image3.resize((widget_size*3,widget_size*3), Image.ANTIALIAS)
    photo3 = ImageTk.PhotoImage(image3)
    widgets[9][0].configure(image=photo3, bg="gray85")
widgets[9].append("medium")

for i in range(10, N):
    if show_window:
        image3 = Image.open("../../images/" + "star10.jpg")
    widgets.append([Label(root), "../../images/" + "star10.jpg"])
    if show_window:
        image3 = image3.resize((widget_size*3,widget_size*3), Image.ANTIALIAS)
        photo3 = ImageTk.PhotoImage(image3)
        widgets[i][0].configure(image=photo3, bg="gray85")
    widgets[i].append("medium")

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
            o.add_soft(w[i][0] == w[i-1][1]+ 5*3, max(15000-100*i, 100))
            o.add_soft(h[i][1] == h[i-1][1], 1000)
    else:
        for i in range(1, n):
            orw = (w[i][0] == w[0][1] + 5*3)
            andw = (w[i][0] >= w[0][1] + 5*3)
            for j in range(1, i):
                orw = Or (orw, (w[i][0] == w[j][1]+5*3))
                andw = And (andw, (w[i][0] >= w[j][1]+5*3))
            position += [Or (And(h[i][0] == h[i-1][1]+5*3, w[i][0] == w[i-1][0]), And (h[i][0] == top, andw, orw))]
            o.add_soft(h[i][0] == h[i-1][1]+ 5*3, max(15000-100*i, 100))
            o.add_soft(w[i][1] == w[i-1][1], 1000)
    o.add(boundary + position)

    # add boundary constraints
    boundary = [And (b1 == left, b2 == right, b3 == top, b4 == bottom)]
    o.add(boundary)

# add variables for boundaries to z3 
b1 = Int('b1')    # left
b2 = Int('b2')    # right
b3 = Int('b3')    # top
b4 = Int('b4')    # bottom

# add variables for the widths and heights of widgets
w = [[Int('w_%s_%s' % (i+1, j+1)) for j in range(2)] for i in range(N)]   # width
h = [[Int("h_%s_%s" % (i+1, j+1)) for j in range(2)] for i in range(N)]   # height

# defines the size of the window
if show_window:
    root.geometry(str(window_width) + "x" + str(window_height))

start = time()

# add position constraints
position_constraints(o, h, w, 5*3, window_width-5*3, 5*3, window_height-5*3, N, True, b1, b2, b3, b4)

# width constraints and height constraints
width = []
height = []

# key is block index i, value is a list of button lengths
button_dict = dict()

# key is block index i, value is a list of lengths
option_menu_dict = dict()

# add all the widget constraints
i = -1
num = -1
while num < N - 1:
    i += 1
    num += 1

    o.add_soft(w[i][1] == b2, 20000) #change
    # width += [w[i][1] - w[i][0] >= 40*3]
    # height += [h[i][1] - h[i][0] >= 40*3]

    if widgets[num][-1] == 'high' or widgets[num][-1] == 'medium' or widgets[num][-1] == 'low':

        if widgets[num][-1] == 'high':
  
            width += [And(w[i][1] - w[i][0] == widget_size*3, h[i][1] - h[i][0] == widget_size*3)]
            if i != 0:
                # makes sure all the labels in the ribbon menu are in the same row 
                width += [w[i][0] == w[i-1][1]+5*3]  
        elif widgets[num][-1] == 'medium':
            if i == 0:
                width += [Or(And(w[i][1] - w[i][0] == widget_size*3, h[i][1] - h[i][0] == widget_size*3), 
                         And(w[i][1] - w[i][0] == 1, h[i][1] - h[i][0] == 1))]
            else:
                width += [Or(And(w[i][1] - w[i][0] == widget_size*3, h[i][1] - h[i][0] == widget_size*3, w[i][0] == w[i-1][1]+5*3), 
                         And(w[i][1] - w[i][0] == 1, h[i][1] - h[i][0] == 1, w[i][0] == w[i-1][1]))]

            o.add_soft(w[i][1] - w[i][0] == widget_size*3, 2000000*3)
            o.add_soft(h[i][1] - h[i][0] == widget_size*3, 2000000*3)
            o.add_soft(w[i][1] - w[i][0] == 1, 200*3)
            o.add_soft(h[i][1] - h[i][0] == 1, 200*3)
        elif widgets[num][-1] == 'low':
            if i == 0:
                width += [Or(And(w[i][1] - w[i][0] == widget_size*3, h[i][1] - h[i][0] == widget_size*3, w[i][0] == w[i-1][1]+5*3), 
                         And(w[i][1] - w[i][0] == 1, h[i][1] - h[i][0] == 1, w[i][0] == w[i-1][1]))]
            else:
                width += [Or(And(w[i][1] - w[i][0] == widget_size*3, h[i][1] - h[i][0] == widget_size*3, w[i][0] == w[i-1][1]+5*3), 
                         And(w[i][1] - w[i][0] == 1, h[i][1] - h[i][0] == 1, w[i][0] == w[i-1][1]))]
            o.add_soft(w[i][1] - w[i][0] == widget_size*3, 2000000*3)
            o.add_soft(h[i][1] - h[i][0] == widget_size*3, 2000000*3)
            o.add_soft(w[i][1] - w[i][0] == 1, 2000*3)
            o.add_soft(h[i][1] - h[i][0] == 1, 2000*3)

    # adds hard constraints
    o.add(width + height)

# gets optimized model
if (o.check() == sat):

    # get the model from z3solver
    m = o.model()
    # print(m)

    # places widgets in the window
    for i in range(N):

        # place Label in the window
        if widgets[i][0].winfo_class() == "Label":
            if show_window:

                image3 = Image.open(widgets[i][1])
                image3 = image3.resize((int(m[w[i][1]].as_string())-int(m[w[i][0]].as_string()),
                      int(m[h[i][1]].as_string())-int(m[h[i][0]].as_string())), Image.ANTIALIAS)
                photo = ImageTk.PhotoImage(image3)
                photos.append(photo)
                widgets[i][0].configure(image=photos[-1])
                widgets[i][0].place(x=m[w[i][0]], y=m[h[i][0]], width=int(m[w[i][1]].as_string())-int(m[w[i][0]].as_string())
                    , height=int(m[h[i][1]].as_string())-int(m[h[i][0]].as_string()))


    # show the total time
    print("Time:" + str(time() - start))

          
# print "no solution" if the constraint system cannot be satisfied
else:
    print("no solution!")


# show windows
if show_window:
    mainloop()
