from abc import ABC, abstractmethod
from math import ceil, floor
from node import *
from flow_solver import *
import cvxpy as cvx
from copy import deepcopy


# global variables to store best results
best_leaf_result = None
best_leaf_loss = None
best_leaf = None


# create a abstract class for all the sublayouts
class ORCLayout(ABC):
    def __init__(self, name, parent, weight=1):
        super().__init__()
        
        # whether this node is the root
        self.root = False
        
        # set the name of the widget
        self.name = name
        
        # width and height of the sublayout
        # initially undefined
        self.height = -1
        self.width = -1
        
        # set parent and children of the node
        self.parent = parent
        self.children = []
        
        # add the current node as a child of its parent node
        if parent != None:
            parent.add_child(self)
        
        # initialize variables, constraints and objectives
        self.variables = {}
        self.constraints = []
        self.objectives = []
        
        # add boundary variables
        self.add_boundary_variables()
        
        # set to ORCColumn or ORCRow if this sublayout belongs to
        # an ORCColumn or an ORCRow
        self.belongs_to = None

        # a penalty weight for this sublayout, i.e., its priority or how
        # much we want it to have its preferred size.
        # set it to 1 by default, used as coeefficient in the objective function
        self.weight = weight
        
        # place to store the penalty value once the layout has been optimized
        self.loss = -1
    
    # set the weight of the sub-layout which represents the priority
    # of the sub-layout.
    def set_weight(self, weight):
        self.weight = weight
        
    # add child node
    def add_child(self, child):
        self.children.append(child)
    
    # get all the children of the node
    def get_children(self):
        return self.children
    
    # get the parent node
    def get_parent(self):
        return self.parent
    
    # add upper tree variables, constraints, objectives to this node
    def update_from_upper_tree(self):
        
        # if it has parent, then get all the variables, constraints, objectives
        # add upper tree variables to the variable dictionary of this node
        # add upper tree constraints to the constraint list of this node
        # add upper tree objectives to the objective list of this node
        # initialize variables, constraints and objectives
        if self.parent:
            self.variables.update(self.parent.variables.copy())
            self.constraints += self.parent.constraints.copy()
            self.objectives += self.parent.objectives.copy()

    # boundary variables
    def add_boundary_variables(self):
        left = cvx.Variable()
        right = cvx.Variable()
        top = cvx.Variable()
        bottom = cvx.Variable()
        self.variables[self.name + "_l"] = left
        self.variables[self.name + "_r"] = right
        self.variables[self.name + "_t"] = top
        self.variables[self.name + "_b"] = bottom
    
    # abstract method that constructs and retures constraints and objective
    # function summands for this layout and possibly some optimization variables
    @abstractmethod
    def constraint_spec(self):
        raise NotImplementedError('Function constraint_spec() needs to be implemented!')
    
    # recursively save a copy of constraints and objectives for the current node
    # and its descendants
    def copy_constraints(self):
        
        # create a copy of variables, constraints, and objectives
        self.variables_copy = self.variables.copy()
        self.constraints_copy = self.constraints.copy()
        self.objectives_copy = self.objectives.copy()
        
        # recurively save a copy for its descendants
        if self.get_children() != []:
            for child in self.get_children():
                child.copy_constraints()

    # solve the constraint system recursively
    def solve(self):
        global best_leaf_result
        global best_leaf_loss

        # True if it is the best leaf
        self.best = False

        # get the constraint system
        self.constraint_spec()
  
        # solve the constraint system
        obj = cvx.Minimize(cvx.sum(self.objectives))
        optimizer = cvx.Problem(obj, self.constraints)
        optimizer.solve()
        self.loss = optimizer.value
        
        # solve the lower level trees
        # if the current loss is larger than best leaf loss, then
        if best_leaf_result != None and best_leaf_loss < self.loss:
            pass
        else:
            if self.get_children() != []:
                for child in self.get_children():
                    child.solve()
        
                    # if any child can reach a best leaf, then it is true
                    if child.best == True:
                        self.best = True
        
            else:
                # compare the leaf node with the best result
                if best_leaf_result == None or best_leaf_loss > self.loss:
                    
                    # save all the best values for variables in the dictionary
                    # we don't save the leaf directly because all the variables
                    # are shared within different nodes, so whenever the solver runs,
                    # it changes the values of the variables in all the nodes. Then
                    # values in the previous saved best leaf are also changed.
                    for k, v in self.variables.items():
                        if v.value == None:
                            print("No Solution!")
                            exit()
                        else:
                            break
                    best_leaf_result = {k: round(float(v.value)) for k, v in self.variables.items()}
                    best_leaf_loss = self.loss
                    
                    # go back to root to update the widths and heights of the widgets
                    # in all the flows
                    global best_leaf
                    best_leaf = self
                    node = self
                    while (node.parent != None):
                        node = node.parent

                        # if the flow is a simple flow
                        # then store all the results for the flow
                        if isinstance(node, Flow) == True:
                            node.best_row_width = node.row_width
                            node.best_row_height = node.row_height

                    # indicate this is the best node
                    self.best = True

    # get best leaf and best leaf loss
    def get_best(self):
        global best_leaf_result
        global best_leaf_loss
        global best_leaf
        
        return best_leaf, best_leaf_result, best_leaf_loss


