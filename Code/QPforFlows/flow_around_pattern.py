from tkinter import *
from PIL import Image, ImageTk
from flow_solver import *
from orclayout_classes import *
import orclayout_classes
import time
from random import randint


# whether we want to show the window
show_window = 1

# widths and heights
top_button_width_min = 30
top_button_width_pref = 80
top_button_width_max = 120
top_button_height_min = 30
top_button_height_pref = 80
top_button_height_max = 120
left_button_width_min = 30
left_button_width_pref = 80
left_button_width_max = 120
left_button_height_min = 30
left_button_height_pref = 80
left_button_height_max = 120
textbox_min = 0
textbox_pref = 700
textbox_max = 1000000


# number of buttons
num = 10

# window size
window_width = 6000
window_height = 6000
fixed_left = 200
fixed_right = 360
fixed_top = 200
fixed_bottom = 360
fixed_left = 191
fixed_right = 351
fixed_top = 277
fixed_bottom = 437
fixed_left = randint(0, window_width - 101)
fixed_right = randint(fixed_left + 100, window_width)
fixed_top = randint(0, window_height - 101)
fixed_bottom = randint(fixed_top + 100, window_height)


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
    for j in range(num):
        image = Image.open("../images/" + "pineapple.jpg")
        widgets.append([Label(root), "pineapple.jpg"])
        image = image.resize((top_button_width_pref, top_button_height_pref), Image.ANTIALIAS)
        photos.append(ImageTk.PhotoImage(image))
        widgets[j][0].configure(image=photos[-1])

    image = Image.open("../images/" + "chi2020.png")
    image = image.resize((fixed_right - fixed_left, fixed_bottom - fixed_top), Image.ANTIALIAS)
    widgets.append([Label(root), "chi2020.png"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[-1][0].configure(image=photos[-1])

# defines the size of the window
if show_window:
    root.geometry(str(window_width) + "x" + str(window_height))


def main():

    print(window_width, window_height)
    
    # create all the widget objects
    flow_widgets = []
    for i in range(num):
        flow_widgets.append(ORCWidget(str(i), \
                                      [top_button_width_min, top_button_width_pref, \
                                       top_button_width_max, top_button_height_min, \
                                       top_button_height_pref, top_button_height_max]))

    # create the layout pattern
    column = ORCColumn("column", None, window_width, window_height)
    flow = FlowAroundFix("flow", fixed_top, fixed_bottom,  fixed_left, fixed_right,flow_widgets, column)
    column.define_sublayouts([flow])

    # Solve the system
    start = time.time()
    column.solve()
    # compute the time it takes
    print("Time: " + str(time.time() - start))
    if show_window:
        time_result.insert(0, str(time.time() - start))
    best_leaf, best_leaf_result, best_leaf_loss = column.get_best()

    # get the positions of widgets
    if best_leaf == None:
        print("No Solution!")
        exit()
    result_index_upper = best_leaf.best_result_index_upper
    result_index_middle = best_leaf.best_result_index_middle
    result_index_lower = best_leaf.best_result_index_lower

    # place the widgets in upper area
    index = 0
    for i in range(num):
        widget_width = best_leaf_result[str(index) + "_r"] - best_leaf_result[str(index) + "_l"]
        widget_height = best_leaf_result[str(index) + "_b"] - best_leaf_result[str(index) + "_t"]

        widgets[index][0].place(x=best_leaf_result[str(index) + "_l"], \
                                y=best_leaf_result[str(index) + "_t"], \
                                width=widget_width, height=widget_height)
        index += 1

 
    widgets[-1][0].place(x=fixed_left, y=fixed_top, width=fixed_right - fixed_left, height=fixed_bottom - fixed_top)

    # show windows
    if show_window:
        mainloop()

# callback for mouse click
def mouse_click(event):  

    global move_fixed_area
    global locationx, locationy

    # get the position of the mouse
    locationx = root.winfo_pointerx() - root.winfo_rootx()
    locationy = root.winfo_pointery() - root.winfo_rooty()

    move_fixed_area = False

    # locate the mouse
    if locationx >= fixed_left and locationx <= fixed_right \
       and locationy >= fixed_top and locationy <= fixed_bottom:
        print("Move!")
        move_fixed_area = True


# callback for mouse release
step = 0
# callback for mouse release
def mouse_release(event):

    global fixed_left, fixed_right, fixed_top, fixed_bottom, root

    # get the mouse position
    currentx = root.winfo_pointerx() - root.winfo_rootx()
    currenty = root.winfo_pointery() - root.winfo_rooty()

    # clears up the window
    for frame in root.winfo_children():
        frame.grid_forget()

    # resize the window
    if move_fixed_area == True:
        width_move = currentx - locationx
        height_move = currenty - locationy

        global step
        if step == 0:
            width_move = 143
            height_move = -130
        elif step == 1:
            width_move = 341-334
            height_move = 303-127
        elif step == 2:
            width_move = 80-341
            height_move = 101-303-20
        step += 1
        
        fixed_left += width_move
        fixed_right += width_move
        fixed_top += height_move
        fixed_bottom += height_move
        main()

# add mouse click functions
if show_window:
    root.bind("<Button-1>", mouse_click)
    root.bind("<ButtonRelease-1>", mouse_release)
main()










