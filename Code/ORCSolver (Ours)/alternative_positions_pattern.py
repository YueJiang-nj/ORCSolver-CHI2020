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
top_button_width_min = 80
top_button_width_pref = 80
top_button_width_max = 80
top_button_height_min = 80
top_button_height_pref = 80
top_button_height_max = 80
left_button_width_min = 80
left_button_width_pref = 80
left_button_width_max = 80
left_button_height_min = 80
left_button_height_pref = 80
left_button_height_max = 80
textbox_min = 0
textbox_pref = 700
textbox_max = 1000000
textbox_width = 200
textbox_height = 400


# number of buttons in the toolbars
num_top = 12

# window size
window_width = 360
window_height = 400


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

        widgets[j][0].configure(image=photos[-1], bg="gray85")

    image3 = Image.open("../images/" + "text.jpg")
    image3 = image3.resize((320, 320), Image.ANTIALIAS)
    widgets.append([Label(root), "text.png"])
    photos.append(ImageTk.PhotoImage(image3))
    widgets[-1][0].configure(image=photos[-1], bg="gray85")

    # image3 = Image.open("../images/" + "CHI2020.png")
    # image3 = image3.resize((320, 320), Image.ANTIALIAS)
    # widgets.append([Label(root), "CHI2020.png"])
    # photos.append(ImageTk.PhotoImage(image3))
    # widgets[-1][0].configure(image=photos[-1], bg="gray85")

# defines the size of the window
if show_window:
    root.geometry(str(window_width) + "x" + str(window_height))

def main():

    print(window_width, window_height)
    
    # create all the widget objects
    top_widgets = []
    left_widgets = []
    for i in range(num_top):
        top_widgets.append(ORCWidget("HF_" + str(i), \
                                      [top_button_width_min, top_button_width_pref, \
                                       top_button_width_max, top_button_height_min, \
                                       top_button_height_pref, top_button_height_max]))

    # create the flow layout pattern
    # the pattern is Column(HorizontalFlow, Row(VerticalFlow, TextBox))
    # create the tree for the flow layout pattern
    # pattern is the root node, Column is the child node of pattern,
    # HorizontalFlow is the child of Column, Row is the child of HorizontalFlow...
    pivot = Pivot("p", None, window_width, window_height)
    column = ORCColumn("column", pivot)
    horizonalflow = HorizontalFlow("HF", top_widgets, column)
    logo1 = ORCWidget("logo1", [textbox_width, textbox_width, textbox_width, \
                                    textbox_height, textbox_height, textbox_height], horizonalflow)
    logo1.set_weight(0.00001)
    pivot.set_layout(column)
    column.define_sublayouts([horizonalflow, logo1])

    # Solve the system
    start = time.time()
    pivot.solve()

    # compute the time it takes
    print("Time: " + str(time.time() - start))
    if show_window:
        time_result.insert(0, str(time.time() - start))
    best_leaf, best_leaf_result, best_leaf_loss = column.get_best()

    # TODO: I should set a pointer pointing to specific flows
    if best_leaf == None:
        print("No Solution!")
        exit()
    horizonalflow_row_height = best_leaf.parent.best_row_height
    horizonalflow_row_width = best_leaf.parent.best_row_width
    horizonalflow_result_index = best_leaf.parent.best_result_index

    # get the positions of sublayouts
    HF_l = best_leaf_result["HF_l"]
    HF_r = best_leaf_result["HF_r"]
    HF_t = best_leaf_result["HF_t"]
    HF_b = best_leaf_result["HF_b"]
    logo1_l = best_leaf_result["logo1_l"]
    logo1_r = best_leaf_result["logo1_r"]
    logo1_t = best_leaf_result["logo1_t"]
    logo1_b = best_leaf_result["logo1_b"]

    # place the widgets in top toolbar in the window
    left = HF_l
    top = HF_t
    for i in range(len(horizonalflow_result_index)):
        if isinstance(horizonalflow_row_width[i], list):
            for j in range(len(horizonalflow_result_index[i])):     
                widget_width = horizonalflow_row_width[i][j]
                widget_height = horizonalflow_row_height[i]
                if show_window:
                    widgets[horizonalflow_result_index[i][j]][0].place(x=left, y=top, width=widget_width, height=widget_height)
                left += widget_width
            left = HF_l
            top += widget_height
        else:
            for j in range(len(horizonalflow_result_index[i])):               
                widget_width = horizonalflow_row_width[i]
                widget_height = horizonalflow_row_height[i][j]
                if show_window:
                    widgets[horizonalflow_result_index[i][j]][0].place(x=left, y=top, width=widget_width, height=widget_height)
                top += widget_height
            left += widget_width
            top = HF_t
    if show_window:
        widgets[-1][0].place(x=logo1_l, y=logo1_t, width=logo1_r - logo1_l, height=logo1_b - logo1_t)

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
        print(window_width, window_height)
        root.geometry(str(window_width) + "x" + str(window_height))
        main()

# add mouse click functions
if show_window:
    root.bind("<Button-1>", mouse_click)
    root.bind("<ButtonRelease-1>", mouse_release)

main()