# class to define widgets
class ORCWidget(ORCLayout):
    
    # if this widget is not a part of the tree, then parent default is None
    def __init__(self, name, width_and_height, parent=None, optional=False):
        super().__init__(name, parent)
        self.copied_tree = False
        
        # set the widget to be optional or not
        self.optional = optional
        
        # save the min/pref/max sizes of the widget
        self.width_and_height = width_and_height
        width_min = width_and_height[0]
        width_pref = width_and_height[1]
        width_max = width_and_height[2]
        height_min = width_and_height[3]
        height_pref = width_and_height[4]
        height_max = width_and_height[5]
        self.width_min = width_min
        self.width_pref = width_pref
        self.width_max = width_max
        self.height_min = height_min
        self.height_pref = height_pref
        self.height_max = height_max
    
    # modify minimum width of the widget
    def modify_width_min(self, width_min):
        self.width_min = width_min

    # modify preferred width of the widget
    def modify_width_pref(self, width_pref):
        self.width_pref = width_pref
    
    # modify maximum width of the widget
    def modify_width_max(self, width_max):
        self.width_max = width_max
    
    # modify minimum height of the widget
    def modify_height_min(self, height_min):
        self.height_min = height_min
    
    # modify preferred height of the widget
    def modify_height_pref(self, height_pref):
        self.height_pref = height_pref
    
    # modify maximum height of the widget
    def modify_height_max(self, height_max):
        self.height_max = height_max

    # set a widget to be optional
    def set_optional(self):
        self.optional = True
    
    # add constraint specifications
    def constraint_spec(self):

        # add upper tree variables, constraints, objectives to this node
        self.update_from_upper_tree()
        
        # get boundary variables
        left = self.variables[self.name + "_l"]
        right = self.variables[self.name + "_r"]
        top = self.variables[self.name + "_t"]
        bottom = self.variables[self.name + "_b"]
        
        # min and max width and height constraints
        min_width_constraint = (right - left >= self.width_min)
        max_width_constraint = (right - left <= self.width_max)
        min_height_constraint = (bottom - top >= self.height_min)
        max_height_constraint = (bottom - top <= self.height_max)
        self.constraints += [min_width_constraint, max_width_constraint, \
                             min_height_constraint, max_height_constraint]
    
        # add soft constraints for preferred width and height
        # The soft constraint right - left == preferred size
        # can be written as right - left + delta == preferred_size
        # and then minimize weight * delta ^ 2
        # add variables for delta
        width_delta = cvx.Variable()
        height_delta = cvx.Variable()
        self.variables[self.name + "_w_delta"] = width_delta
        self.variables[self.name + "_h_delta"] = height_delta
        
        # add soft constraints for its preferred size
        pref_width_constraint = (right - left + width_delta == self.width_pref)
        pref_height_constraint = (bottom - top + height_delta == self.height_pref)
        self.constraints += [pref_width_constraint, pref_height_constraint]
        width_objective = self.weight * cvx.square(width_delta)
        height_objective = self.weight * cvx.square(height_delta)
        self.objectives +=  [width_objective, height_objective]


