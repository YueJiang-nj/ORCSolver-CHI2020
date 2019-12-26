class Node:
    
    # width list = the list of widths of the widgets
    # height list =  the list of the heights of rows
    def __init__(self, parent, loss, width_list, top_boundary, height_list, start_index, finish):
        self.parent = parent
        self.loss = loss
        self.width_list = width_list
        self.top_boundary = top_boundary
        self.height_list = height_list
        self.start_index = start_index
        self.finish = finish

    def get_parent(self):
        return self.parent

    def get_loss(self):
        return self.loss

    def get_width_list(self):
        return self.width_list
    
    def get_top_boundary(self):
        return self.top_boundary

    def get_height_list(self):
        return self.height_list

    def get_start_index(self):
        return self.start_index

    def get_finish(self):
        return self.finish
