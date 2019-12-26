from math import *
from node import *
import cvxpy as cvx


# given the width of the sublayout and the min/pref/max widths of all the widgets,
# calculate the min/pref/max number of rows
def get_num_rows(sublayout_width, w_list):

    # the total number of widgets in the sublayout
    num = len(w_list)

    # the current occupied width in the row
    row_length = 0
    
    # total number of rows
    num_row = 1
    
    # use pref widths to fill rows
    for i in range(num):
        row_length += w_list[i]
        
        # if there is enough space for this widget with its pref width,
        # then put this widget to this row
        if row_length <= sublayout_width:
            pass
        
        # if not enough space, then put it to the next row.
        else:
            row_length = w_list[i]
            num_row += 1

    return num_row


# given the height of the sublayout and the min/pref/max heights of all the widgets,
# calculate the min/pref/max number of columns
def get_num_cols(sublayout_height, h_list):
    
    return get_num_rows(sublayout_height, h_list)


# horizontal flow
def horizontal_flow(sublayout_width, sublayout_height, num_widgets, \
                    width_min_list, width_pref_list, width_max_list, \
                    height_min_list, height_pref_list, height_max_list):

    # get the best result node
    result = flow(sublayout_width, sublayout_height, num_widgets, \
                width_min_list, width_pref_list, width_max_list, \
                height_min_list, height_pref_list, height_max_list, {})[0]

    # get the loss of the flow
    flow_loss = result.get_loss()

    # get the heights of all the rows in the flow
    row_height = result.get_height_list()

    # get the index resulta and widths of the widgets in the flow
    row_width = []
    row_width.insert(0, result.get_width_list())
    while(result.parent):
        result = result.get_parent()
        row_width.insert(0, result.get_width_list())

    return row_width, row_height, flow_loss


# vertical flow
def vertical_flow(sublayout_width, sublayout_height, num_widgets, \
                    width_min_list, width_pref_list, width_max_list, \
                    height_min_list, height_pref_list, height_max_list):

    return horizontal_flow(sublayout_height, sublayout_width, num_widgets, \
                height_min_list, height_pref_list, height_max_list, \
                width_min_list, width_pref_list, width_max_list)


# the definition of loss function
def loss_fn(x):
    return If(x > 0, x, -x)


# calculate the loss function result
def loss_fn_value(x):
    if (x >= 0):
        return x
    else:
        return -x


# calculate the loss of the current node
def calculate_loss(sublayout_width, remaining_height, min_w, pref_w, max_w, min_h, pref_h, max_h):
    
    # number of widgets
    num_widgets = len(min_w)

    # initialize constraints and objectives
    constraints = []
    objectives = []

    # the width of each widget should be less than max width
    # and greater than min width, and the height of each widget
    # should be closer to the row height
    h = cvx.Variable()
    constraints += [h >= 1, h <= remaining_height]
    loss = 0
    w = []
    for i in range(num_widgets):
        w.append(cvx.Variable())

        # we have panelty on the distance between our resulting sizes
        # and preferred sizes
        # minimize the distance between result sizes and preferred sizes
        constraints = [w[i] >= min_w[i], w[i] <= max_w[i]]
        objectives += [cvx.square(w[i] - pref_w[i]) + cvx.square(h - pref_h[i])]

    # the right boundary of the rightmost widget should be the same as
    # the right boundary of the sublayout
    constraints += [sum(w) == sublayout_width]

    # get the solve model
    # solve the constraint system to get the width and height of the flow sublayout
    obj = cvx.Minimize(cvx.sum(objectives))
    optimizer = cvx.Problem(obj, constraints)
    optimizer.solve()

    # loss is the sum of the distance between preferred size and
    # result size for each widget
    # we can get it from objective function
    loss = optimizer.value

    # get the width results
    width_list = []

    # get the width result of all the widgets
    for i in range(num_widgets):
        width_list.append(w[i].value)

    return loss, width_list, h.value


