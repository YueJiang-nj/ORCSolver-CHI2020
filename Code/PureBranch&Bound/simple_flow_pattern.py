from tkinter import *
from PIL import Image, ImageTk
from flow_solver import *
from orclayout_classes import *
import orclayout_classes
import time
from random import randint

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


# whether we want to show the window
show_window = 0

# widths and heights
top_button_width_min = 40
top_button_width_pref = 80
top_button_width_max = 120
top_button_height_min = 40
top_button_height_pref = 80
top_button_height_max = 120
left_button_width_min = 40
left_button_width_pref = 80
left_button_width_max = 120
left_button_height_min = 40
left_button_height_pref = 80
left_button_height_max = 120
textbox_min = 0
textbox_pref = 700
textbox_max = 1000000


# number of buttons in the toolbars
total = 100
num_top = randint(10, total-10)
num_left = total - num_top

# window size
window_width = int((top_button_width_pref) * num_top/6)  
window_height = int((top_button_height_pref)*4 + (left_button_height_pref) * num_left/2)
window_width = randint(int((top_button_width_pref) * num_top/10), int((top_button_width_pref) * num_top/2))
window_height = randint(int((top_button_height_pref) + (left_button_height_pref) * num_left/2), int((top_button_height_pref)*10 + (left_button_height_pref) * num_left/2))

# create the window
if show_window:
    root = Tk()
    root.title("Canvas Layout")
    time_panel = Tk()
    time_panel.title("Time")
    time_frame = Frame(time_panel)
    time_frame.pack(side=TOP)
    Label(time_frame, text="Time: ", font = "Times 30").pack(side=LEFT)
    time_result = Entry(time_frame, font = "Helvetica 30")
    time_result.config(width=10)
    time_result.insert(0, "")
    time_result.pack(side=LEFT)

# store all the widgets
widgets = []
photos = []

# add widgets
if show_window:
    for j in range(num_top):
        if num_top <= 10:
            image3 = Image.open("../images/" + str(j+1) + ".png")
            widgets.append([Label(root), str(j+1) + ".png"])
        elif num_top <= 20:
            image3 = Image.open("../images/" + str(j%10+1) + ".png")
            widgets.append([Label(root), str(j%10+1) + ".png"])
        else: 
            image3 = Image.open("../images/" + "1" + ".png")
            widgets.append([Label(root), "1" + ".png"])
        image3 = image3.resize((top_button_width_pref, top_button_height_pref), Image.ANTIALIAS)
        photos.append(ImageTk.PhotoImage(image3))
        widgets[j][0].configure(image=photos[-1], bg="gray85")

    for j in range(num_top, num_top + num_left):
        if num_top <= 20: 
            image3 = Image.open("../images/" + str(j+1-num_top)*2 + ".png")
            widgets.append([Label(root), str(j+1-num_top)*2 + ".png"])
        else:
            image3 = Image.open("../images/" + "2" + ".png")
            widgets.append([Label(root), "2" + ".png"])
        image3 = image3.resize((top_button_width_pref, top_button_height_pref), Image.ANTIALIAS)
        photos.append(ImageTk.PhotoImage(image3))
        widgets[j][0].configure(image=photos[-1], bg="gray85")

    image3 = Image.open("../images/" + "text.jpg")
    widgets.append([Label(root), "text.jpg"])
    photos.append(ImageTk.PhotoImage(image3))
    widgets[num_top + num_left][0].configure(image=photos[-1], bg="gray85")

# defines the size of the window
if show_window:
    root.geometry(str(window_width) + "x" + str(window_height))


