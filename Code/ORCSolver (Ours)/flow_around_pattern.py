from tkinter import *
from PIL import Image, ImageTk
from flow_solver import *
from orclayout_classes import *
import orclayout_classes
import time
from random import randint


# whether we want to show the window
show_window = 0

# widths and heights
top_button_width_min = 50
top_button_width_pref = 80
top_button_width_max = 120
top_button_height_min = 50
top_button_height_pref = 80
top_button_height_max = 120
left_button_width_min = 50
left_button_width_pref = 80
left_button_width_max = 120
left_button_height_min = 50
left_button_height_pref = 80
left_button_height_max = 120
textbox_min = 0
textbox_pref = 700
textbox_max = 1000000


# number of buttons
num = 100

# window size
window_width = 600
window_height = 600
fixed_left = 200
fixed_right = 360
fixed_top = 200
fixed_bottom = 360
fixed_left = 191
fixed_right = 351
fixed_top = 277
fixed_bottom = 437
# window_width = randint(int((top_button_width_pref) * num_top/10), int((top_button_width_pref) * num_top/2))
# window_height = randint(int((top_button_height_pref) + (left_button_height_pref) * num_left/2), int((top_button_height_pref)*10 + (left_button_height_pref) * num_left/2))
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

    image = Image.open("../images/" + "CHI2020.png")
    image = image.resize((fixed_right - fixed_left, fixed_bottom - fixed_top), Image.ANTIALIAS)
    widgets.append([Label(root), "chi2020.png"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[-1][0].configure(image=photos[-1])

# defines the size of the window
if show_window:
    root.geometry(str(window_width) + "x" + str(window_height))


def main():
    
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
    # TODO: I should set a pointer pointing to specific flows
    if best_leaf == None:
        print("No Solution!")
        exit()
    result_index_upper = best_leaf.best_result_index_upper
    row_width_upper = best_leaf.best_row_width_upper
    row_height_upper = best_leaf.best_row_height_upper
    result_index_middle = best_leaf.best_result_index_middle
    row_width_middle = best_leaf.best_row_width_middle
    row_height_middle = best_leaf.best_row_height_middle
    result_index_lower = best_leaf.best_result_index_lower
    row_width_lower = best_leaf.best_row_width_lower
    row_height_lower = best_leaf.best_row_height_lower

    # place the widgets in upper area
    left = 0
    top = 0
    index = 0
    for i in range(len(result_index_upper)):
        for j in range(len(result_index_upper[i])):
            widget_width = row_width_upper[i][j]
            widget_height = row_height_upper[i]
            if index - 1 > len(widgets):
                exit()
            if show_window:
                widgets[index][0].place(x=left, y=top, width=widget_width, height=widget_height)
            left += widget_width
            index += 1
        left = 0
        top += widget_height

    for i in range(len(result_index_middle)):
        for j in range(len(result_index_middle[i][0])):
            widget_width = row_width_middle[i][0][j]
            widget_height = row_height_middle[i]
            if index - 1 > len(widgets):
                exit()
            if show_window:
                widgets[index][0].place(x=left, y=top, width=widget_width, height=widget_height)
            left += widget_width
            index += 1
        left = fixed_right
        for j in range(len(result_index_middle[i][1])):
            widget_width = row_width_middle[i][1][j]
            widget_height = row_height_middle[i]
            if index - 1 > len(widgets):
                exit()
            if show_window:
                widgets[index][0].place(x=left, y=top, width=widget_width, height=widget_height)
            left += widget_width
            index += 1
        left = 0
        top += widget_height

    for i in range(len(result_index_lower)):
        for j in range(len(result_index_lower[i])):
            widget_width = row_width_lower[i][j]
            widget_height = row_height_lower[i]
            if index - 1 > len(widgets):
                exit()
            if show_window:
                widgets[index][0].place(x=left, y=top, width=widget_width, height=widget_height)
            left += widget_width
            index += 1
        left = 0
        top += widget_height
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