# fixed right boundary and flexible bottom boundary
# return best result node or None if no solution
# priority_queue is empty if it is the first time flowing in this sublayout
# priority queue contains the remaining possible solution for the sublayout
# if it is not the first time flowing in this sublayout
def flow(sublayout_width, sublayout_height, num, min_w, pref_w, max_w, min_h, pref_h, max_h, priority_queue):
    
    # initialization
    priority_queue = {}
    index = 0
    curr_node = None
    remaining_height = sublayout_height
    
    # get the best result in the priority queue
    if priority_queue == {}:
        best_result = Node(None, 0, [], 0, [], 0, False)
    else:

        # sort to get the node with best result
        priority_order = sorted(priority_queue, key=lambda x:priority_queue[x])

        # get the best reault node
        best_result = priority_order.pop(0)
        del priority_queue[best_result]
        curr_node = best_result
        
        # compute remaining height
        remaining_height = sublayout_height - sum(best_result.get_height_list())
        
        # store the current index
        index = best_result.get_start_index() + len(best_result.get_width_list())
    
    # stop when the best result reaches the last widget
    while not best_result.get_finish():
        
        start_index = index  # [start_index, end_index)
        
        # compute the maximum end index
        curr_width_min = 0
        for i in range(start_index, num):
            curr_width_min += min_w[i]
            if curr_width_min > sublayout_width:
                end_index_max = i   # when widths are minimized, index is maxmimum
                break
            elif i == num - 1:
                end_index_max = num
    
        # compute the minimum end index
        curr_width_max = 0
        for i in range(start_index, num):
            curr_width_max += max_w[i]
            if curr_width_max > sublayout_width:
                end_index_min = i   # when widths are maximized, index is minimimum
                break
            elif i == num - 1:
                end_index_min = num
    
        # solve for all the possible end index
        for end_index in range(end_index_min, end_index_max + 1):
            
            # no solution
            if end_index == start_index:
                continue
            
            # calculate the loss, width of each widget and the height of the row
            loss, width_list, height = calculate_loss(sublayout_width, remaining_height,\
                                                      min_w[start_index:end_index], \
                                                      pref_w[start_index:end_index], \
                                                      max_w[start_index:end_index], \
                                                      min_h[start_index:end_index], \
                                                      pref_h[start_index:end_index], \
                                                      max_h[start_index:end_index])
                
            # if no solution, then continue to next loop
            if loss == None:
                continue

            # check whether we have reached the last widget
            finish = (end_index == num)

            # create the root node
            if curr_node == None:
                node = Node(None, loss, width_list, sublayout_height - remaining_height, [height], start_index, finish)
                priority_queue[node] = loss
            
            # create the child node
            else:
                node_loss = loss + curr_node.get_loss()
                height_list = curr_node.get_height_list() + [height]
                node = Node(curr_node, node_loss, width_list, sublayout_height - remaining_height, height_list, start_index, finish)
                priority_queue[node] = node_loss
    
        # sort the priority queue
        priority_order = sorted(priority_queue, key=lambda x:priority_queue[x])
        
        # if no solution can be found, return None
        if priority_order == []:
            return None
        
        # get the best reault node
        best_result = priority_order.pop(0)
        del priority_queue[best_result]
        curr_node = best_result
        
        # compute remaining height
        remaining_height = sublayout_height - sum(best_result.get_height_list())
        
        # store the current index
        index = best_result.get_start_index() + len(best_result.get_width_list())
            
    return best_result, priority_queue


# get the widget list which should be put in the horizontal flow and put other widgets
# to the connected flow
def horizontal_flow_connected(sublayout_width, sublayout_height, target_num_row, pref_w_list, pref_h_list):
    
    # the total number of widgets in the sublayout
    num = len(pref_w_list)
    
    # the current occupied width in the row
    row_length = 0
    
    # total number of rows
    num_row = 1
    
    # use pref widths to fill rows
    for i in range(num):
        row_length += pref_w_list[i]
        
        # if there is enough space for this widget with its pref width,
        # then put this widget to this row
        if row_length <= sublayout_width:
            pass
        
        # if not enough space, then put it to the next row.
        else:
            row_length = pref_w_list[i]
            num_row += 1
        
        # if we have filled all the rows, we know how many widgets should be
        # placed in this flow sublayout
        if num_row == target_num_row + 1:
            
            # widgets[:i] should be in this flow, and widgets[i:] should be in
            # the connected flow
            return i

    # if there are not enough widgets to fill in the flow, we return the last one
    return i

# get all the factors of the number
def get_factors(n):
    lst = []
    i = 1
    while i <= sqrt(n):
        if n % i == 0:
            lst.append(i)
        i += 1
    return lst


# get the widget list which should be put in the vertical flow and put other widgets
# to the connected flow
def vertical_flow_connected(sublayout_width, sublayout_height, target_num_col, pref_w_list, pref_h_list):

    return horizontal_flow_connected(sublayout_height, sublayout_width, target_num_col, pref_h_list, pref_w_list)


