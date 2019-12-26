from math import *


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

# given the width of the sublayout and the min/pref/max widths of all the widgets,
# calculate the min/pref/max number of rows
# this function is just for flowing around the fixed area
def get_num_rows_for_upper_area(sublayout_width, sublayout_height, pref_w_list, pref_h_list):
    
    ############### Upper Area ###############
    # the total number of widgets in the sublayout
    num = len(pref_w_list)
    
    # the current occupied width in the row
    row_length = 0
    
    # total pref number of rows for the above area
    pref_num_row = 1
    
    # store the sum of the widget heights in the row
    row_height = 0
    sum_row_height = 0
    num_widget_in_row = 0
    
    # use pref widths to fill rows
    for i in range(num):
        row_length += pref_w_list[i]
        row_height += pref_h_list[i]
        num_widget_in_row += 1
        
        # if there is enough space for this widget with its pref width,
        # then put this widget to this row
        if row_length <= sublayout_width:
            pass
        
        # if not enough space, then put it to the next row.
        else:
            sum_row_height += (row_height - pref_h_list[i]) / (num_widget_in_row - 1)
            if sum_row_height >= sublayout_height:
                break
            row_height = pref_h_list[i]
            row_length = pref_w_list[i]
            num_widget_in_row = 1
            pref_num_row += 1

    return pref_num_row


# given the width of the sublayout and the min/pref/max widths of all the widgets,
# calculate the min/pref/max number of rows
# this function is just for flowing around the fixed area
# left_width is the width to the left of the fixed area
# right_width is the width to the right of the fixed area
def get_num_rows_for_middle_area(sublayout_left_width, sublayout_right_width, sublayout_height, pref_w_list, pref_h_list):
    
    ############### Middle Area ###############
    # the total number of widgets in the sublayout
    num = len(pref_w_list)
    
    # the current occupied width in the row
    row_length = 0
    
    # total pref number of rows for the above area
    pref_num_row = 1
    
    # store the sum of the widget heights in the row
    row_height = 0
    sum_row_height = 0
    num_widget_in_row = 0
    
    # use pref widths to fill rows
    position = "left"
    for i in range(num):
        row_length += pref_w_list[i]
        row_height += pref_h_list[i]
        num_widget_in_row += 1
        
        # case 1: left area
        if position == "left":
        
            # if there is enough space in the left for this widget with its pref width,
            # then put this widget in the left area
            if row_length <= sublayout_left_width:
                pass
            
            # if not enough space in the left area, then put it to the right.
            else:
                position = "right"
                row_length = pref_w_list[i]
        
        # case 2: right area
        if position == "right":
            
            # if there is enough space in the right for this widget with its pref width,
            # then put this widget in the right area
            if row_length <= sublayout_left_width:
                pass
        
            # if not enough space in the right area, then put it to the next row.
            else:
                if num_widget_in_row == 1:
                    break
                sum_row_height += (row_height - pref_h_list[i]) / (num_widget_in_row - 1)
                if sum_row_height >= sublayout_height:
                    break
                position = "left"
                row_height = pref_h_list[i]
                row_length = pref_w_list[i]
                num_widget_in_row = 1
                pref_num_row += 1

    return pref_num_row


# given the height of the sublayout and the min/pref/max heights of all the widgets,
# calculate the min/pref/max number of columns
def get_num_cols(sublayout_height, h_list):
    
    return get_num_rows(sublayout_height, h_list)


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



# get the widget list which should be put in the vertical flow and put other widgets
# to the connected flow
def vertical_flow_connected(sublayout_width, sublayout_height, target_num_col, pref_w_list, pref_h_list):

    return horizontal_flow_connected(sublayout_height, sublayout_width, target_num_col, pref_h_list, pref_w_list)




# get the widget list which should be put in the horizontal flow and put other widgets
# to the connected flow
# this function is just for flowing around a fixed area
def horizontal_flow_connected_for_middle_area(sublayout_left_width, sublayout_right_width, sublayout_height, \
                                              target_num_row, pref_w_list, pref_h_list):
    
    # the total number of widgets in the sublayout
    num = len(pref_w_list)
    
    # the current occupied width in the row
    row_length = 0
    
    # total number of rows
    num_row = 1
    
    # use pref widths to fill rows
    position = "left"
    for i in range(num):
        row_length += pref_w_list[i]
        
        # case 1: left area
        if position == "left":
            
            # if there is enough space for this widget with its pref width,
            # then put this widget to this row
            if row_length <= sublayout_left_width:
                pass
            
            # if not enough space, then put it to the next row.
            else:
                position = "right"
                row_length = pref_w_list[i]
    
        # case 2: right area
        if position == "right":
            
            # if there is enough space for this widget with its pref width,
            # then put this widget to this row
            if row_length <= sublayout_right_width:
                pass
                
            # if not enough space, then put it to the next row.
            else:
                row_length = pref_w_list[i]
                num_row += 1
                position = "left"

        # if we have filled all the rows, we know how many widgets should be
        # placed in this flow sublayout
        if num_row == target_num_row + 1:
            
            # widgets[:i] should be in this flow, and widgets[i:] should be in
            # the connected flow
            return i

    # if there is not enough widgets, then return the last index
    return i


# compute the loss of the widgets (the squared distance between the preferred sizes of widgets
# and the resulting sizes of widgets)
# this function is only for flowing around the fixed area
def compute_loss(result_index, row_width, row_height, pref_w_list, pref_h_list):
    
    loss = 0
    
    # the loss is the sum of the squared distance between the preferred sizes of widgets
    # and the resulting sizes of widgets
    for i in range(len(result_index)):
        for j in range(len(result_index[i])):
            loss += (row_width[i][j] - pref_w_list[result_index[i][j]]) ** 2 \
                + (row_height[i] - pref_h_list[result_index[i][j]]) ** 2

    return loss

