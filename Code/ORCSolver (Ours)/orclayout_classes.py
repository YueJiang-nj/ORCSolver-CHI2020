from abc import ABC, abstractmethod
from math import ceil, floor
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
    
    # abstract method that constructs the constraint system including optimization variables, 
    # constraints, and objective functions for this layout.
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

        if self.parent != None:
            self.loss = self.parent.loss
  
        # solve the lower level trees
        # if the current loss is larger than best leaf loss, then
        if self.get_children() != []:
            for child in self.get_children():
                child.solve()
    
                # if any child can reach a best leaf, then it is true
                if child.best == True:
                    self.best = True
    
        else:
            
            # solve the constraint system
            obj = cvx.Minimize(cvx.sum(self.objectives))
            optimizer = cvx.Problem(obj, self.constraints)
            optimizer.solve()
            self.loss += optimizer.value

            # compare the leaf node with the best result
            if (best_leaf_result == None or best_leaf_loss > self.loss) and self.loss != inf:
                
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
                    node = node.parent

                    # if the flow is flowing around a fixed area, 
                    # then store all the results for upper, middle, and lower areas
                    if isinstance(node, FlowAroundFix) == True:
                        node.best_row_width_upper = node.row_width_upper
                        node.best_row_height_upper = node.row_height_upper
                        node.best_result_index_upper = node.result_index_upper
                        node.best_row_width_middle = node.row_width_middle
                        node.best_row_height_middle = node.row_height_middle
                        node.best_result_index_middle = node.result_index_middle
                        node.best_row_width_lower = node.row_width_lower
                        node.best_row_height_lower = node.row_height_lower
                        node.best_result_index_lower = node.result_index_lower

                    # if the flow is a simple flow
                    # then store all the results for the flow
                    elif isinstance(node, Flow) == True:
                        node.best_row_width = node.row_width
                        node.best_row_height = node.row_height
                        node.best_result_index = node.result_index

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
        width_objective = self.weight * cvx.square(right - left - self.width_pref)
        height_objective = self.weight * cvx.square(bottom - top - self.height_pref)
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

        # if it the node is the root, then its boundaries are window boundaries
        if self.root:
            left_constraint = (self.variables[self.name + "_l"] == 0)
            right_constraint = (self.variables[self.name + "_r"] == self.width)
            top_constraint = (self.variables[self.name + "_t"] == 0)
            bottom_constraint = (self.variables[self.name + "_b"] == self.height)
            self.constraints += [left_constraint, right_constraint, \
                                 top_constraint, bottom_constraint]

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

        self.update_from_upper_tree()
    
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
            row = ORCRow(self.column_or_row.name, self, self.width, \
                         self.height)
            if self.root:
                row.root = True
            else: 
                row.root = False
            column_copy = deepcopy(self.column_or_row)
            row.sublayouts = column_copy.sublayouts
            
            # copy the subtree of column_or_row and connect it to row
            row.children = column_copy.children
            for child in row.children:
                child.parent = row
            if len(child.children) > 0:
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
            column = ORCColumn(self.column_or_row.name, self, self.width, \
                         self.height)
            if self.root:
                column.root = True
            else: 
                column.root = False
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
        if parent == None: 
            global best_leaf_result, best_leaf_loss, best_leaf
            best_leaf_result = None
            best_leaf_loss = None
            best_leaf = None
        
        if isinstance(parent, Pivot):
            self.width = self.parent.width
            self.height = self.parent.height

        if window_width != None and window_height != None:
            self.root = True
            self.width = window_width
            self.height = window_height

    # define the widgets or sublayouts contained in the column
    def define_sublayouts(self, sublayouts):
        self.sublayouts = sublayouts
        for layout in self.sublayouts:
            layout.belongs_to = self
            if isinstance(layout, Pivot):
                layout.children[0].belongs_to = self
    
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
            elif isinstance(self.parent, Pivot): 
                left_constraint = (self.variables[self.name + "_l"] == self.variables[self.parent.name + "_l"])
                right_constraint = (self.variables[self.name + "_r"] == self.variables[self.parent.name + "_r"])
                top_constraint = (self.variables[self.name + "_t"] == self.variables[self.parent.name + "_t"])
                bottom_constraint = (self.variables[self.name + "_b"] == self.variables[self.parent.name + "_b"])
                self.constraints += [left_constraint, right_constraint, \
                                     top_constraint, bottom_constraint]
        
        # add boundary constraints for all the sublayouts in the column structure
        for i in range(len(self.sublayouts)):
            
            # in column structure, the left boundaries of all the sublayouts
            # are the same as the left boundaries of the column sublayout
            # the right boundaries of all the sublayouts
            # are the same as or less than the left boundaries of the column sublayout
            left_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_l"] \
                               == self.variables[self.name + "_l"])
            right_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_r"] 
                                == self.variables[self.name + "_r"])
            
            # the top boundary of each sublayout in the column structure is the same
            # as the bottom boundary of the previous sublayout in the column structure
            if i == 0:
                top_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_t"] \
                                   == self.variables[self.name + "_t"])
            else:
                top_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_t"] \
                                   == self.sublayouts[i-1].variables[self.sublayouts[i-1].name + "_b"])
            self.sublayouts[i].constraints += [left_constraint, right_constraint, top_constraint]
            
            # the bottom boundary of the last sublayout in the column sturcture is
            # the same as or less than the bottom boundary of the column structure
            if i == len(self.sublayouts) - 1:
                bottom_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_b"]
                                    == self.variables[self.name + "_b"])
                self.sublayouts[i].constraints += [bottom_constraint]


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
        if parent == None: 
            global best_leaf_result, best_leaf_loss, best_leaf
            best_leaf_result = None
            best_leaf_loss = None
            best_leaf = None

        if isinstance(parent, Pivot):
            # self.root = True
            self.width = self.parent.width
            self.height = self.parent.height

        if window_width != None and window_height != None:
            self.root = True
            self.width = window_width
            self.height = window_height

    # define the widgets or sublayouts contained in the column
    def define_sublayouts(self, sublayouts):
        self.sublayouts = sublayouts
        for layout in self.sublayouts:
            layout.belongs_to = self
            if isinstance(layout, Pivot):
                layout.children[0].belongs_to = self
    
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
            elif isinstance(self.parent, Pivot):
                left_constraint = (self.variables[self.name + "_l"] == self.variables[self.parent.name + "_l"])
                right_constraint = (self.variables[self.name + "_r"] == self.variables[self.parent.name + "_r"])
                top_constraint = (self.variables[self.name + "_t"] == self.variables[self.parent.name + "_t"])
                bottom_constraint = (self.variables[self.name + "_b"] == self.variables[self.parent.name + "_b"])
                self.constraints += [left_constraint, right_constraint, \
                                     top_constraint, bottom_constraint]
        
        # add boundary constraints for all the sublayouts in the row structure
        for i in range(len(self.sublayouts)):
            
            
            # in column structure, the top boundaries of all the sublayouts
            # are the same as the top boundaries of the row sublayout
            # the bottom boundaries of all the sublayouts
            # are the same as or less than the bottom boundaries of the row sublayout
            top_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_t"] \
                               == self.variables[self.name + "_t"])
            bottom_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_b"]
                                 == self.variables[self.name + "_b"])
           
            # the left boundary of each sublayout in the column structure is the same
            # as the right boundary of the previous sublayout in the column structure
            if i == 0:
               left_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_l"] \
                                 == self.variables[self.name + "_l"])
            else:
               left_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_l"] \
                                 == self.sublayouts[i-1].variables[self.sublayouts[i-1].name + "_r"])
            self.sublayouts[i].constraints += [left_constraint, bottom_constraint, \
                                               top_constraint]

            # the right boundary of the last sublayout in the column sturcture is
            # the same as the right boundary of the column structure
            if i == len(self.sublayouts) - 1:
                right_constraint = (self.sublayouts[i].variables[self.sublayouts[i].name + "_r"]
                                    == self.variables[self.name + "_r"])
                self.sublayouts[i].constraints += [right_constraint]


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

        # True if we force the min/max constraints
        self.force_bound = False
        
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

    # force the min/max constraints
    def set_force_bound(self):
        self.force_bound = True

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
            if hasattr(self, 'optional_widget_list'):
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
        
        # solve the lower level trees
        # if the current loss is larger than best leaf loss, then ignore the subtree
        # if no solution, the loss is inf
        if self.get_children() != []:
            for child in self.get_children():
                
                # solve the child node
                child.solve()
                
                # if any child can reach a best leaf, then it is true
                if child.best == True:
                    self.best = True
        else:

            # solve the constraint system
            obj = cvx.Minimize(cvx.sum(self.objectives))
            optimizer = cvx.Problem(obj, self.constraints)
            optimizer.solve()
            self.loss += optimizer.value

            # compare the leaf node with the best result
            if (best_leaf_result == None or best_leaf_loss > self.loss) and self.loss != inf:
                
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

                    # if the flow is flowing around a fixed area, 
                    # then store all the results for upper, middle, and lower areas
                    if isinstance(node, FlowAroundFix) == True:
                        node.best_row_width_upper = node.row_width_upper
                        node.best_row_height_upper = node.row_height_upper
                        node.best_result_index_upper = node.result_index_upper
                        node.best_row_width_middle = node.row_width_middle
                        node.best_row_height_middle = node.row_height_middle
                        node.best_result_index_middle = node.result_index_middle
                        node.best_row_width_lower = node.row_width_lower
                        node.best_row_height_lower = node.row_height_lower
                        node.best_result_index_lower = node.result_index_lower

                    # if the flow is a simple flow
                    # then store all the results for the flow
                    elif isinstance(node, Flow) == True:
                        node.best_row_width = node.row_width
                        node.best_row_height = node.row_height
                        node.best_result_index = node.result_index

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
        
        # fixed boundary distance
        if self.boundary_distance != None:
            boundary_distance_constraint = (self.variables[self.name + "_b"] \
                                            == self.variables[self.name + "_t"] + self.boundary_distance)
            self.constraints += [boundary_distance_constraint]

        # we compute the preferred widgets in each row
        if not hasattr(self, 'pref_row'):
            self.copied_tree = False
        if self.copied_tree:
            
            # go back to the column/row it belongs to and add corresponding constraints
            self.belongs_to.back = True
            self.belongs_to.constraint_spec()
            
            # add upper tree variables, constraints, objectives to this node
            self.update_from_upper_tree()
        
        else:
            
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
            
            # if it is the original tree, then we apply our heuristics to get the min/pref/max number of rows
            if self.connect_to == None:
                self.min_row = 1        # get_num_rows(self.width, self.min_w_list) if no optional widgets
                self.pref_row = get_num_rows(self.width, self.pref_w_list)
                self.max_row = get_num_rows(self.width, self.max_w_list)
            else:
                # if it is connected to another flow then we also need to count the widgets in the connected flow
                self.min_row = 1
                self.pref_row = get_num_rows(self.width, self.pref_w_list)
                self.max_row = get_num_rows(self.width, self.max_w_list + self.connect_to.max_w_list)
            
            # put all the possible number of rows in the list
            if not self.balanced:
                self.possible_smaller_num = list(range(self.pref_row - 1, self.min_row - 1, -1))
                self.possible_larger_num = list(range(self.pref_row + 1, self.max_row + 1))
            else:
                for i in range(self.pref_row - 1, self.min_row - 1, -1):
                    if i in self.factors:
                        self.possible_smaller_num.append(i)
                for i in range(self.pref_row + 1, self.max_row + 1):
                    if i in self.factors:
                        self.possible_larger_num.append(i)


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

        # calculate the flow result
        result = horizontal_flow(self.width, self.height, self.pref_row, \
                                 self.pref_w_list, self.pref_h_list, \
                                 self.optional_index_weight_dict, self.fixed_boundary)
        if result == None:
            self.flow_loss = inf
            return "No Solution!"
        else:
            self.result_index, self.row_width, self.row_height, flow_loss = result
            self.flow_loss += flow_loss

        # The loss is the distance between preferred sizes and result sizes
        self.flow_loss += compute_loss(self.result_index, self.row_width, self.row_height, \
                                        self.pref_w_list, self.pref_h_list)

        # check whether the widget size is larger than the max size or min size
        # if so, add more loss
        self.flow_loss += compute_additional_loss(self.result_index, self.row_width, self.row_height, self.widget_list, \
                                self.max_w_list, self.min_w_list, self.max_h_list, self.min_h_list)

        # the bottom boundary of the last widget in the flow sublayout is the same as
        # the bottom boundary of the flow sublayout
        if self.variables[self.name + "_b"].value == None:
            bottom_constraint = (self.variables[self.name + "_b"] \
                                == self.variables[self.name + "_t"] + sum(self.row_height))
            self.constraints += [bottom_constraint]

        # if the bottom boundary is also fixed, then we also need to take
        # the empty space to the bottom boundary into account
        if self.fixed_boundary:
            self.flow_loss += self.weight * (self.height - sum(self.row_height)) ** 2 * len(self.row_height)


