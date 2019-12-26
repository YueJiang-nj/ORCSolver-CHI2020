from tkinter import *
from PIL import Image, ImageTk
from flow_solver import *
from orclayout_classes import *
import orclayout_classes
import time
from random import randint

# % large:
# % AAAAAA
# % C
# % 
# %
# % small:
# % AAA
# % AAA
# % C
# % 


# whether we want to show the window
show_window = 0

# widths and heights
top_button_width_min = 60
top_button_width_pref = 80
top_button_width_max = 100
top_button_height_min = 60
top_button_height_pref = 80
top_button_height_max = 100
left_button_width_min = 60
left_button_width_pref = 80
left_button_width_max = 100
left_button_height_min = 60
left_button_height_pref = 80
left_button_height_max = 100
textbox_min = 0
textbox_pref = 700
textbox_max = 1000000


# number of buttons in the toolbars
num_top = 10
# num_left = total - num_top
# num_top = 20
# num_left = 6

# window size
window_width = randint(10*num_top, 30*num_top)
window_height = 1000
# window_height = (top_button_height_pref) + (left_button_height_pref) * num_left
# window_width = int((top_button_width_pref) * num_top/4)
# window_height = int((top_button_height_pref)*4 + (left_button_height_pref) * num_left/2) 
# window_width = randint(int((top_button_width_pref) * num_top/10), int((top_button_width_pref) * num_top/2))
# window_height = randint(int((top_button_height_pref) + (left_button_height_pref) * num_left/2), int((top_button_height_pref)*10 + (left_button_height_pref) * num_left/2))

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

    # for j in range(num_top, num_top + num_left):
    #     if num_top <= 20: 
    #         image3 = Image.open("../images/" + str(j+1-num_top)*2 + ".png")
    #         widgets.append([Label(root), str(j+1-num_top)*2 + ".png"])
    #     else:
    #         image3 = Image.open("../images/" + "2" + ".png")
    #         widgets.append([Label(root), "2" + ".png"])
    #     image3 = image3.resize((top_button_width_pref, top_button_height_pref), Image.ANTIALIAS)
    #     photos.append(ImageTk.PhotoImage(image3))
    #     widgets[j][0].configure(image=photos[-1], bg="gray85")

    image3 = Image.open("../images/" + "text.jpg")
    widgets.append([Label(root), "text.jpg"])
    photos.append(ImageTk.PhotoImage(image3))
    widgets[num_top][0].configure(image=photos[-1], bg="gray85")

# defines the size of the window
if show_window:
    root.geometry(str(window_width) + "x" + str(window_height))

def main():
    
    # create all the widget objects
    top_widgets = []
    for i in range(num_top):
        top_widgets.append(ORCWidget("HF_" + str(i), \
                                      [top_button_width_min, top_button_width_pref, \
                                       top_button_width_max, top_button_height_min, \
                                       top_button_height_pref, top_button_height_max]))

    # create the flow layout pattern
    column = ORCColumn("column", None, window_width, window_height)
    horizonalflow = HorizontalFlow("HF", top_widgets, column, True)
    textbox = ORCWidget("textbox", [textbox_min, textbox_pref, textbox_max, \
                                    textbox_min, textbox_pref, textbox_max], horizonalflow)
    textbox.set_weight(0.00001)
    column.define_sublayouts([horizonalflow, textbox])

    # Solve the system
    start = time.time()
    column.solve()

    # compute the time it takes
    print("Time: " + str(time.time() - start))
    if show_window:
        time_result.insert(0, str(time.time() - start))
    best_leaf, best_leaf_result, best_leaf_loss = column.get_best()

    # TODO: I should set a pointer pointing to specific flows
    if best_leaf == None:
        print("No Solution!")
        exit()
    horizontalflow_row_height = best_leaf.parent.best_row_height
    horizontalflow_row_width = best_leaf.parent.best_row_width
    # horizontalflow_result_index = best_leaf.parent.best_result_index

    # get the positions of sublayouts
    HF_l = best_leaf_result["HF_l"]
    HF_r = best_leaf_result["HF_r"]
    HF_t = best_leaf_result["HF_t"]
    HF_b = best_leaf_result["HF_b"]
    textbox_l = best_leaf_result["textbox_l"]
    textbox_r = best_leaf_result["textbox_r"]
    textbox_t = best_leaf_result["textbox_t"]
    textbox_b = best_leaf_result["textbox_b"]

    # place the widgets in top toolbar in the window
    left = HF_l
    top = HF_t
    index = 0
    for i in range(len(horizontalflow_row_width)):
        for j in range(len(horizontalflow_row_width[i])):
            widget_width = horizontalflow_row_width[i][j]
            widget_height = horizontalflow_row_height[i]
            if show_window:
                widgets[index][0].place(x=left, y=top, width=widget_width, height=widget_height)
            left += widget_width
            index += 1
        left = HF_l
        top += widget_height

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
        print(window_width, window_height)
        root.geometry(str(window_width) + "x" + str(window_height))
        main()

# add mouse click functions
if show_window:
    root.bind("<Button-1>", mouse_click)
    # root.bind("<ButtonRelease-1>", mouse_release)
    root.bind("<B1-Motion>", mouse_release)

main()