# compute the loss of the widgets (the squared distance between the preferred sizes of widgets
# and the resulting sizes of widgets)
# this function is only for flowing around the fixed area
def compute_loss_for_middle_area(result_index, row_width, row_height, pref_w_list, pref_h_list):
    
    loss = 0
    
    # the loss is the sum of the squared distance between the preferred sizes of widgets
    # and the resulting sizes of widgets
    for i in range(len(result_index)):
        for j in range(len(result_index[i])):
            for k in range(len(result_index[i][j])):
                loss += (row_width[i][j][k] - pref_w_list[result_index[i][j][k]]) ** 2 \
                    + (row_height[i] - pref_h_list[result_index[i][j][k]]) ** 2

    return loss


# compute the additional loss for the part larger than max sizes or smaller than min sizes
# add_index is the index we need to add to the result_index since result_index 
# starts at 0
def compute_additional_loss(result_index, row_width, row_height, widget_list, \
                            max_w_list, min_w_list, max_h_list, min_h_list, add_index=0):

    # store the additional loss
    loss = 0

    # loop over all the widgets in the flow
    for i in range(len(result_index)):
        for j in range(len(result_index[i])):
            index = result_index[i][j] + add_index

            # larger than the max sizes
            if row_width[i][j] > max_w_list[index]:
                loss += 10 * (row_width[i][j] \
                                      - max_w_list[index]) ** 2
            elif row_width[i][j] < min_w_list[index]:
                loss += 10 * (row_width[i][j] \
                                      - min_w_list[index]) ** 2

            # smaller than the min sizes
            if row_height[i] > max_h_list[index]:
                loss += 10 * (row_height[i] \
                                      - max_h_list[index]) ** 2
            elif row_height[i] < min_h_list[index]:
                loss += 10 * (row_height[i] \
                                      - min_h_list[index]) ** 2
    return loss


# compute the additional loss for the part larger than max sizes or smaller than min sizes
def compute_additional_loss_for_middle_area(result_index, row_width, row_height, widget_list, \
                                            max_w_list, min_w_list, max_h_list, min_h_list, add_index):

    # store the additional loss
    loss = 0

    # loop over all the widgets in the flow
    for i in range(len(result_index)):
        for j in range(len(result_index[i])):
            for k in range(len(result_index[i][j])):
                index = result_index[i][j][k] + add_index

                # larger than the max sizes
                if row_width[i][j][k] > max_w_list[index]:
                    loss += 10 * widget_list[index].weight * (row_width[i][j][k] \
                                          - max_w_list[index]) ** 2
                elif row_width[i][j][k] < min_w_list[index]:
                    loss += 10 * widget_list[index].weight * (row_width[i][j][k] \
                                          - min_w_list[index]) ** 2

                # smaller than the min sizes
                if row_height[i] > max_h_list[index]:
                    loss += 10 * widget_list[index].weight * (row_height[i] \
                                          - max_h_list[index]) ** 2
                elif row_height[i] < min_h_list[index]:
                    loss += 10 * widget_list[index].weight * (row_height[i] \
                                          - min_h_list[index]) ** 2
    return loss



# fixed right boundary and flexible bottom boundary
# given the width and height of the sublayout, the pref widths and heights,
# the number of rows we want to put in this sublayout
# return indices of widgets in each row (list of lists),
# widget width list (list of lists), widget height list (list)
def horizontal_flow_for_middle_area(sublayout_left_width, sublayout_right_width, sublayout_height, num_row, \
                                    pref_w_list, pref_h_list):
    
    # the total number of widgets in the sublayout
    num = len(pref_w_list)
    
    # store the indices of widgets in each row
    result_index = []
    
    # store the widths and heights of the widgets
    # width for each widget and height for each row
    row_width = []
    row_height = []
    
    # we put all the widgets in this sublayout
    i = 0
    for r in range(num_row):
        row_width.append([])
        row_width[r].append([])
        row_width[r].append([])
        result_index.append([])
        
        # get the remaining available width
        remaining_total_available_width = (num_row - r) * (sublayout_left_width + sublayout_right_width)
        
        # get how much each widget will likely need more or less than its preferred size
        overall_delta = remaining_total_available_width - sum(pref_w_list[i:])

        # the current occupied width in the row
        row_length = 0
        
        # fill this row
        start_index = i
        position = "left"
        result_index[r].append([])
        while i < num:
            
            delta = overall_delta / (num - start_index)
            row_length += pref_w_list[i] + delta
            
            # case 1: left area
            if position == "left":
                if row_length <= sublayout_left_width:
                    result_index[-1][-1].append(i)
                    i += 1
            
                # once we go beyond the width of the row, we keep this last widget only if
                # adding it can make us become more closer to the width of the row
                else:
                    if row_length - sublayout_left_width < sublayout_left_width \
                        - (row_length - pref_w_list[i] - delta):
                        result_index[-1][-1].append(i)
                        i += 1
                    else:
                        # move to the right area
                        position = "right"
                        row_length = pref_w_list[i] + delta
                        result_index[r].append([])

            # case 2: right area
            if position == "right":
                if row_length <= sublayout_right_width:
                    result_index[-1][-1].append(i)
                    i += 1
                
                # once we go beyond the width of the row, we keep this last widget only if
                # adding it can make us become more closer to the width of the row
                else:
                    if row_length - sublayout_right_width < sublayout_right_width \
                        - (row_length - pref_w_list[i] - delta):
                        result_index[-1][-1].append(i)
                        i += 1
                    else:
                        # put it to the next row
                        break
    
        end_index = i

        if len(result_index[r]) == 1:
            result_index[r].append([])
        
        # no solution
        if end_index == start_index:
            return None

        # get precisely how much each widget will likely need more or less than its preferred size
        sum_row_width = 0
        sum_row_height = 0
        for index in result_index[-1][0]:
            sum_row_width += pref_w_list[index]
            sum_row_height += pref_h_list[index]
        if len(result_index[-1][0]) != 0:
            row_left_delta = (sublayout_left_width - sum_row_width) / len(result_index[-1][0])
        
        # get the preferred width of each widget in this row
        for index in result_index[-1][0]:
            row_width[-1][0].append(pref_w_list[index] + row_left_delta)

        # get precisely how much each widget will likely need more or less than its preferred size
        sum_row_width = 0
        for index in result_index[-1][1]:
            sum_row_width += pref_w_list[index]
            sum_row_height += pref_h_list[index]
        if len(result_index[-1][1]) != 0:
            row_right_delta = (sublayout_right_width - sum_row_width) / len(result_index[-1][1])

        # get the preferred height of this row
        row_height.append(sum_row_height / (len(result_index[-1][0]) + len(result_index[-1][1])))
        
        # get the preferred width of each widget in this row
        for index in result_index[-1][1]:
            row_width[-1][1].append(pref_w_list[index] + row_right_delta)
    
    # adjust row heights
    delta = (sum(row_height) - sublayout_height) / num_row
    row_height = [x - delta for x in row_height]
    
    return result_index, row_width, row_height


