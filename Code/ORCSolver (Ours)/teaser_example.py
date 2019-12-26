from tkinter import *
from PIL import Image, ImageTk
from flow_solver import *
from orclayout_classes import *
import orclayout_classes
import time

# Formal Notation:
# Pivot(Column(HF1, Column(HF2, Pivot(Column(HF3)))

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
textbox_height = 80
button_width = 160
button_height = 80
CHI_width = 320
CHI_height = 240

# number of buttons in the toolbars
num_top = 8
window_width = 640
window_height = 480
window_width = 400
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

    image = Image.open("../images/" + "CHI2020.png")
    image = image.resize((CHI_width-15, CHI_height-15), Image.ANTIALIAS)
    widgets.append([Label(root), "CHI2020.png"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[-1][0].configure(image=photos[-1], bg="gray85")

    image = Image.open("../images/" + "CHI2019.png")
    image = image.resize((CHI_width-15, CHI_height-15), Image.ANTIALIAS)
    widgets.append([Label(root), "CHI2019.png"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[-1][0].configure(image=photos[-1], bg="gray85")

    image = Image.open("../images/" + "message_new.png")
    image = image.resize((button_width+5, button_height-20), Image.ANTIALIAS)
    widgets.append([Label(root), "message.png"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[-1][0].configure(image=photos[-1], bg="gray85")

    image = Image.open("../images/" + "blank.png")
    image = image.resize((textbox_width-180, textbox_height-20), Image.ANTIALIAS)
    widgets.append([Label(root), "blank.png"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[-1][0].configure(image=photos[-1], bg="gray85")

    image = Image.open("../images/" + "send_new.png")
    image = image.resize((button_width-60, button_height-37), Image.ANTIALIAS)
    widgets.append([Label(root), "send.png"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[-1][0].configure(image=photos[-1], bg="gray85")

    image = Image.open("../images/" + "email_new.png")
    image = image.resize((button_width-10, button_height-30), Image.ANTIALIAS)
    widgets.append([Label(root), "email.png"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[-1][0].configure(image=photos[-1], bg="gray85")

    image = Image.open("../images/" + "blank.png")
    image = image.resize((textbox_width-180, textbox_height-20), Image.ANTIALIAS)
    widgets.append([Label(root), "blank.png"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[-1][0].configure(image=photos[-1], bg="gray85")

    image = Image.open("../images/" + "clear_new.png")
    image = image.resize((button_width-60, button_height-37), Image.ANTIALIAS)
    widgets.append([Label(root), "clear.png"])
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
    top_widgets[0].set_optional()
    top_widgets[1].set_optional()
    top_widgets[2].set_optional()


    CHI2020 = ORCWidget("CHI2020", [CHI_width, CHI_width, CHI_width, \
                                    CHI_height, CHI_height, CHI_height])
    CHI2019 = ORCWidget("CHI2019", [CHI_width, CHI_width, CHI_width, \
                                    CHI_height, CHI_height, CHI_height])
    CHI2019.set_optional()
    CHI2019.set_weight(0.000001)

    message = ORCWidget("message", [button_width, button_width, button_width, \
                                    button_height, button_height, button_height])
    send = ORCWidget("send", [button_width, button_width, button_width, \
                                    button_height, button_height, button_height])
    email = ORCWidget("email", [button_width, button_width, button_width, \
                                    button_height, button_height, button_height])
    clear = ORCWidget("clear", [button_width, button_width, button_width, \
                                    button_height, button_height, button_height])

    blank1 = ORCWidget("blank1", [textbox_width-160, textbox_width, textbox_width, \
                                    textbox_height, textbox_height, textbox_height])
    blank2 = ORCWidget("blank1", [textbox_width-160, textbox_width, textbox_width, \
                                    textbox_height, textbox_height, textbox_height])

    pivot1 = Pivot("p1", None, window_width, window_height)
    column1 = ORCColumn("column1", pivot1)
    HF1 = HorizontalFlow("HF1", top_widgets, column1)
    column2 = ORCColumn("column2", HF1)
    HF2 = HorizontalFlow("HF2", [CHI2020, CHI2019], column2)
    pivot2 = Pivot("p2", HF2)
    column3 = ORCColumn("column3", pivot2)
    HF3 = HorizontalFlow("HF3", [message, blank1, send, email, blank2, clear], column3)
    
    pivot1.set_layout(column1)
    pivot2.set_layout(column3)
    column1.define_sublayouts([HF1, column2])
    column2.define_sublayouts([HF2, pivot2])
    column3.define_sublayouts([HF3])

    # Solve the system
    start = time.time()
    print(time.time() - start)
    pivot1.solve()

    # compute the time it takes
    print("Time: " + str(time.time() - start))
    if show_window:
        time_result.insert(0, str(time.time() - start))
    best_leaf, best_leaf_result, best_leaf_loss = pivot1.get_best()

    # TODO: I should set a pointer pointing to specific flows
    HF1_row_height = best_leaf.parent.parent.parent.parent.parent.best_row_height
    HF1_row_width = best_leaf.parent.parent.parent.parent.parent.best_row_width
    HF1_result_index = best_leaf.parent.parent.parent.parent.parent.best_result_index
    HF2_row_height = best_leaf.parent.parent.parent.best_row_height
    HF2_row_width = best_leaf.parent.parent.parent.best_row_width
    HF2_result_index = best_leaf.parent.parent.parent.best_result_index
    HF3_row_height = best_leaf.best_row_height
    HF3_row_width = best_leaf.best_row_width
    HF3_result_index = best_leaf.best_result_index

    # get the positions of sublayouts
    HF1_l = best_leaf_result["HF1_l"]
    HF1_r = best_leaf_result["HF1_r"]
    HF1_t = best_leaf_result["HF1_t"]
    HF1_b = best_leaf_result["HF1_b"]
    HF2_l = best_leaf_result["HF2_l"]
    HF2_r = best_leaf_result["HF2_r"]
    HF2_t = best_leaf_result["HF2_t"]
    HF2_b = best_leaf_result["HF2_b"]
    HF3_l = best_leaf_result["HF3_l"]
    HF3_r = best_leaf_result["HF3_r"]
    HF3_t = best_leaf_result["HF3_t"]
    HF3_b = best_leaf_result["HF3_b"]

    # place the widgets in the window
    left = HF1_l
    top = HF1_t
    for i in range(len(HF1_result_index)):
        if isinstance(HF1_row_width[i], list):
            for j in range(len(HF1_result_index[i])):     
                widget_width = HF1_row_width[i][j]
                widget_height = HF1_row_height[i]
                if show_window:
                    widgets[HF1_result_index[i][j]][0].place(x=left, y=top, width=widget_width, height=widget_height)
                left += widget_width
            left = HF1_l
            top += widget_height
        else:
            for j in range(len(HF1_result_index[i])):               
                widget_width = HF1_row_width[i]
                widget_height = HF1_row_height[i][j]
                if show_window:
                    widgets[HF1_result_index[i][j]][0].place(x=left, y=top, width=widget_width, height=widget_height)
                top += widget_height
            left += widget_width
            top = HF1_t

    # place the widgets in the window
    left = HF2_l
    top = HF2_t
    for i in range(len(HF2_result_index)):
        if isinstance(HF2_row_width[i], list):
            for j in range(len(HF2_result_index[i])):     
                widget_width = HF2_row_width[i][j]
                widget_height = HF2_row_height[i]
                if show_window:
                    widgets[HF2_result_index[i][j]+num_top][0].place(x=left, y=top, width=widget_width, height=widget_height)
                left += widget_width
            left = HF2_l
            top += widget_height
        else:
            for j in range(len(HF2_result_index[i])):               
                widget_width = HF2_row_width[i]
                widget_height = HF2_row_height[i][j]
                if show_window:
                    widgets[HF2_result_index[i][j]+num_top][0].place(x=left, y=top, width=widget_width, height=widget_height)
                top += widget_height
            left += widget_width
            top = HF2_t

    # place the widgets in the window
    left = HF3_l
    top = HF3_t
    for i in range(len(HF3_result_index)):
        if isinstance(HF3_row_width[i], list):
            for j in range(len(HF3_result_index[i])):     
                widget_width = HF3_row_width[i][j]
                widget_height = HF3_row_height[i]
                if show_window:
                    widgets[HF3_result_index[i][j]+num_top+2][0].place(x=left, y=top, width=widget_width, height=widget_height)
                left += widget_width
            left = HF3_l
            top += widget_height
        else:
            for j in range(len(HF3_result_index[i])):               
                widget_width = HF3_row_width[i]
                widget_height = HF3_row_height[i][j]
                if show_window:
                    widgets[HF3_result_index[i][j]+num_top+2][0].place(x=left, y=top, width=widget_width, height=widget_height)
                top += widget_height
            left += widget_width
            top = HF3_t


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