# class to define sublayouts with pivot structure
# switch between Column + HorizontalFlow and Row + VerticalFlow
class Pivot(ORCLayout):
    
    # if this node is root, then we input window width and window height
    # if the node is not root, then they are both set to be None
    def __init__(self, name, parent, window_width=None, window_height=None):
        super().__init__(name, parent)
        
        # if the node is the root, then set width to be window width
        # and set height to be window height
        if parent == None and window_width != None and window_height != None:
            global best_leaf_result, best_leaf_loss, best_leaf
            best_leaf_result = None
            best_leaf_loss = None
            best_leaf = None
            self.root = True
            self.width = window_width
            self.height = window_height

    # column_or_row is the layout Pivot wants to switch.
    # if the input is column, then column has higher priority than row
    # when the losses are the same.
    def set_layout(self, column_or_row):
        self.column_or_row = column_or_row
        self.column_or_row.width = self.width
        self.column_or_row.height = self.height
        self.column_or_row.root = self.root

    # recursively copy the children of the node
    def copy_children(self, node):
        if node.children != []:
            for i in range(len(node.get_children())):
                child = node.children[i]
                new_child = child
                new_child.copied_tree = False
                new_child.best = False
                
                # restore the variables, constraints, and objectives before update
                new_child.variables = {}
                new_child.constraints = []
                new_child.objectives = []
                new_child.add_boundary_variables()

                node.children[i] = new_child
                new_child.parent = node
                self.copy_children(new_child)

    # add constraint specifications
    def constraint_spec(self):
        
        # if it the node is the root, then its boundaries are window boundaries
        if self.root:
            left_constraint = (self.variables[self.name + "_l"] == 0)
            right_constraint = (self.variables[self.name + "_r"] == self.width)
            top_constraint = (self.variables[self.name + "_t"] == 0)
            bottom_constraint = (self.variables[self.name + "_b"] == self.height)
            self.constraints += [left_constraint, right_constraint, \
                                 top_constraint, bottom_constraint]
        
        # if column_or_row is a column structure
        if isinstance(self.column_or_row, ORCColumn):
            row = ORCRow(self.name, self, self.width, \
                         self.height)
            row.root = True
            column_copy = deepcopy(self.column_or_row)
            row.sublayouts = column_copy.sublayouts
            
            # copy the subtree of column_or_row and connect it to row
            row.children = column_copy.children
            for child in row.children:
                child.parent = row
            child.children[0].parent = child
        
            # check sublayouts, and switch from horizontal flow to vertical flow
            # also update sublayouts
            new_sublayouts = []
            for sublayout in row.sublayouts:
                if isinstance(sublayout, HorizontalFlow):
                    row.children.remove(sublayout)
                    vf = VerticalFlow(sublayout.name, sublayout.widget_list, \
                                      row)
                    new_sublayouts.append(vf)
                    vf.parent = sublayout.parent
                    vf.children = sublayout.children
                    self.copy_children(vf)
                else:
                    new_sublayouts.append(sublayout)
    
            # define the sublayouts of row
            row.define_sublayouts(new_sublayouts)

        # if column_or_row is a rpw structure
        elif isinstance(self.column_or_row, ORCRow):
            column = ORCColumn(self.name, self, self.width, \
                         self.height)
            column.root = True
            row_copy = deepcopy(self.column_or_row)
            column.sublayouts = row_copy.sublayouts

            # copy the subtree of column_or_row and connect it to row
            column.children = row_copy.children
            for child in column.get_children():
                child.parent = column
        
            # check sublayouts, and switch from horizontal flow to vertical flow
            # also update sublayouts
            new_sublayouts = []
            for sublayout in column.sublayouts:
                if isinstance(sublayout, VerticalFlow):
                    column.children.remove(sublayout)
                    hf = HorizontalFlow(sublayout.name, sublayout.widget_list, \
                                        column)
                    new_sublayouts.append(hf)
                    hf.parent = sublayout.parent
                    hf.children = sublayout.children
                    self.copy_children(hf)
                else:
                    new_sublayouts.append(sublayout)
                        
            # define the sublayouts of column
            column.define_sublayouts(new_sublayouts)