# flowing around a fixed area layout
class FlowAroundFix(Flow):

    def __init__(self, name, fixed_top, fixed_bottom, fixed_left, fixed_right, widget_list, parent):
        super().__init__(name, widget_list, parent)
        self.fixed_top = fixed_top
        self.fixed_bottom= fixed_bottom
        self.fixed_left = fixed_left
        self.fixed_right = fixed_right

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
    
        # calculate the flow result
        result = flow_around_fixed_area(self.width, self.height, \
                           self.fixed_top, self.fixed_bottom, self.fixed_left, self.fixed_right, \
                           self.pref_w_list, self.pref_h_list)

        if result == None:
            return "No Solution!"
        else:
            self.result_index_upper, self.result_index_middle, self.result_index_lower, \
            self.row_width_upper, self.row_width_middle, self.row_width_lower, \
            self.row_height_upper, self.row_height_middle, self.row_height_lower, \
            self.end_index_upper, self.end_index_middle, best_loss = result
            self.flow_loss += best_loss

        # Compute the additional loss for the upper area
        self.flow_loss += compute_additional_loss(self.result_index_upper, self.row_width_upper, \
                                                    self.row_height_upper, self.widget_list, \
                                                    self.max_w_list, self.min_w_list, \
                                                    self.max_h_list, self.min_h_list)

        # Compute the additional loss for the middle area
        self.flow_loss += compute_additional_loss_for_middle_area(self.result_index_middle, self.row_width_middle, \
                                                    self.row_height_middle, self.widget_list, \
                                                    self.max_w_list, self.min_w_list, \
                                                    self.max_h_list, self.min_h_list, self.end_index_upper)

        # Compute the additional loss for the lower area
        self.flow_loss += compute_additional_loss(self.result_index_lower, self.row_width_lower, \
                                                    self.row_height_lower, self.widget_list, \
                                                    self.max_w_list, self.min_w_list, \
                                                    self.max_h_list, self.min_h_list, self.end_index_middle)

        # the bottom boundary of the last widget in the flow sublayout is the same as
        # the bottom boundary of the flow sublayout
        if self.variables[self.name + "_b"].value == None:
            bottom_constraint = (self.variables[self.name + "_b"] \
                                == self.variables[self.name + "_t"] + sum(self.row_height))
            self.constraints += [bottom_constraint]