# fixed right boundary and flexible bottom boundary
# given the width and height of the sublayout, the pref widths and heights,
# the number of rows we want to put in this sublayout
# return indices of widgets in each row (list of lists),
# widget width list (list of lists), widget height list (list)
def horizontal_flow(sublayout_width, sublayout_height, num_row, pref_w_list, pref_h_list, \
                    optional_index_weight_dict, fixed_boundary):

    # the total number of widgets in the sublayout
    num = len(pref_w_list)
    
    # store the indices of widgets in each row
    result_index = []
    
    # store the widths and heights of the widgets
    # width for each widget and height for each row
    row_width = []
    row_height = []

    # we put all the widgets in this sublayout
    i = 0
    removed_index_weight_dict = {}
    for r in range(num_row):
        row_width.append([])
        result_index.append([])
        
        # get the remaining available width
        remaining_total_available_width = (num_row - r) * sublayout_width
    
        # get how much each widget will likely need more or less than its preferred size
        overall_delta = remaining_total_available_width - sum(pref_w_list[i:])
        
        # compute the loss as the sum of the overall delta and the sum of removed weights
        loss = abs(overall_delta) + sum(removed_index_weight_dict.values())
        
        # remove optional widgets
        if (overall_delta <= 0):
            while (overall_delta <= 0 and optional_index_weight_dict != {}):
                flag = False
                
                for index, weight in optional_index_weight_dict.items():
                    if index >= i:
                        removed_index_weight_dict[index] = weight
                        flag = True
                        
                        # get how much each widget will likely need more
                        # or less than its preferred size
                        prev_overall_delta = overall_delta
                        overall_delta += pref_w_list[index]
                        break
        
                # compute the loss as the sum of the overall delta
                # and the sum of removed weights
                if loss > overall_delta + sum(removed_index_weight_dict.values()):
                    loss = abs(overall_delta) + sum(removed_index_weight_dict.values())
                    del optional_index_weight_dict[index]
                else:
                    if flag:
                        del removed_index_weight_dict[index]
                        overall_delta = prev_overall_delta
                    break
    
        # add back optional widgets
        else:
            while (overall_delta > 0 and removed_index_weight_dict != {}):
                for index, weight in removed_index_weight_dict.items():
                    if index >= i:
                        optional_index_weight_dict[index] = weight
                        
                        # get how much each widget will likely need more
                        # or less than its preferred size
                        overall_delta = remaining_total_available_width - sum(pref_w_list)
                        break
            
                # compute the loss as the sum of the overall delta
                # and the sum of removed weights
                if loss > overall_delta + sum(removed_index_weight_dict.values()):
                    loss = overall_delta + sum(removed_index_weight_dict.values())
                    del optional_index_weight_dict[index]
                else:
                    del removed_index_weight_dict[index]
                    break


        # the current occupied width in the row
        row_length = 0

        # fill this row
        start_index = i
        while i < num:
            
            # if the widget is not removed, then place it in the row
            if i not in removed_index_weight_dict.keys():
                delta = overall_delta / (num - len(removed_index_weight_dict) - start_index)
                row_length += pref_w_list[i] + delta
                if row_length <= sublayout_width:
                    result_index[-1].append(i)
                    i += 1

                # once we go beyond the width of the row, we keep this last widget only if
                # adding it can make us become more closer to the width of the row
                else:
                    if row_length - sublayout_width < sublayout_width \
                        - (row_length - pref_w_list[i] - delta):
                        result_index[-1].append(i)
                        i += 1
                    else:
                        # put it to the next row
                        break
            else:
                i += 1
        end_index = i
        
        # no solution
        if end_index == start_index:
            return None
    
        # get precisely how much each widget will likely need more or less than its preferred size
        sum_row_width = 0
        sum_row_height = 0
        for index in result_index[-1]:
            sum_row_width += pref_w_list[index]
            sum_row_height += pref_h_list[index]
        row_delta = (sublayout_width - sum_row_width) / len(result_index[-1])
        
        # get the preferred height of this row
        row_height.append(sum_row_height / len(result_index[-1]))

        # get the preferred width of each widget in this row
        for index in result_index[-1]:
            row_width[-1].append(pref_w_list[index] + row_delta)
    
    # adjust row heights
    if sum(row_height) > sublayout_height or fixed_boundary:
        delta = (sum(row_height) - sublayout_height) / num_row
        row_height = [x - delta for x in row_height]

    if end_index != len(pref_w_list):
        return None

    return result_index, row_width, row_height, sum(removed_index_weight_dict.values())