def main():
    
    # create all the widget objects
    top_widgets = []
    left_widgets = []
    for i in range(num_top):
        top_widgets.append(ORCWidget("HF_" + str(i), \
                                      [top_button_width_min, top_button_width_pref, \
                                       top_button_width_max, top_button_height_min, \
                                       top_button_height_pref, top_button_height_max]))

    for i in range(num_top, num_top + num_left):
        left_widgets.append(ORCWidget("VF_" + str(i), \
                                      [left_button_width_min, left_button_width_pref, \
                                       left_button_width_max, left_button_height_min, \
                                       left_button_height_pref, left_button_height_max]))

    # create the flow layout pattern
    # the pattern is Column(HorizontalFlow, Row(VerticalFlow, TextBox))
    # create the tree for the flow layout pattern
    # pattern is the root node, Column is the child node of pattern,
    # HorizontalFlow is the child of Column, Row is the child of HorizontalFlow...
    column = ORCColumn("column", None, window_width, window_height)
    horizonalflow = HorizontalFlow("HF", top_widgets, column)
    row = ORCRow("row", horizonalflow)
    verticalflow = VerticalFlow("VF", left_widgets, row)
    textbox = ORCWidget("textbox", [textbox_min, textbox_pref, textbox_max, \
                                    textbox_min, textbox_pref, textbox_max], verticalflow)
    textbox.weight = 0.00001
    column.define_sublayouts([horizonalflow, row])
    row.define_sublayouts([verticalflow, textbox])

    # Solve the system
    start = time.time()
    column.solve()
    # compute the time it takes
    print("Time: " + str(time.time() - start))
    if show_window:
        time_result.insert(0, str(time.time() - start))
    best_leaf, best_leaf_result, best_leaf_loss = column.get_best()

    # TODO: I should set a pointer pointing to specific flows
    horizonalflow_row_height = best_leaf.parent.parent.parent.best_row_height
    horizonalflow_row_width = best_leaf.parent.parent.parent.best_row_width
    verticalflow_row_height = best_leaf.parent.best_row_height
    verticalflow_row_width = best_leaf.parent.best_row_width

    # get the positions of sublayouts
    HF_l = best_leaf_result["HF_l"]
    HF_r = best_leaf_result["HF_r"]
    HF_t = best_leaf_result["HF_t"]
    HF_b = best_leaf_result["HF_b"]
    VF_l = best_leaf_result["VF_l"]
    VF_r = best_leaf_result["VF_r"]
    VF_t = best_leaf_result["VF_t"]
    VF_b = best_leaf_result["VF_b"]
    textbox_l = best_leaf_result["textbox_l"]
    textbox_r = best_leaf_result["textbox_r"]
    textbox_t = best_leaf_result["textbox_t"]
    textbox_b = best_leaf_result["textbox_b"]

    # place the widgets in top toolbar in the window
    left = HF_l
    top = HF_t
    index = 0
    for i in range(len(horizonalflow_row_width)):
        for j in range(len(horizonalflow_row_width[i])):
            widget_width = horizonalflow_row_width[i][j]
            widget_height = horizonalflow_row_height[i]
            if show_window:
                widgets[index][0].place(x=left, y=top, width=widget_width, height=widget_height)
            left += widget_width
            index += 1
        left = HF_l
        top += widget_height

    # place the widgets in left toolbar in the window
    left = VF_l
    top = VF_t
    index = num_top
    for i in range(len(verticalflow_row_height)):
        for j in range(len(verticalflow_row_height[i])):
            widget_width = verticalflow_row_width[i]
            widget_height = verticalflow_row_height[i][j]
            if show_window:
                widgets[index][0].place(x=left, y=top, width=widget_width, height=widget_height)
            top += widget_height
            index += 1
        left += widget_width
        top = VF_t

    if show_window:
        widgets[-1][0].place(x=textbox_l, y=textbox_t, width=textbox_r - textbox_l, height=textbox_b - textbox_t)

    # show windows
    if show_window:
        mainloop()

# callback for mouse click
def mouse_click(event):  

    global resize_window

    # get the position of the mouse
    locationx = root.winfo_pointerx() - root.winfo_rootx()
    locationy = root.winfo_pointery() - root.winfo_rooty()

    resize_window = False

    # locate the mouse
    if abs(locationx - window_width) < 30 and abs(locationy - window_height) < 30:
        print("window!")
        resize_window = True


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
        root.geometry(str(window_width) + "x" + str(window_height))
        main()

# add mouse click functions
if show_window:
    root.bind("<Button-1>", mouse_click)
    root.bind("<ButtonRelease-1>", mouse_release)
main()










