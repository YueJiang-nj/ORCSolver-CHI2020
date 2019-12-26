from z3 import *
from tkinter import *
from PIL import Image, ImageTk
import time
from random import randint


# whether we show the window
show_window = 1

# widths and heights
button_width_min = 50
button_width = 80
button_width_max = 120
button_height_min = 50
button_height = 80
button_height_max = 120

# window size
window_width = 600
window_height = 600

# number of buttons in the toolbars
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
        image = Image.open("../../images/" + "pineapple.jpg")
        widgets.append([Label(root), "pineapple.jpg"])
        image = image.resize((button_width, button_height), Image.ANTIALIAS)
        photos.append(ImageTk.PhotoImage(image))
        widgets[j][0].configure(image=photos[-1])

    image = Image.open("../../images/" + "chi2020.png")
    image = image.resize((fixed_right - fixed_left, fixed_bottom - fixed_top), Image.ANTIALIAS)
    widgets.append([Label(root), "chi2020.png"])
    photos.append(ImageTk.PhotoImage(image))
    widgets[-1][0].configure(image=photos[-1])

    # defines the size of the window
    root.geometry(str(window_width) + "x" + str(window_height))


def special_position_constraints(o, h, w, left, right, top, bottom, n, horizonal, b1, b2, b3, b4):

    # every widget must be in the window
    boundary = [And(Or(And(Or(left+button_width <= w[n][0]-0, top+button_height <= h[n][0]-0), w[0][0] == b1),
                       And(left+button_width > w[n][0]-0, top+button_height > h[n][0]-0, w[0][0] == w[n][1]+0)), h[0][0] == b3)]
    for i in range(n):
        boundary += [And (w[i][1] <= b2, h[i][1] <= b4)]

    # position constraints (widgets cannot be outside of the window and every 
    # widget can only be to the right of the previous widgest or at the 
    # beginning of the next row)
    position = []
    if horizonal:
        for i in range(1, n):
            orh = (h[i][0] == h[0][1] + 0)
            andh = (h[i][0] >= h[0][1] + 0)
            for j in range(1, i):
                orh = Or (orh, (h[i][0] == h[j][1]+0))
                andh = And (andh, (h[i][0] >= h[j][1]+0))
   
            position += [Or(
    						And(
    							Or(And(h[i-1][0] + button_height <= h[n][0]-0, w[i-1][1]+0+button_width <= right),
    							   h[i-1][0] >= h[n][1]+0,
    							   h[i-1][0] + button_height*2 <= h[n][0]-0*2,

    							   And(h[i-1][1]+0 >= h[n][1], w[i-1][1] > w[n][1],
    							       Or(w[i-1][1]+0 + button_width > right, 
    							          And(w[i-1][1]+0 + button_width > w[n][0], right-w[n][1]-0<button_width))
    							   )
    							 ),

    						     Or (And(w[i][0] == w[i-1][1]+0, h[i][0] == h[i-1][0]), And (w[i][0] == left, andh, orh))),
    		                And(
    		                	 Not(Or(And(h[i-1][0] + button_height <= h[n][0]-0, w[i-1][1]+0+button_width <= right),
    							   h[i-1][0] + button_height*2 <= h[n][0]-0*2,
    							   h[i-1][0] >= h[n][1]+0,
    							   And(h[i-1][1]+0 >= h[n][1], w[i-1][1] > w[n][1],
    							       Or(w[i-1][1]+0 + button_width > right, 
    							          And(w[i-1][1]+0 + button_width > w[n][0], right-w[n][1]-0<button_width))
    						
    							   	)
    							   )),
    		                	  Or (
    		                	  		And (Or (w[i-1][1]+0 + button_width +0 <= w[n][0],
    		                			     And(w[i-1][1] >= w[n][1], w[i-1][1]+0 + button_width <= right),
    		                			     And(w[i-1][1] <= w[n][1], w[n][1]+0 + button_width <= right)
    		                			     ),
    		                				
		    		                		h[i][0] == h[i-1][0],
		    		                		# And(andh, orh),
		    		                		Or(
		    		                		   And(
			    		                			Or(w[i-1][1]+0+button_width+0 <= w[n][0], w[i-1][1] > w[n][1]),
			    		                			w[i][0] == w[i-1][1]+0,
			    		                			),
		    		                		   And(
		    		                		   		Not(Or(w[i-1][1]+0+button_width+0 <= w[n][0], w[i-1][1] > w[n][1])),
		    		                				w[i][0] == w[n][1]+0, 
		    		                				)
		    		                		  ),
	    		                 		),
    		                			And (
    		                				Not(Or (w[i-1][1]+0 + button_width +0 <= w[n][0],
    		                			     And(w[i-1][1] >= w[n][1], w[i-1][1]+0 + button_width <= right),
    		                			     And(w[i-1][1] <= w[n][1], w[n][1]+0 + button_width <= right)),
    		                			 	),
	    		                			 And(andh, orh),
	    		                			 Or(And(left + button_width+0 <= w[n][0], w[i][0] == left),
	    		                			 	And(left + button_width+0 > w[n][0], w[i][0] == w[n][1]+0))
    		                		)

    		                	)
    		                )
						)]
            o.add_soft(w[i][0] == w[i-1][1]+ 0, max(150000-100*i, 100))
            o.add_soft(h[i][1] == h[i-1][1], 1000)

    o.add(position)

    # add boundary constraints
    boundary += [And (b1 == left, b2 == right, b3 == top, b4 == bottom)]
    o.add(boundary)