# fixed bottom boundary and flexible right boundary
# given the width and height of the sublayout, the pref widths and heights,
# the number of columns we want to put in this sublayout
# return indices of widgets in each column (list of lists),
# widget height list (list of lists), widget width list (list)
def vertical_flow(sublayout_width, sublayout_height, num_col, pref_w_list, pref_h_list, optional_index_weight_dict, fixed_boundary):
    
    return horizontal_flow(sublayout_height, sublayout_width, num_col, pref_h_list, pref_w_list, optional_index_weight_dict, fixed_boundary)


# get all the factors of the number
def get_factors(n):
    lst = []
    i = 1
    while i <= sqrt(n):
        if n % i == 0:
            lst.append(i)
        i += 1
    return lst


# flow around a fixed area
# Note that the resulting indices are all starting from 0
def flow_around_fixed_area(sublayout_width, sublayout_height, \
                           fixed_top, fixed_bottom, fixed_left, fixed_right, \
                           pref_w_list, pref_h_list):
    
    # store the best loss
    best_loss = None

    ############### Upper Area ###############
    # compute the preferred number of rows in the upper area
    pref_num_row_upper = get_num_rows_for_upper_area(sublayout_width, fixed_top, pref_w_list, pref_h_list)

    # get the max number of rows
    max_num_row_upper = get_num_rows(sublayout_width, pref_w_list)

    # get all possible number of rows for the above area
    less_rows_upper = []
    for i in range(pref_num_row_upper, 0, -1):
        less_rows_upper.append(i)
    more_rows_upper = []
    for i in range(pref_num_row_upper+1, max_num_row_upper+1):
        more_rows_upper.append(i)

    # check all the possible number of rows which are less than the preferred number
    for num_row_upper in less_rows_upper:
        
        # compute the result for the upper area of flowing around the fixed area
        end_index_upper = horizontal_flow_connected(sublayout_width, fixed_top, num_row_upper, \
                                              pref_w_list, pref_h_list)
        result_index_upper, row_width_upper, row_height_upper, _ = horizontal_flow(sublayout_width, \
                                                            fixed_top, num_row_upper, pref_w_list[:end_index_upper], \
                                                            pref_h_list[:end_index_upper], {}, True)
        loss_upper = compute_loss(result_index_upper, row_width_upper, row_height_upper, \
                                  pref_w_list[:end_index_upper], pref_h_list[:end_index_upper])
                                  
        # if the loss is already too large, then we skip this loop
        if best_loss != None and best_loss <= loss_upper:
            break

        ############### Middle Area ###############
        # compute the preferred number of rows in the middle area
        pref_num_row_middle = get_num_rows_for_middle_area(fixed_left, \
                                                           sublayout_width - fixed_right, \
                                                           fixed_bottom - fixed_top, \
                                                           pref_w_list[end_index_upper:], \
                                                           pref_h_list[end_index_upper:])

        # get the max number of rows
        max_num_row_middle = get_num_rows_for_middle_area(fixed_left, \
                                                         sublayout_width - fixed_right, \
                                                         sublayout_height, \
                                                         pref_w_list[end_index_upper:], \
                                                         pref_h_list[end_index_upper:])

        # get all possible number of rows for the above area
        less_rows_middle = []
        for i in range(pref_num_row_middle, 0, -1):
            less_rows_middle.append(i)
        more_rows_middle = []
        for i in range(pref_num_row_middle+1, max_num_row_middle+1):
            more_rows_middle.append(i)

        # check all the possible number of rows which are less than the preferred number
        for num_row_middle in less_rows_middle:

            # get the last index of the widget to flow in the middle area
            end_index_middle = horizontal_flow_connected_for_middle_area(fixed_left, sublayout_width - fixed_right, \
                                                      fixed_bottom - fixed_top, num_row_middle, \
                                                      pref_w_list[end_index_upper:], pref_h_list[end_index_upper:])

            # make end_index_middle be a global index
            end_index_middle += end_index_upper

            # flow in the middle area
            result = horizontal_flow_for_middle_area(fixed_left, \
                                                   sublayout_width - fixed_right, \
                                                   fixed_bottom - fixed_top, \
                                                   num_row_middle, \
                                        pref_w_list[end_index_upper:end_index_middle], \
                                        pref_h_list[end_index_upper:end_index_middle])

            # if we can put some widgets in this area, then compute the loss as usual
            if result != None:
                result_index_middle, row_width_middle, row_height_middle = result
            
                # compute the loss of the middle area
                loss_middle = compute_loss_for_middle_area(result_index_middle, row_width_middle, row_height_middle, \
                                                           pref_w_list[end_index_upper:end_index_middle], \
                                                           pref_h_list[end_index_upper:end_index_middle])

            # if there is no widgets which can fit in this area, then the loss equals
            # the area of the available space
            else:
                result_index_middle = []
                row_width_middle = [] 
                row_height_middle = []
                loss_middle = ((fixed_bottom - fixed_top) * (fixed_left + sublayout_width - fixed_right)) ** 2
         
            # if the loss is already too large, then we skip this branch
            if best_loss != None and best_loss <= loss_upper + loss_middle:
                break

            ############### Lower Area ###############
            # get the pref number of rows
            pref_num_row_lower = get_num_rows(sublayout_width, pref_w_list[end_index_middle:])

            # get all possible number of rows for the above area
            less_rows_lower = []
            for i in range(pref_num_row_lower, 0, -1):
                less_rows_lower.append(i)
            more_rows_lower = []
            for i in range(pref_num_row_lower+1, len(pref_w_list[end_index_middle:])):
                more_rows_lower.append(i)

            # check all the possible number of rows which are less than the preferred number
            for num_row_lower in less_rows_lower:

                # flow in the bottom area
                result = horizontal_flow(sublayout_width, \
                                          sublayout_height - fixed_bottom, \
                                          num_row_lower, \
                                          pref_w_list[end_index_middle:], \
                                          pref_h_list[end_index_middle:], {}, True)

                # if we can put some widgets in this area, then compute the loss as usual
                if result != None:
                    result_index_lower, row_width_lower, row_height_lower, _ = result
                
                    # compute the loss of the bottom area
                    loss_lower = compute_loss(result_index_lower, row_width_lower, row_height_lower, \
                                           pref_w_list[end_index_middle:], pref_h_list[end_index_middle:])

                # if there is no widgets which can fit in this area, then the loss equals
                # the area of the available space
                else:
                    result_index_lower = [] 
                    row_width_lower = [] 
                    row_height_lower = []
                    loss_lower = ((sublayout_height - fixed_bottom) * sublayout_width) ** 2

                # get the best result
                if best_loss == None or best_loss > loss_upper + loss_middle + loss_lower:
                    best_loss = loss_upper + loss_middle + loss_lower
                    best_result_index_upper = result_index_upper
                    best_result_index_middle = result_index_middle
                    best_result_index_lower = result_index_lower
                    best_row_width_upper = row_width_upper
                    best_row_width_middle = row_width_middle
                    best_row_width_lower = row_width_lower
                    best_row_height_upper = row_height_upper
                    best_row_height_middle = row_height_middle
                    best_row_height_lower = row_height_lower
                    best_end_index_upper = end_index_upper
                    best_end_index_middle = end_index_middle
                else:
                    break  

            # check all the possible number of rows which are more than the preferred number
            for num_row_lower in more_rows_lower:
                
                # flow in the bottom area
                result = horizontal_flow(sublayout_width, \
                                          sublayout_height - fixed_bottom, \
                                          num_row_lower, \
                                          pref_w_list[end_index_middle:], \
                                          pref_h_list[end_index_middle:], {}, True)

                # if we can put some widgets in this area, then compute the loss as usual
                if result != None:
                    result_index_lower, row_width_lower, row_height_lower, _ = result
                
                    # compute the loss of the bottom area
                    loss_lower = compute_loss(result_index_lower, row_width_lower, row_height_lower, \
                                           pref_w_list[end_index_middle:], pref_h_list[end_index_middle:])

                # if there is no widgets which can fit in this area, then the loss equals
                # the area of the available space
                else:
                    result_index_lower = [] 
                    row_width_lower = [] 
                    row_height_lower = []
                    loss_lower = ((sublayout_height - fixed_bottom) * sublayout_width) ** 2

                # get the best result
                if best_loss == None or best_loss > loss_upper + loss_middle + loss_lower:
                    best_loss = loss_upper + loss_middle + loss_lower
                    best_result_index_upper = result_index_upper
                    best_result_index_middle = result_index_middle
                    best_result_index_lower = result_index_lower
                    best_row_width_upper = row_width_upper
                    best_row_width_middle = row_width_middle
                    best_row_width_lower = row_width_lower
                    best_row_height_upper = row_height_upper
                    best_row_height_middle = row_height_middle
                    best_row_height_lower = row_height_lower
                    best_end_index_upper = end_index_upper
                    best_end_index_middle = end_index_middle
                else:
                    break  

        # check all the possible number of rows which are more than the preferred number
        for num_row_middle in more_rows_middle:
            end_index_middle = horizontal_flow_connected_for_middle_area(fixed_left, sublayout_width - fixed_right, \
                                                      fixed_bottom - fixed_top, num_row_middle, \
                                                      pref_w_list[end_index_upper:], pref_h_list[end_index_upper:])
            end_index_middle += end_index_upper

            result = horizontal_flow_for_middle_area(fixed_left, \
                                                   sublayout_width - fixed_right, \
                                                   fixed_bottom - fixed_top, \
                                                   num_row_middle, \
                                        pref_w_list[end_index_upper:end_index_middle], \
                                        pref_h_list[end_index_upper:end_index_middle])

            # if we can put some widgets in this area, then compute the loss as usual
            if result != None:
                result_index_middle, row_width_middle, row_height_middle = result
            
                # compute the loss of the middle area
                loss_middle = compute_loss_for_middle_area(result_index_middle, row_width_middle, row_height_middle, \
                                                           pref_w_list[end_index_upper:end_index_middle], \
                                                           pref_h_list[end_index_upper:end_index_middle])

            # if there is no widgets which can fit in this area, then the loss equals
            # the area of the available space
            else:
                result_index_middle = []
                row_width_middle = [] 
                row_height_middle = []
                loss_middle = ((fixed_bottom - fixed_top) * (fixed_left + sublayout_width - fixed_right)) ** 2
                            
            # if the loss is already too large, then we skip this branch
            if best_loss != None and best_loss <= loss_upper + loss_middle:
                break

            ############### Bottom Area ###############
            # get the pref number of rows
            pref_num_row_lower = get_num_rows(sublayout_width, pref_w_list[end_index_middle:])

            # get all possible number of rows for the above area
            less_rows_lower = []
            for i in range(pref_num_row_lower, 0, -1):
                less_rows_lower.append(i)
            more_rows_lower = []
            for i in range(pref_num_row_lower+1, len(pref_w_list[end_index_middle:])):
                more_rows_lower.append(i)

            # check all the possible number of rows which are less than the preferred number
            for num_row_lower in less_rows_lower:

                # flow in the bottom area
                result = horizontal_flow(sublayout_width, \
                                          sublayout_height - fixed_bottom, \
                                          num_row_lower, \
                                          pref_w_list[end_index_middle:], \
                                          pref_h_list[end_index_middle:], {}, True)

                # if we can put some widgets in this area, then compute the loss as usual
                if result != None:
                    result_index_lower, row_width_lower, row_height_lower, _ = result
                
                    # compute the loss of the bottom area
                    loss_lower = compute_loss(result_index_lower, row_width_lower, row_height_lower, \
                                           pref_w_list[end_index_middle:], pref_h_list[end_index_middle:])

                # if there is no widgets which can fit in this area, then the loss equals
                # the area of the available space
                else:
                    result_index_lower = [] 
                    row_width_lower = [] 
                    row_height_lower = []
                    loss_lower = ((sublayout_height - fixed_bottom) * sublayout_width) ** 2

                # get the best result
                if best_loss == None or best_loss > loss_upper + loss_middle + loss_lower:
                    best_loss = loss_upper + loss_middle + loss_lower
                    best_result_index_upper = result_index_upper
                    best_result_index_middle = result_index_middle
                    best_result_index_lower = result_index_lower
                    best_row_width_upper = row_width_upper
                    best_row_width_middle = row_width_middle
                    best_row_width_lower = row_width_lower
                    best_row_height_upper = row_height_upper
                    best_row_height_middle = row_height_middle
                    best_row_height_lower = row_height_lower
                    best_end_index_upper = end_index_upper
                    best_end_index_middle = end_index_middle
                else:
                    break 

            # check all the possible number of rows which are more than the preferred number
            for num_row_lower in more_rows_lower:

                # flow in the bottom area
                result = horizontal_flow(sublayout_width, \
                                          sublayout_height - fixed_bottom, \
                                          num_row_lower, \
                                          pref_w_list[end_index_middle:], \
                                          pref_h_list[end_index_middle:], {}, True)

                # if we can put some widgets in this area, then compute the loss as usual
                if result != None:
                    result_index_lower, row_width_lower, row_height_lower, _ = result
                
                    # compute the loss of the bottom area
                    loss_lower = compute_loss(result_index_lower, row_width_lower, row_height_lower, \
                                           pref_w_list[end_index_middle:], pref_h_list[end_index_middle:])

                # if there is no widgets which can fit in this area, then the loss equals
                # the area of the available space
                else:
                    result_index_lower = [] 
                    row_width_lower = [] 
                    row_height_lower = []
                    loss_lower = ((sublayout_height - fixed_bottom) * sublayout_width) ** 2

                # get the best result
                if best_loss == None or best_loss > loss_upper + loss_middle + loss_lower:
                    best_loss = loss_upper + loss_middle + loss_lower
                    best_result_index_upper = result_index_upper
                    best_result_index_middle = result_index_middle
                    best_result_index_lower = result_index_lower
                    best_row_width_upper = row_width_upper
                    best_row_width_middle = row_width_middle
                    best_row_width_lower = row_width_lower
                    best_row_height_upper = row_height_upper
                    best_row_height_middle = row_height_middle
                    best_row_height_lower = row_height_lower
                    best_end_index_upper = end_index_upper
                    best_end_index_middle = end_index_middle
                else:
                    break 


    # check all the possible number of rows which are less than the preferred number
    for num_row_upper in more_rows_upper:
        
        # compute the result for the upper area of flowing around the fixed area
        end_index_upper = horizontal_flow_connected(sublayout_width, fixed_top, num_row_upper, \
                                              pref_w_list, pref_h_list)
        result_index_upper, row_width_upper, row_height_upper, _ = horizontal_flow(sublayout_width, \
                                                            fixed_top, num_row_upper, pref_w_list[:end_index_upper], \
                                                            pref_h_list[:end_index_upper], {}, True)
        loss_upper = compute_loss(result_index_upper, row_width_upper, row_height_upper, \
                                  pref_w_list[:end_index_upper], pref_h_list[:end_index_upper])
                                  
        # if the loss is already too large, then we skip this loop
        if best_loss != None and best_loss <= loss_upper:
            break

        ############### Middle Area ###############
        # compute the preferred number of rows in the middle area
        pref_num_row_middle = get_num_rows_for_middle_area(fixed_left, \
                                                           sublayout_width - fixed_right, \
                                                           fixed_bottom - fixed_top, \
                                                           pref_w_list[end_index_upper:], \
                                                           pref_h_list[end_index_upper:])

        # get the max number of rows
        max_num_row_middle = get_num_rows_for_middle_area(fixed_left, \
                                                         sublayout_width - fixed_right, \
                                                         sublayout_height, \
                                                         pref_w_list[end_index_upper:], \
                                                         pref_h_list[end_index_upper:])

        # get all possible number of rows for the above area
        less_rows_middle = []
        for i in range(pref_num_row_middle, 0, -1):
            less_rows_middle.append(i)
        more_rows_middle = []
        for i in range(pref_num_row_middle+1, max_num_row_middle+1):
            more_rows_middle.append(i)

        # check all the possible number of rows which are less than the preferred number
        for num_row_middle in less_rows_middle:
            end_index_middle = horizontal_flow_connected_for_middle_area(fixed_left, sublayout_width - fixed_right, \
                                                      fixed_bottom - fixed_top, num_row_middle, \
                                                      pref_w_list[end_index_upper:], pref_h_list[end_index_upper:])
            end_index_middle += end_index_upper
            result = horizontal_flow_for_middle_area(fixed_left, \
                                                   sublayout_width - fixed_right, \
                                                   fixed_bottom - fixed_top, \
                                                   num_row_middle, \
                                        pref_w_list[end_index_upper:end_index_middle], \
                                        pref_h_list[end_index_upper:end_index_middle])

            # if we can put some widgets in this area, then compute the loss as usual
            if result != None:
                result_index_middle, row_width_middle, row_height_middle = result
            
                # compute the loss of the middle area
                loss_middle = compute_loss_for_middle_area(result_index_middle, row_width_middle, row_height_middle, \
                                                           pref_w_list[end_index_upper:end_index_middle], \
                                                           pref_h_list[end_index_upper:end_index_middle])

            # if there is no widgets which can fit in this area, then the loss equals
            # the area of the available space
            else:
                result_index_middle = []
                row_width_middle = [] 
                row_height_middle = []
                loss_middle = ((fixed_bottom - fixed_top) * (fixed_left + sublayout_width - fixed_right)) ** 2
                            
            # if the loss is already too large, then we skip this branch
            if best_loss != None and best_loss <= loss_upper + loss_middle:
                break

            ############### Bottom Area ###############
            # get the pref number of rows
            pref_num_row_lower = get_num_rows(sublayout_width, pref_w_list[end_index_middle:])

            # get all possible number of rows for the above area
            less_rows_lower = []
            for i in range(pref_num_row_lower, 0, -1):
                less_rows_lower.append(i)
            more_rows_lower = []
            for i in range(pref_num_row_lower+1, len(pref_w_list[end_index_middle:])):
                more_rows_lower.append(i)

            # check all the possible number of rows which are less than the preferred number
            for num_row_lower in less_rows_lower:
                
                # flow in the bottom area
                result = horizontal_flow(sublayout_width, \
                                          sublayout_height - fixed_bottom, \
                                          num_row_lower, \
                                          pref_w_list[end_index_middle:], \
                                          pref_h_list[end_index_middle:], {}, True)

                # if we can put some widgets in this area, then compute the loss as usual
                if result != None:
                    result_index_lower, row_width_lower, row_height_lower, _ = result
                
                    # compute the loss of the bottom area
                    loss_lower = compute_loss(result_index_lower, row_width_lower, row_height_lower, \
                                           pref_w_list[end_index_middle:], pref_h_list[end_index_middle:])

                # if there is no widgets which can fit in this area, then the loss equals
                # the area of the available space
                else:
                    result_index_lower = [] 
                    row_width_lower = [] 
                    row_height_lower = []
                    loss_lower = ((sublayout_height - fixed_bottom) * sublayout_width) ** 2

                # get the best result
                if best_loss == None or best_loss > loss_upper + loss_middle + loss_lower:
                    best_loss = loss_upper + loss_middle + loss_lower
                    best_result_index_upper = result_index_upper
                    best_result_index_middle = result_index_middle
                    best_result_index_lower = result_index_lower
                    best_row_width_upper = row_width_upper
                    best_row_width_middle = row_width_middle
                    best_row_width_lower = row_width_lower
                    best_row_height_upper = row_height_upper
                    best_row_height_middle = row_height_middle
                    best_row_height_lower = row_height_lower
                    best_end_index_upper = end_index_upper
                    best_end_index_middle = end_index_middle
                else:
                    break  

            # check all the possible number of rows which are more than the preferred number
            for num_row_lower in more_rows_lower:
                
                # flow in the bottom area
                result = horizontal_flow(sublayout_width, \
                                          sublayout_height - fixed_bottom, \
                                          num_row_lower, \
                                          pref_w_list[end_index_middle:], \
                                          pref_h_list[end_index_middle:], {}, True)

                # if we can put some widgets in this area, then compute the loss as usual
                if result != None:
                    result_index_lower, row_width_lower, row_height_lower, _ = result
                
                    # compute the loss of the bottom area
                    loss_lower = compute_loss(result_index_lower, row_width_lower, row_height_lower, \
                                           pref_w_list[end_index_middle:], pref_h_list[end_index_middle:])

                # if there is no widgets which can fit in this area, then the loss equals
                # the area of the available space
                else:
                    result_index_lower = [] 
                    row_width_lower = [] 
                    row_height_lower = []
                    loss_lower = ((sublayout_height - fixed_bottom) * sublayout_width) ** 2

                # get the best result
                if best_loss == None or best_loss > loss_upper + loss_middle + loss_lower:
                    best_loss = loss_upper + loss_middle + loss_lower
                    best_result_index_upper = result_index_upper
                    best_result_index_middle = result_index_middle
                    best_result_index_lower = result_index_lower
                    best_row_width_upper = row_width_upper
                    best_row_width_middle = row_width_middle
                    best_row_width_lower = row_width_lower
                    best_row_height_upper = row_height_upper
                    best_row_height_middle = row_height_middle
                    best_row_height_lower = row_height_lower
                    best_end_index_upper = end_index_upper
                    best_end_index_middle = end_index_middle
                else:
                    break 

        # check all the possible number of rows which are more than the preferred number
        for num_row_middle in more_rows_middle:
            end_index_middle = horizontal_flow_connected_for_middle_area(fixed_left, sublayout_width - fixed_right, \
                                                      fixed_bottom - fixed_top, num_row_middle, \
                                                      pref_w_list[end_index_upper:], pref_h_list[end_index_upper:])
            end_index_middle += end_index_upper

            result = horizontal_flow_for_middle_area(fixed_left, \
                                                   sublayout_width - fixed_right, \
                                                   fixed_bottom - fixed_top, \
                                                   num_row_middle, \
                                        pref_w_list[end_index_upper:end_index_middle], \
                                        pref_h_list[end_index_upper:end_index_middle])
            
            # if we can put some widgets in this area, then compute the loss as usual
            if result != None:
                result_index_middle, row_width_middle, row_height_middle = result
            
                # compute the loss of the middle area
                loss_middle = compute_loss_for_middle_area(result_index_middle, row_width_middle, row_height_middle, \
                                                           pref_w_list[end_index_upper:end_index_middle], \
                                                           pref_h_list[end_index_upper:end_index_middle])

            # if there is no widgets which can fit in this area, then the loss equals
            # the area of the available space
            else:
                result_index_middle = []
                row_width_middle = [] 
                row_height_middle = []
                loss_middle = ((fixed_bottom - fixed_top) * (fixed_left + sublayout_width - fixed_right)) ** 2
                            
            # if the loss is already too large, then we skip this branch
            if best_loss != None and best_loss <= loss_upper + loss_middle:
                break

            ############### Bottom Area ###############
            # get the pref number of rows
            pref_num_row_lower = get_num_rows(sublayout_width, pref_w_list[end_index_middle:])

            # get all possible number of rows for the above area
            less_rows_lower = []
            for i in range(pref_num_row_lower, 0, -1):
                less_rows_lower.append(i)
            more_rows_lower = []
            for i in range(pref_num_row_lower+1, len(pref_w_list[end_index_middle:])):
                more_rows_lower.append(i)

            # check all the possible number of rows which are less than the preferred number
            for num_row_lower in less_rows_lower:

                # flow in the bottom area
                result = horizontal_flow(sublayout_width, \
                                          sublayout_height - fixed_bottom, \
                                          num_row_lower, \
                                          pref_w_list[end_index_middle:], \
                                          pref_h_list[end_index_middle:], {}, True)

                # if we can put some widgets in this area, then compute the loss as usual
                if result != None:
                    result_index_lower, row_width_lower, row_height_lower, _ = result
                
                    # compute the loss of the bottom area
                    loss_lower = compute_loss(result_index_lower, row_width_lower, row_height_lower, \
                                           pref_w_list[end_index_middle:], pref_h_list[end_index_middle:])

                # if there is no widgets which can fit in this area, then the loss equals
                # the area of the available space
                else:
                    result_index_lower = [] 
                    row_width_lower = [] 
                    row_height_lower = []
                    loss_lower = ((sublayout_height - fixed_bottom) * sublayout_width) ** 2

                # get the best result
                if best_loss == None or best_loss > loss_upper + loss_middle + loss_lower:
                    best_loss = loss_upper + loss_middle + loss_lower
                    best_result_index_upper = result_index_upper
                    best_result_index_middle = result_index_middle
                    best_result_index_lower = result_index_lower
                    best_row_width_upper = row_width_upper
                    best_row_width_middle = row_width_middle
                    best_row_width_lower = row_width_lower
                    best_row_height_upper = row_height_upper
                    best_row_height_middle = row_height_middle
                    best_row_height_lower = row_height_lower
                    best_end_index_upper = end_index_upper
                    best_end_index_middle = end_index_middle
                else:
                    break  

            # check all the possible number of rows which are more than the preferred number
            for num_row_lower in more_rows_lower:
                
                # flow in the bottom area
                result = horizontal_flow(sublayout_width, \
                                          sublayout_height - fixed_bottom, \
                                          num_row_lower, \
                                          pref_w_list[end_index_middle:], \
                                          pref_h_list[end_index_middle:], {}, True)

                # if we can put some widgets in this area, then compute the loss as usual
                if result != None:
                    result_index_lower, row_width_lower, row_height_lower, _ = result
                
                    # compute the loss of the bottom area
                    loss_lower = compute_loss(result_index_lower, row_width_lower, row_height_lower, \
                                           pref_w_list[end_index_middle:], pref_h_list[end_index_middle:])

                # if there is no widgets which can fit in this area, then the loss equals
                # the area of the available space
                else:
                    result_index_lower = [] 
                    row_width_lower = [] 
                    row_height_lower = []
                    loss_lower = ((sublayout_height - fixed_bottom) * sublayout_width) ** 2

                # get the best result
                if best_loss == None or best_loss > loss_upper + loss_middle + loss_lower:
                    best_loss = loss_upper + loss_middle + loss_lower
                    best_result_index_upper = result_index_upper
                    best_result_index_middle = result_index_middle
                    best_result_index_lower = result_index_lower
                    best_row_width_upper = row_width_upper
                    best_row_width_middle = row_width_middle
                    best_row_width_lower = row_width_lower
                    best_row_height_upper = row_height_upper
                    best_row_height_middle = row_height_middle
                    best_row_height_lower = row_height_lower
                    best_end_index_upper = end_index_upper
                    best_end_index_middle = end_index_middle
                else:
                    break 

    return best_result_index_upper, best_result_index_middle, best_result_index_lower, \
            best_row_width_upper, best_row_width_middle, best_row_width_lower, \
            best_row_height_upper, best_row_height_middle, best_row_height_lower, \
            best_end_index_upper, best_end_index_middle, best_loss                      

















	