# class to define sublayouts with column structure
class ORCColumn(ORCLayout):
    
    # if this node is root, then we input window width and window height
    # if the node is not root, then they are both set to be None
    def __init__(self, name, parent, window_width=None, window_height=None):
        super().__init__(name, parent)
        self.back = False
        self.window_width = window_width
        self.window_height = window_height
        
        # if the node is the root, then set width to be window width
        # and set height to be window height
        if parent == None and window_width != None and window_height != None:
            global best_leaf_result, best_leaf_loss, best_leaf
            best_leaf_result = None
            best_leaf_loss = None
            best_leaf = None
            self.root = True
            self.width = window_width
            self.height = window_height

    # define the widgets or sublayouts contained in the column
    def define_sublayouts(self, sublayouts):
        self.sublayouts = sublayouts
        for layout in self.sublayouts:
            layout.belongs_to = self
    
    # add constraint specifications
    def constraint_spec(self):
        
        if not self.back:
            
            # add upper tree variables, constraints, objectives to this node
            self.update_from_upper_tree()

            # if it the node is the root, then its boundaries are window boundaries
            if self.root:
                left_constraint = (self.variables[self.name + "_l"] == 0)
                right_constraint = (self.variables[self.name + "_r"] == self.width)
                top_constraint = (self.variables[self.name + "_t"] == 0)
                bottom_constraint = (self.variables[self.name + "_b"] == self.height)
                self.constraints += [left_constraint, right_constraint, \
                                     top_constraint, bottom_constraint]
        
        # add boundary constraints for all the sublayouts in the column structure
        for i in range(len(self.sublayouts)):
            
            # in column structure, the left boundaries of all the sublayouts
            # are the same as the left boundaries of the column sublayout
            # the right boundaries of all the sublayouts
            # are the same as or less than the left boundaries of the column sublayout
            right_delta = cvx.Variable()
            self.variables[self.name + str(i) + "_r_delta"] = right_delta
            left_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_l"] \
                               == self.variables[self.name + "_l"])
            right_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_r"] + right_delta \
                                == self.variables[self.name + "_r"])
            right_constraint_hard = (self.sublayouts[i].variables[self.sublayouts[i].name + "_r"] \
                                <= self.variables[self.name + "_r"])
            right_objective = self.weight * cvx.square(right_delta)
            self.sublayouts[i].objectives += [right_objective]
            
            # the top boundary of each sublayout in the column structure is the same
            # as the bottom boundary of the previous sublayout in the column structure
            if i == 0:
                top_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_t"] \
                                   == self.variables[self.name + "_t"])
            else:
                top_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_t"] \
                                   == self.sublayouts[i-1].variables[self.sublayouts[i-1].name + "_b"])
            self.sublayouts[i].constraints += [left_constraint, right_constraint, top_constraint, right_constraint_hard]
            
            # the bottom boundary of the last sublayout in the column sturcture is
            # the same as or less than the bottom boundary of the column structure
            if i == len(self.sublayouts) - 1:
                bottom_delta = cvx.Variable()
                self.variables[self.name + "_b_delta"] = bottom_delta
                bottom_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_b"] + bottom_delta \
                                    == self.variables[self.name + "_b"])
                bottom_constraint_hard = (self.sublayouts[i].variables[self.sublayouts[i].name + "_b"] \
                                     <= self.variables[self.name + "_b"])
                self.sublayouts[i].constraints += [bottom_constraint, bottom_constraint_hard]
                bottom_objective = self.weight * cvx.square(bottom_delta)
                self.sublayouts[i].objectives += [bottom_objective]


