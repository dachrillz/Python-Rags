class SynAttr():
    '''
    This class is the Synthesized Attribute Class.

    - Type of Class is the class node that is to be attributed.
    - Attribute name is the name of the attribute

    - self.name is the name of the attribute that is to be given an equation
    - the expression is an expression that we are to implement.
    '''
    def __init__(self, type_of_class, attribute_name):
        self.type_of_class = type_of_class
        self.attribute_name = attribute_name

    def equation(self, name, expression):
        self.name = name
        self.expression = expression


class MinTree():
    """
    This is a class that defines the attributes we want to give to the a tree.

    That is, this is the class where one defines the reference attribute grammar.
    This is also the class we expect the user to define!

    The user of this package Declares attributes, and then Defines equations for these attributes.
    """

    def __init__(self):
        #Declare attributes
        self.leaf = SynAttr("Leaf", "localmin")
        self.pair = SynAttr("Pair", "localmin")

        #Define their equations
        self.leaf.equation('localmin', 'Leaf.value') #The right most argument here means that we have to evaluate a python expression
        #self.pair.equation('localmin', 'min(Pair.left.value, Pair.right.value)') #This is an example of an expression that we want to be able to parse.
        self.pair.equation('localmin', '42')

        #@TODO: Everything between these lines should be automated, and not be a concern for the user.
        self.attribute_dict = {}

        self.attribute_dict['Leaf']  = self.leaf
        self.attribute_dict['Pair']  = self.pair

    def get_attribute_dict(self):
        return self.attribute_dict
        #######################################################

class Weaver:
    """
    This is the class that weaves together the attribute grammar with a tree.

    Note, this is a rough first draft.
    """

    def __init__(self, class_to_weave, attribute_class):
        self.instance = class_to_weave
        self.attribute_class = attribute_class() #An instance of the user defined attribute class


    def evaluate_expression(self, node, expression):
        """
        This function later has to be expanded to a full blown parser/evaluator
        that can handle Python expressions.

        Right not it was simply crudly implemented to handle straight numbers and direct members of the node reference.
        (That is in jastadd for example, node.minvalue = node.value, where node.value was defined when constructing the ast)
        """

        #this is a very crude implementation for now just to demonstrate that this works.
        expr = expression.expression
        if expr.isdigit():
            return int(expr)
        else:
            import collections
            qualified_members = collections.deque(expr.split('.')) #the idea here is simply that we split on '.' to find children
            qualified_members.popleft() #Throw away the reference to oneself
            field_to_retrieve = qualified_members.popleft() #Note this only works for with a single dot for now, since we assume this pop brings a string.
            ret = getattr(node, field_to_retrieve)
            return int(ret)


    def traverse_and_inject(self):
        #This implementation requires that the tree has
        #a traversal algorithm that exposes each node.
        attribute_dict = self.attribute_class.get_attribute_dict()
        for node in self.instance.traverse():

            #We look at the name of the class if it matches any class name in synthesized attributes, we evaluate the equation to and add the attr. to the node.
            if node.__class__.__name__ in attribute_dict:
                name_of_attribute = attribute_dict[node.__class__.__name__].attribute_name #Get attribute name
                evaluated_expression = self.evaluate_expression(node,attribute_dict[node.__class__.__name__]) #Evaluate the expression
                self.to_be_injected(node, name_of_attribute, evaluated_expression) #inject the attribute into the tree.

    def to_be_injected(self, node, name_of_attribute, attribute):
        #1st arg is a class instance
        #2nd arg is name of attribute
        #3rd arg is the attribute to be set
        setattr(node, name_of_attribute, attribute)



#########################################################
#
# Example implementation of a tree class in Python
#
##########################################################

#The abstract class construct has to be imported in Python
from abc import ABC

class Program:

    def __init__(self, node):
        self.node = node

    def traverse_tree_aux(self, node, result):
        '''
        Support Function for the tree traversal
        '''

        result.append(node)

        if isinstance(node.left, Leaf):
            result.append(node.left)
        else:
            self.traverse_tre_aux(node.left, result)

        if isinstance(node.right, Leaf):
            result.append(node.right)
        else:
            self.traverse_tree_aux(node.right, result)

    def traverse(self):
        """
        In order traversal of the tree.

        Returns all the nodes in a list.
        """
        result = [self] #The result is currently stored as a list, should this be a generator? Also how to enforce such that a tree actually behaves nicely.

        first_node = self.node

        self.traverse_tree_aux(first_node, result)

        return result


class Node(ABC):

    def __init__(self):
        super().__init__()

class Pair(Node):
    def __init__(self, left, right):
        self.left = left
        self.right = right


class Leaf(Node):
    def __init__(self, value):
        self.value = value


if __name__ == '__main__':
    #an instance of this class
    instance = Program(Pair(Leaf(1), Pair(Leaf(2), Leaf(3))))

    #Instance of the weaver class
    weaver = Weaver(instance, MinTree) #Note here that we can simply give it a reference to the class MinTree!

    weaver.traverse_and_inject()

    allnodes = instance.traverse() #this simply gets all the nodes in the tree after the tree has been attributed, so one can print the nodes to check the result.

    for item in allnodes:
        try:
            print(str(item), item.localmin)
        except Exception as e:
            pass