# Vertical flow layout
class VerticalFlow(Flow):

    # add constraint specifications
    def constraint_spec(self):
        
        # initialize flow loss
        self.flow_loss = 0
        
        # fixed boundary distance
        if self.boundary_distance != None:
            boundary_distance_constraint = (self.variables[self.name + "_r"] \
                                            == self.variables[self.name + "_l"] + self.boundary_distance)
            self.constraints += [boundary_distance_constraint]

        # we compute the preferred widgets in each row
        if not hasattr(self, 'pref_col'):
            self.copied_tree = False
        if self.copied_tree:

            # go back to the column/row it belongs to and add corresponding constraints
            self.belongs_to.back = True
            self.belongs_to.constraint_spec()

            # add upper tree variables, constraints, objectives to this node
            self.update_from_upper_tree()

        else:

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

            # if it is the original tree, then we apply our heuristics to get the min/pref/max number of cols
            if self.connect_to == None:
                self.min_col = 1 # get_num_cols(self.height, self.min_h_list)
                self.pref_col = get_num_cols(self.height, self.pref_h_list)
                self.max_col = get_num_cols(self.height, self.max_h_list)
            else:
                # if it is connected to another flow then we also need to count the widgets in the connected flow
                self.min_col = 1
                self.pref_col = get_num_cols(self.height, self.pref_h_list)
                self.max_col = get_num_cols(self.height, self.max_h_list + self.connect_to.max_h_list)

            # put all the possible number of columns in the list
            if not self.balanced:
                self.possible_smaller_num = list(range(self.pref_col - 1, self.min_col - 1, -1))
                self.possible_larger_num = list(range(self.pref_col + 1, self.max_col + 1))
            else:
                for i in range(self.pref_col - 1, self.min_col - 1, -1):
                    if i in self.factors:
                        self.possible_smaller_num.append(i)
                for i in range(self.pref_col + 1, self.max_col + 1):
                    if i in self.factors:
                        self.possible_larger_num.append(i)


                        
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
        result = vertical_flow(self.width, \
                              self.height, self.pref_col, self.pref_w_list, self.pref_h_list, self.optional_index_weight_dict, self.fixed_boundary)
        if result == None:
            self.flow_loss = inf
            return "No Solution!"
        else:
            self.result_index, self.row_height, self.row_width, flow_loss = result
            self.flow_loss += flow_loss

        # The loss is the distance between preferred sizes and result sizes
        self.flow_loss += compute_loss(self.result_index, self.row_height, self.row_width, \
                                        self.pref_h_list, self.pref_w_list)

        for i in range(self.pref_col):
        
            # check whether the widget size is larger than the max size or min size
            # if so, add more loss
            for j in range(len(self.result_index[i])):
                if self.row_height[i][j] > self.max_h_list[self.result_index[i][j]]:
                    self.flow_loss += 10 * self.weight * (self.row_height[i][j] \
                                                          - self.max_h_list[self.result_index[i][j]]) ** 2
                elif self.row_height[i][j] < self.min_h_list[self.result_index[i][j]]:
                    self.flow_loss += 10 * self.weight * (self.row_height[i][j] \
                                                          - self.min_h_list[self.result_index[i][j]]) ** 2
                if self.row_width[i] > self.max_w_list[self.result_index[i][j]]:
                    self.flow_loss += 10 * self.weight * (self.row_width[i] \
                                                          - self.max_w_list[self.result_index[i][j]]) ** 2
                elif self.row_width[i] < self.min_w_list[self.result_index[i][j]]:
                    self.flow_loss += 10 * self.weight * (self.row_width[i] \
                                                              - self.min_w_list[self.result_index[i][j]]) ** 2

        # the right boundary of the last widget in the flow sublayout is the same as
        # the right boundary of the flow sublayout
        if self.variables[self.name + "_r"].value == None:
            right_constraint = (self.variables[self.name + "_r"] \
                                 == self.variables[self.name + "_l"] + sum(self.row_width))
            self.constraints += [right_constraint]

        # if the right boundary is fixed, then we also need to take
        # the empty space to the right boundary into account
        if self.fixed_boundary:
            self.flow_loss += self.weight * (self.width - sum(self.row_width)) ** 2 * len(self.row_width)