class ORCRow(ORCLayout):
    
    # if this node is root, then we input window width and window height
    # if the node is not root, then they are both set to be None
    def __init__(self, name, parent, window_width=None, window_height=None):
        super().__init__(name, parent)
        self.back = False
        self.window_width = window_width
        self.window_height = window_height
        
        # if the node is the root, then set width to be window width
        # and set height to be window height
        if parent == None and window_width != None and window_height != None:
            global best_leaf_result, best_leaf_loss, best_leaf
            best_leaf_result = None
            best_leaf_loss = None
            best_leaf = None
            self.root = True
            self.width = window_width
            self.height = window_height

    # define the widgets or sublayouts contained in the column
    def define_sublayouts(self, sublayouts):
        self.sublayouts = sublayouts
        for layout in self.sublayouts:
            layout.belongs_to = self
    
    # add constraint specifications
    def constraint_spec(self):

        if not self.back:
        
            # add upper tree variables, constraints, objectives to this node
            self.update_from_upper_tree()
            
            # if it the node is the root, then its boundaries are window boundaries
            if self.root:
                left_constraint = (self.variables[self.name + "_l"] == 0)
                right_constraint = (self.variables[self.name + "_r"] == self.width)
                top_constraint = (self.variables[self.name + "_t"] == 0)
                bottom_constraint = (self.variables[self.name + "_b"] == self.height)
                self.constraints += [left_constraint, right_constraint, \
                                     top_constraint, bottom_constraint]
        
        # add boundary constraints for all the sublayouts in the row structure
        for i in range(len(self.sublayouts)):
            
            
            # in column structure, the top boundaries of all the sublayouts
            # are the same as the top boundaries of the row sublayout
            # the bottom boundaries of all the sublayouts
            # are the same as or less than the bottom boundaries of the row sublayout
            bottom_delta = cvx.Variable()
            self.variables[self.name + str(i) + "_b_delta"] = bottom_delta
            top_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_t"] \
                               == self.variables[self.name + "_t"])
            bottom_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_b"] + bottom_delta \
                                 == self.variables[self.name + "_b"])
            bottom_constraint_hard = (self.sublayouts[i].variables[self.sublayouts[i].name + "_b"] \
                                      <= self.variables[self.name + "_b"])
            bottom_objective = self.weight * cvx.square(bottom_delta)
            self.sublayouts[i].objectives += [bottom_objective]
           
            # the left boundary of each sublayout in the column structure is the same
            # as the right boundary of the previous sublayout in the column structure
            if i == 0:
               left_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_l"] \
                                 == self.variables[self.name + "_l"])
            else:
               left_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_l"] \
                                 == self.sublayouts[i-1].variables[self.sublayouts[i-1].name + "_r"])
            self.sublayouts[i].constraints += [left_constraint, bottom_constraint, \
                                               bottom_constraint_hard, top_constraint]

            # the right boundary of the last sublayout in the column sturcture is
            # the same as the right boundary of the column structure
            if i == len(self.sublayouts) - 1:
                right_delta = cvx.Variable()
                self.variables[self.name + "_r_delta"] = right_delta
                right_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_r"] + right_delta \
                                    == self.variables[self.name + "_r"])
                right_constraint_hard = (self.sublayouts[i].variables[self.sublayouts[i].name + "_r"] \
                                         <= self.variables[self.name + "_r"])
                self.sublayouts[i].constraints += [right_constraint, right_constraint_hard]
                right_objective = self.weight * cvx.square(right_delta)
                self.sublayouts[i].objectives += [right_objective]


