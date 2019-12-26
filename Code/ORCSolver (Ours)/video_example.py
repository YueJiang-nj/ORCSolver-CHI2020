from tkinter import *
from PIL import Image, ImageTk
from flow_solver import *
from orclayout_classes import *
import orclayout_classes
import time


# Formal Notation:
# Pivot(Column(HF(optional widgets), Row(optional widgets), VF(TextBox, TextBox[optional])))


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
textbox_width = 320
textbox_height = 240


# number of buttons in the toolbars
num_top = 10
num_left = 6

# window size
window_width = 400
window_height = 640
window_width = 640
window_height = 240

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

    image = Image.open("../images/" + "CHI2020.png")
    image = image.resize((textbox_width, textbox_height), Image.ANTIALIAS)
    widgets.append([Label(root), "CHI2020.png"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[-1][0].configure(image=photos[-1], bg="gray85")

    image = Image.open("../images/" + "CHI2019.png")
    image = image.resize((textbox_width, textbox_height), Image.ANTIALIAS)
    widgets.append([Label(root), "CHI2019.png"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[-1][0].configure(image=photos[-1], bg="gray85")

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

        # set some widgets to be optional
        top_widgets[-1].set_optional()

    for i in range(num_top, num_top + num_left):
        left_widgets.append(ORCWidget("VF_" + str(i), \
                                      [left_button_width_min, left_button_width_pref, \
                                       left_button_width_max, left_button_height_min, \
                                       left_button_height_pref, left_button_height_max]))
        left_widgets[-1].set_optional()

    logo1 = ORCWidget("logo1", [textbox_width, textbox_width, textbox_width, \
                                    textbox_height, textbox_height, textbox_height])
    logo2 = ORCWidget("logo2", [textbox_width, textbox_width, textbox_width, \
                                    textbox_height, textbox_height, textbox_height])
    logo2.set_optional()
    logo2.set_weight(0.0001)

    # define the layout
    pivot = Pivot("p", None, window_width, window_height)
    column = ORCColumn("column", pivot)
    horizonalflow = HorizontalFlow("HF", top_widgets, column)
    row = ORCRow("row", horizonalflow)
    verticalflow = VerticalFlow("VF", left_widgets, row)
    verticallogo = VerticalFlow("VL", [logo1, logo2], verticalflow) 
    logo1.set_weight(0.00001)
    pivot.set_layout(column)
    logo2.set_weight(0.00001)
    column.define_sublayouts([horizonalflow, row])
    row.define_sublayouts([verticalflow, verticallogo])

    # Solve the system
    start = time.time()
    pivot.solve()

    # compute the time it takes
    print("Time: " + str(time.time() - start))
    if show_window:
        time_result.insert(0, str(time.time() - start))
    best_leaf, best_leaf_result, best_leaf_loss = pivot.get_best()

    # TODO: I should set a pointer pointing to specific flows
    horizonalflow_row_height = best_leaf.parent.parent.parent.best_row_height
    horizonalflow_row_width = best_leaf.parent.parent.parent.best_row_width
    horizonalflow_result_index = best_leaf.parent.parent.parent.best_result_index
    verticalflow_row_height = best_leaf.parent.best_row_height
    verticalflow_row_width = best_leaf.parent.best_row_width
    verticalflow_result_index = best_leaf.parent.best_result_index
    verticallogo_row_height = best_leaf.best_row_height
    verticallogo_row_width = best_leaf.best_row_width
    verticallogo_result_index = best_leaf.best_result_index

    # get the positions of sublayouts
    HF_l = best_leaf_result["HF_l"]
    HF_r = best_leaf_result["HF_r"]
    HF_t = best_leaf_result["HF_t"]
    HF_b = best_leaf_result["HF_b"]
    VF_l = best_leaf_result["VF_l"]
    VF_r = best_leaf_result["VF_r"]
    VF_t = best_leaf_result["VF_t"]
    VF_b = best_leaf_result["VF_b"]
    VL_l = best_leaf_result["VL_l"]
    VL_r = best_leaf_result["VL_r"]
    VL_t = best_leaf_result["VL_t"]
    VL_b = best_leaf_result["VL_b"]

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

    # place the widgets in top toolbar in the window
    left = VF_l
    top = VF_t
    for i in range(len(verticalflow_result_index)):
        if isinstance(verticalflow_row_width[i], list):
            for j in range(len(verticalflow_result_index[i])):     
                widget_width = verticalflow_row_width[i][j]
                widget_height = verticalflow_row_height[i]
                if show_window:
                    widgets[verticalflow_result_index[i][j]+num_top][0].place(x=left, y=top, width=widget_width, height=widget_height)
                left += widget_width
            left = VF_l
            top += widget_height
        else:
            for j in range(len(verticalflow_result_index[i])):               
                widget_width = verticalflow_row_width[i]
                widget_height = verticalflow_row_height[i][j]
                if show_window:
                    widgets[verticalflow_result_index[i][j]+num_top][0].place(x=left, y=top, width=widget_width, height=widget_height)
                top += widget_height
            left += widget_width
            top = VF_t

    # place the widgets in top toolbar in the window
    left = VL_l
    top = VL_t
    for i in range(len(verticallogo_result_index)):
        if isinstance(verticallogo_row_width[i], list):
            for j in range(len(verticallogo_result_index[i])):     
                widget_width = verticallogo_row_width[i][j]
                widget_height = verticallogo_row_height[i]
                if show_window:
                    widgets[verticallogo_result_index[i][j]+num_top+num_left][0].place(x=left, y=top, width=widget_width, height=widget_height)
                left += widget_width
            left = VL_l
            top += widget_height
        else:
            for j in range(len(verticallogo_result_index[i])):               
                widget_width = verticallogo_row_width[i]
                widget_height = verticallogo_row_height[i][j]
                if show_window:
                    print(verticallogo_result_index[i][j])
                    widgets[verticallogo_result_index[i][j]+num_top+num_left][0].place(x=left, y=top, width=widget_width, height=widget_height)
                top += widget_height
            left += widget_width
            top = VL_t

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
window_width = 80 * 10