def main():

    # start time
    start = time.time()

    # creates Optimize object (for the layout, top toolbar, left toolbar)
    o = Optimize()

    # add variables for the widths and heights of widgets
    w = [[Int('w_%s_%s' % (i+1, j+1)) for j in range(2)] for i in range(num+1)]   # width
    h = [[Int("h_%s_%s" % (i+1, j+1)) for j in range(2)] for i in range(num+1)]   # height

    # add variables for boundaries to z3 
    b1 = Int('b1')    # left
    b2 = Int('b2')    # right
    b3 = Int('b3')    # top
    b4 = Int('b4')    # bottom

    special_position_constraints(o, h, w, 0, window_width, 0, window_height, num, True \
                                , b1, b2, b3, b4)

    # width constraints and height constraints
    constraints = []
    for i in range(num):
        constraints += [w[i][1] - w[i][0] == button_width, h[i][1] - h[i][0] == button_height]
    constraints += [w[num][0] == fixed_left, w[num][1] == fixed_right,
    			    h[num][0] == fixed_top, h[num][1] == fixed_bottom]
    o.add(constraints)

    # width constraints and height constraints
    width = []
    height = []

    # constraints for each button in the left toolbar
    for i in range(num):
        width += [w[i][1] - w[i][0] <= button_width_max]
        height += [h[i][1] - h[i][0] <= button_height_max]
        width += [w[i][1] - w[i][0] >= button_width_min]
        height += [h[i][1] - h[i][0] >= button_height_min]
        o.add_soft(w[i][1] - w[i][0] == button_width, 1000)
        o.add_soft(h[i][1] - h[i][0] == button_height, 1000)
    o.add(width + height)

    # gets optimized model
    if (o.check() == sat):
        m = o.model()
        
        # place all the widgets
        for i in range(num):
            widget_width = int(m[w[i][1]].as_string()) - int(m[w[i][0]].as_string())
            widget_height = int(m[h[i][1]].as_string()) - int(m[h[i][0]].as_string())
            if show_window:
                widgets[i][0].place(x=m[w[i][0]], y=m[h[i][0]], width=widget_width, height=widget_height)

        widget_width = int(m[w[num][1]].as_string()) - int(m[w[num][0]].as_string())
        widget_height = int(m[h[num][1]].as_string()) - int(m[h[num][0]].as_string())
        if show_window:
            widgets[-1][0].place(x=m[w[num][0]], y=m[h[num][0]], width=widget_width, height=widget_height)
    else:
        print("No solution!")

    # compute the time it takes
    print("Time: " + str(time.time() - start))
    time_result.insert(0, str(time.time() - start))

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