# Here we assume all the widgets in the flow layout have the SAME size
# We also have a function for solving different-size flows in the file
# flow_solver.py called diff_type_widget.
class Flow(ORCLayout, ABC):

    def __init__(self, name, widget_list, parent, balanced=False, \
                 fixed_boundary=False, boundary_distance=None):
        super().__init__(name, parent)
        self.widget_list = widget_list
        self.num_widgets = len(self.widget_list)
        self.fixed_boundary = fixed_boundary
        self.boundary_distance = boundary_distance
        
        # sort the optional widget list
        # key is widget, value is its weight
        optional_widgets = {}
        for i in range(len(self.widget_list)):
            if self.widget_list[i].optional:
                optional_widgets[i] = self.widget_list[i].weight
        optional_widgets = sorted(optional_widgets.items(), key=lambda kv:kv[1])
        self.optional_index_weight_dict = {}
        for (k, v) in optional_widgets:
            self.optional_index_weight_dict[k] = v
    
        # if the flow is balanced, then we compute the factors of
        # the number of widgets in the flow
        self.balanced = balanced
        if self.balanced:
            self.factors = get_factors(len(self.widget_list))
        
        # by default, the flow does not connect to any other flow
        self.connect_to = None
        
        # True if it is a copied tree
        self.copied_tree = False
        
        # possible number of rows / columns in flows
        self.possible_smaller_num = []
        self.possible_larger_num = []
            
        # gather all the min/pref/max widths and heights of widgets in the flow
        self.min_w_list = []
        self.pref_w_list = []
        self.max_w_list = []
        self.min_h_list = []
        self.pref_h_list = []
        self.max_h_list = []
        for i in range(len(self.widget_list)):
            self.min_w_list.append(self.widget_list[i].width_min)
            self.pref_w_list.append(self.widget_list[i].width_pref)
            self.max_w_list.append(self.widget_list[i].width_max)
            self.min_h_list.append(self.widget_list[i].height_min)
            self.pref_h_list.append(self.widget_list[i].height_pref)
            self.max_h_list.append(self.widget_list[i].height_max)

    # define connected flows (e.g. top toolbar and left toolbar can be connected)
    def connect_to_flow(self, other_flow):
        self.connect_to = other_flow

    # copy the subtree of this node
    def copy_tree(self):
        new_subtree = deepcopy(self)
        
        # restore the variables, constraints, and objectives before update
        new_subtree.variables = {}
        new_subtree.constraints = []
        new_subtree.objectives = []
        new_subtree.add_boundary_variables()

        # recursively copy the subtree
        new_subtree.copied_tree = True
        new_subtree.best = False
        self.copy_children(new_subtree)

        return new_subtree

    # recursively copy the children of the node
    def copy_children(self, node):
        if node.children != []:
            for i in range(len(node.get_children())):
                child = node.children[i]
                new_child = child
                new_child.copied_tree = False
                new_child.best = False
                
                # restore the variables, constraints, and objectives before update
                new_child.variables = {}
                new_child.constraints = []
                new_child.objectives = []
                new_child.add_boundary_variables()

                node.children[i] = new_child
                new_child.parent = node
                self.copy_children(new_child)

    

    # solve the constraint system recursively
    def solve(self):
        global best_leaf_result
        global best_leaf_loss
        
        # whether it is the best leaf
        self.best = False
        
        # recursively save a copy of constraints and objectives for the current node
        # and its descendants
        if self.copied_tree == False:
            self.copy_constraints()

        # get the constraint system
        if self.constraint_spec() == "No Solution!":
            if self.optional_widget_list == []:
                return
            while self.optional_widget_list != []:
                self.widget_list.remove(self.optional_widget_list.pop(0))
                
                # gather all the min/pref/max widths and heights of widgets in the flow
                self.min_w_list = []
                self.pref_w_list = []
                self.max_w_list = []
                self.min_h_list = []
                self.pref_h_list = []
                self.max_h_list = []
                for i in range(len(self.widget_list)):
                    self.min_w_list.append(self.widget_list[i].width_min)
                    self.pref_w_list.append(self.widget_list[i].width_pref)
                    self.max_w_list.append(self.widget_list[i].width_max)
                    self.min_h_list.append(self.widget_list[i].height_min)
                    self.pref_h_list.append(self.widget_list[i].height_pref)
                    self.max_h_list.append(self.widget_list[i].height_max)
            
                # check whether a solution exists
                if self.constraint_spec() != "No Solution!":
                    break
                elif self.optional_widget_list == {}:
                    return
        
        # solve the constraint system
        self.loss = self.parent.loss + self.flow_loss
        
        # solve the constraint system
        obj = cvx.Minimize(cvx.sum(self.objectives))
        optimizer = cvx.Problem(obj, self.constraints)
        optimizer.solve()
        
        # solve the lower level trees
        # if the current loss is larger than best leaf loss, then ignore the subtree
        # if no solution, the loss is inf
        if best_leaf_result != None and best_leaf_loss < self.loss:
            pass
        else:
            if self.get_children() != []:
                for child in self.get_children():
                    
                    # solve the child node
                    child.solve()
                    
                    # if any child can reach a best leaf, then it is true
                    if child.best == True:
                        self.best = True
            else:
                # compare the leaf node with the best result
                if best_leaf_result == None or best_leaf_loss > self.loss:
                    
                    # save all the best values for variables in the dictionary
                    # we don't save the leaf directly because all the variables
                    # are shared within different nodes, so whenever the solver runs,
                    # it changes the values of the variables in all the nodes. Then
                    # values in the previous saved best leaf are also changed.
                    best_leaf_result = {k: round(float(v.value)) for k, v in self.variables.items()}
                    best_leaf_loss = self.loss
                    
                    # go back to root to update the widths and heights of the widgets
                    # in all the flows
                    global best_leaf
                    best_leaf = self
                    node = self
                    while (node.parent != None):

                        # if the flow is a simple flow
                        # then store all the results for the flow
                        if isinstance(node, Flow) == True:
                            node.best_row_width = node.row_width
                            node.best_row_height = node.row_height

                        # go to the parent node
                        node = node.parent
                    
                    # indicate we get better solution in the leaf
                    self.best = True
        
        if not self.copied_tree:
            # check smaller possible number
            while self.possible_smaller_num != []:
                num = self.possible_smaller_num.pop(0)
                
                # copy a subtree to reflow
                subtree = self.copy_tree()
                if isinstance(self, HorizontalFlow):
                    subtree.pref_row = num
                else:
                    subtree.pref_col = num
            
                # solve the subtree
                subtree.solve()
                
                # if we cannot get a better solution via this subtree, then stop
                # searching for smaller numbers
                if subtree.best == False:
                    break

            # check larger possible number
            while self.possible_larger_num != []:
                num = self.possible_larger_num.pop(0)

                # copy a subtree to reflow
                subtree = self.copy_tree()
                if isinstance(self, HorizontalFlow):
                    subtree.pref_row = num
                else:
                    subtree.pref_col = num

                # solve the subtree
                subtree.solve()

                # if we cannot get a better solution via this subtree, then stop
                # searching for larger numbers
                if subtree.best == False:
                    break


# Horizontal flow layout
class HorizontalFlow(Flow):

    # add constraint specifications
    def constraint_spec(self):
        
        # initialize flow loss
        self.flow_loss = 0
            
        # add upper tree variables, constraints, objectives to this node
        self.update_from_upper_tree()
        
        # solve the constraint system to get the width and height of the flow sublayout
        obj = cvx.Minimize(cvx.sum(self.objectives))
        optimizer = cvx.Problem(obj, self.constraints)
        optimizer.solve()
        self.width = self.variables[self.name + "_r"].value - self.variables[self.name + "_l"].value
        
        # if it is the last sublayout in the column/row structure, then it has fixed boundary
        if self.variables[self.name + "_b"].value != None:
            self.fixed_boundary = True
            self.height = self.variables[self.name + "_b"].value - self.variables[self.name + "_t"].value
        else:
            self.height = self.variables[self.parent.name + "_b"].value - self.variables[self.name + "_t"].value
        
        self.pref_row = get_num_rows(self.width, self.pref_w_list)

        # get the lists of width and height lists for connected flows
        if self.connect_to != None:
            entire_min_w_list = self.min_w_list + self.connect_to.min_w_list
            entire_pref_w_list = self.pref_w_list + self.connect_to.pref_w_list
            entire_max_w_list = self.max_w_list + self.connect_to.max_w_list
            entire_min_h_list = self.min_h_list + self.connect_to.min_h_list
            entire_pref_h_list = self.pref_h_list + self.connect_to.pref_h_list
            entire_max_h_list = self.max_h_list + self.connect_to.max_h_list
            index = horizontal_flow_connected(self.width, self.height, self.pref_row, \
                                              entire_pref_w_list, entire_pref_h_list)
            self.min_w_list = entire_min_w_list[:index]
            self.pref_w_list = entire_pref_w_list[:index]
            self.max_w_list = entire_max_w_list[:index]
            self.min_h_list = entire_min_h_list[:index]
            self.pref_h_list = entire_pref_h_list[:index]
            self.max_h_list = entire_max_h_list[:index]
            self.connect_to.min_w_list = entire_min_w_list[index:]
            self.connect_to.pref_w_list = entire_pref_w_list[index:]
            self.connect_to.max_w_list = entire_max_w_list[index:]
            self.connect_to.min_h_list = entire_min_h_list[index:]
            self.connect_to.pref_h_list = entire_pref_h_list[index:]
            self.connect_to.max_h_list = entire_max_h_list[index:]

        print(len(self.pref_w_list), "AAAAA")
        # calculate the flow result
        result = horizontal_flow(self.width, self.height, len(self.pref_w_list), \
                                 self.min_w_list, self.pref_w_list, self.max_w_list, \
                                 self.min_w_list, self.pref_h_list, self.max_h_list)
        if result == None:
            return "No Solution!"
        else:
            self.row_width, self.row_height, flow_loss = result
            self.flow_loss += flow_loss

            # the bottom boundary of the last widget is the same as the bottom boundary
            # of the sublayout
            bottom_constraint = (sum(self.row_height) + self.variables[self.name + "_t"] \
                                           == self.variables[self.name + "_b"])
            self.constraints += [bottom_constraint]


# Vertical flow layout
class VerticalFlow(Flow):

    # add constraint specifications
    def constraint_spec(self):
        
        # initialize flow loss
        self.flow_loss = 0          

        # add upper tree variables, constraints, objectives to this node
        self.update_from_upper_tree()

        # solve the constraint system to get the width and height of the flow sublayout
        obj = cvx.Minimize(cvx.sum(self.objectives))
        optimizer = cvx.Problem(obj, self.constraints)
        optimizer.solve()
        self.height = self.variables[self.name + "_b"].value - self.variables[self.name + "_t"].value

        # if it is the last sublayout in the column/row structure, then it has fixed boundary
        if self.variables[self.name + "_r"].value != None:
            self.fixed_boundary = True
            self.width = self.variables[self.name + "_r"].value - self.variables[self.name + "_l"].value
        else:
            self.width = self.variables[self.parent.name + "_r"].value - self.variables[self.name + "_l"].value

        self.pref_col = get_num_cols(self.height, self.pref_h_list)

        # get the lists of width and height lists for connected flows
        if self.connect_to != None:
            entire_min_w_list = self.min_w_list + self.connect_to.min_w_list
            entire_pref_w_list = self.pref_w_list + self.connect_to.pref_w_list
            entire_max_w_list = self.max_w_list + self.connect_to.max_w_list
            entire_min_h_list = self.min_h_list + self.connect_to.min_h_list
            entire_pref_h_list = self.pref_h_list + self.connect_to.pref_h_list
            entire_max_h_list = self.max_h_list + self.connect_to.max_h_list
            index = vertical_flow_connected(self.width, self.height, self.pref_col, \
                                              entire_pref_w_list, entire_pref_h_list)
            self.min_w_list = entire_min_w_list[:index]
            self.pref_w_list = entire_pref_w_list[:index]
            self.max_w_list = entire_max_w_list[:index]
            self.min_h_list = entire_min_h_list[:index]
            self.pref_h_list = entire_pref_h_list[:index]
            self.max_h_list = entire_max_h_list[:index]
            self.connect_to.min_w_list = entire_min_w_list[index:]
            self.connect_to.pref_w_list = entire_pref_w_list[index:]
            self.connect_to.max_w_list = entire_max_w_list[index:]
            self.connect_to.min_h_list = entire_min_h_list[index:]
            self.connect_to.pref_h_list = entire_pref_h_list[index:]
            self.connect_to.max_h_list = entire_max_h_list[index:]

        # calculate the flow result
        result = vertical_flow(self.width, self.height, len(self.pref_w_list), \
                               self.min_w_list, self.pref_w_list, self.max_w_list, \
                               self.min_w_list, self.pref_h_list, self.max_h_list)
        if result == None:
            return "No Solution!"
        else:
            self.row_height, self.row_width, flow_loss = result
            self.flow_loss += flow_loss

            # the bottom boundary of the last widget is the same as the bottom boundary
            # of the sublayout
            right_constraint = (sum(self.row_width) + self.variables[self.name + "_l"] \
                                           == self.variables[self.name + "_r"])
            self.constraints += [right_constraint]





